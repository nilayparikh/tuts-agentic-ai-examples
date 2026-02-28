"""
Lesson 11 — OrchestratorAgent using CrewAI.

The OrchestratorAgent wraps the three validation tool functions as CrewAI
tools, assigns them to role-based agents, and runs a sequential crew.
Kimi-K2 (Azure AI Foundry) is accessed via LiteLLM's AzureOpenAI wrapper.

Reuses ``loan_data.py`` and ``validation_rules.py`` from Lesson 08 —
same problem, different framework.

Environment variables required (loaded from ``_examples/.env``):
    AZURE_OPENAI_ENDPOINT
    AZURE_AI_API_KEY
    AZURE_AI_MODEL_DEPLOYMENT_NAME   (default: Kimi-K2)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Literal

from crewai import Agent as CrewAgent, Crew, Process, Task as CrewTask
from crewai.tools import BaseTool as CrewBaseTool

from loan_data import LoanApplication
from validation_rules import lookup_policy_notes, run_hard_checks, run_soft_checks


# ─── Output Model ─────────────────────────────────────────────────────────────


@dataclass
class ValidationReport:  # pylint: disable=too-many-instance-attributes
    """Structured output produced by the OrchestratorAgent."""

    applicant_id: str
    full_name: str
    verdict: Literal["APPROVED", "NEEDS_REVIEW", "DECLINED"]
    hard_check_results: list[dict] = field(default_factory=list)
    soft_check_results: list[dict] = field(default_factory=list)
    reasoning_summary: str = ""
    conditions: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    compensating_factors: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        v_sym = {"APPROVED": "✅", "NEEDS_REVIEW": "⚠️", "DECLINED": "❌"}[self.verdict]
        lines = [
            f"{'─'*60}",
            f"VALIDATION REPORT  {v_sym} {self.verdict}",
            f"Applicant  : {self.full_name} ({self.applicant_id})",
            f"{'─'*60}",
            "",
            "■ REASONING",
            self.reasoning_summary,
            "",
        ]
        if self.compensating_factors:
            lines += (
                ["■ COMPENSATING FACTORS"]
                + [f"  + {f}" for f in self.compensating_factors]
                + [""]
            )
        if self.risk_flags:
            lines += ["■ RISK FLAGS"] + [f"  ⚑ {f}" for f in self.risk_flags] + [""]
        if self.conditions:
            lines += (
                ["■ UNDERWRITER CONDITIONS"]
                + [f"  {i+1}. {c}" for i, c in enumerate(self.conditions)]
                + [""]
            )
        lines.append(f"{'─'*60}")
        return "\n".join(lines)


# ─── CrewAI Tool Wrappers ────────────────────────────────────────────────────


class HardCheckTool(CrewBaseTool):
    """Execute hard-fail business rules against a loan application."""

    name: str = "run_hard_checks"
    description: str = (
        "Execute hard-fail business rules against a loan application. "
        "Pass the full JSON string from LoanApplication.to_dict(). "
        "Returns JSON list of rule results."
    )

    def _run(self, application_json: str) -> str:
        return run_hard_checks(application_json)


class SoftCheckTool(CrewBaseTool):
    """Execute soft advisory checks against a loan application."""

    name: str = "run_soft_checks"
    description: str = (
        "Execute soft advisory checks against a loan application. "
        "Pass the full JSON string from LoanApplication.to_dict(). "
        "Returns JSON list of advisory rule results."
    )

    def _run(self, application_json: str) -> str:
        return run_soft_checks(application_json)


class PolicyLookupTool(CrewBaseTool):
    """Look up policy guidance for underwriting questions."""

    name: str = "lookup_policy_notes"
    description: str = (
        "Look up policy guidance for a specific underwriting question. "
        "Returns policy memo text."
    )

    def _run(self, question: str) -> str:
        return lookup_policy_notes(question)


# ─── LLM Configuration ──────────────────────────────────────────

_AZURE_MODEL_STRING = "azure/{deployment}"


def _get_llm_config() -> dict:
    """Return the LLM config dict for CrewAI agents."""
    deployment = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2-Thinking")
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_AI_API_KEY"]

    # CrewAI uses litellm under the hood
    os.environ.setdefault("AZURE_API_BASE", endpoint)
    os.environ.setdefault("AZURE_API_KEY", api_key)
    os.environ.setdefault("AZURE_API_VERSION", "2025-04-01-preview")

    return {"model": f"azure/{deployment}"}


# ─── OrchestratorAgent ────────────────────────────────────────────────────────


class OrchestratorAgent:
    """Wraps CrewAI crew + Kimi-K2 for loan validation."""

    def __init__(self) -> None:
        llm_config = _get_llm_config()

        # Define role-based agents
        self._compliance_analyst = CrewAgent(
            role="Compliance Analyst",
            goal="Run all hard-fail and soft advisory checks against the loan application",
            backstory=(
                "You are a meticulous mortgage compliance analyst with deep knowledge "
                "of conventional, FHA, and VA loan requirements. You run deterministic "
                "rule checks and report the results precisely."
            ),
            tools=[HardCheckTool(), SoftCheckTool()],
            llm=llm_config["model"],
            verbose=False,
        )

        self._underwriter = CrewAgent(
            role="Senior Underwriter",
            goal="Synthesise rule check results into a final verdict with conditions",
            backstory=(
                "You are a senior mortgage underwriter with 20 years of experience. "
                "You analyse compliance results, consider FHA exceptions, compensating "
                "factors, and produce a structured JSON verdict."
            ),
            tools=[PolicyLookupTool()],
            llm=llm_config["model"],
            verbose=False,
        )

    async def validate(self, application: LoanApplication) -> ValidationReport:
        """Run the full validation pipeline for one loan application."""
        app_json = json.dumps(application.to_dict())

        # Step 1 & 2: deterministic checks (no LLM)
        hard_results: list[dict] = json.loads(run_hard_checks(app_json))
        soft_results: list[dict] = json.loads(run_soft_checks(app_json))

        # Step 3: CrewAI crew for LLM reasoning
        prompt = _build_prompt(application, hard_results, soft_results)

        analysis_task = CrewTask(
            description=f"Analyse the following loan application data:\n\n{app_json}",
            expected_output="Hard check and soft check results in structured format",
            agent=self._compliance_analyst,
        )

        verdict_task = CrewTask(
            description=(
                f"Based on ALL rule check results below, produce the final verdict.\n\n"
                f"{prompt}\n\n"
                f"Respond with ONLY valid JSON matching this schema:\n"
                f'{{"verdict": "APPROVED"|"NEEDS_REVIEW"|"DECLINED", '
                f'"reasoning_summary": "...", "compensating_factors": [...], '
                f'"risk_flags": [...], "conditions": [...]}}'
            ),
            expected_output="A valid JSON object with verdict, reasoning, and conditions",
            agent=self._underwriter,
        )

        crew = Crew(
            agents=[self._compliance_analyst, self._underwriter],
            tasks=[analysis_task, verdict_task],
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff()
        raw_text = str(result)

        # Step 4: parse verdict
        verdict_data = _parse_verdict(raw_text)

        return ValidationReport(
            applicant_id=application.applicant_id,
            full_name=application.full_name,
            verdict=verdict_data.get("verdict", "NEEDS_REVIEW"),
            hard_check_results=hard_results,
            soft_check_results=soft_results,
            reasoning_summary=verdict_data.get("reasoning_summary", raw_text),
            conditions=verdict_data.get("conditions", []),
            risk_flags=verdict_data.get("risk_flags", []),
            compensating_factors=verdict_data.get("compensating_factors", []),
        )


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _build_prompt(app: LoanApplication, hard: list[dict], soft: list[dict]) -> str:
    hard_summary = _format_results(hard)
    soft_summary = _format_results(soft)
    return (
        f"Loan Application Pre-Screening\n{'='*50}\n"
        f"Applicant  : {app.full_name} ({app.applicant_id})\n"
        f"Loan type  : {app.loan_type.upper()}\n"
        f"Credit score: {app.credit_score}\n"
        f"Annual income: ${app.annual_income_usd:,.0f}\n"
        f"DTI ratio  : {app.dti_ratio:.1%}\n"
        f"LTV ratio  : {app.ltv_ratio:.1%}\n"
        f"Employment : {app.employment_months} months\n"
        f"Derogatory marks: {app.derogatory_marks}\n"
        f"Mark notes : {app.derogatory_mark_notes}\n"
        f"First-time homebuyer: {app.first_time_homebuyer}\n"
        f"Has LOE    : {app.has_letter_of_explanation}\n\n"
        f"HARD CHECK RESULTS\n{'─'*50}\n{hard_summary}\n\n"
        f"SOFT CHECK RESULTS\n{'─'*50}\n{soft_summary}\n\n"
        f"Produce the final pre-screening verdict.\n"
    )


def _format_results(results: list[dict]) -> str:
    lines = []
    for r in results:
        status = "PASS ✓" if r["passed"] else f"FAIL ✗ [{r['severity'].upper()}]"
        lines.append(f"  {r['rule']:30s}  {status}")
        lines.append(f"    → {r['message']}")
    return "\n".join(lines)


def _parse_verdict(raw: str) -> dict:
    text = raw.strip()
    if "```" in text:
        start = text.find("{", text.find("```"))
        end = text.rfind("}") + 1
        text = text[start:end] if start >= 0 and end > 0 else text
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        return {
            "verdict": "NEEDS_REVIEW",
            "reasoning_summary": text[:800],
            "conditions": ["Manual review required — parsing failed."],
            "risk_flags": [],
            "compensating_factors": [],
        }
