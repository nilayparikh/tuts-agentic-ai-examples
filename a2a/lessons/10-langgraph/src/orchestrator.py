"""
Lesson 10 — OrchestratorAgent using LangGraph ReAct pattern.

The OrchestratorAgent uses LangGraph's ``create_react_agent`` to wrap the
three validation tool functions.  Kimi-K2 (Azure AI Foundry) is accessed
via ``langchain-openai``'s ``AzureChatOpenAI``.

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

from langchain_core.tools import tool as langchain_tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

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


# ─── LangChain Tool Wrappers ─────────────────────────────────────────────────


@langchain_tool
def lc_run_hard_checks(application_json: str) -> str:
    """Execute hard-fail business rules against a loan application.

    Pass the full JSON string from LoanApplication.to_dict().
    Returns JSON list of rule results — any with passed=False is
    an automatic disqualifier.
    """
    return run_hard_checks(application_json)


@langchain_tool
def lc_run_soft_checks(application_json: str) -> str:
    """Execute soft advisory checks against a loan application.

    Pass the full JSON string from LoanApplication.to_dict().
    Returns JSON list of advisory rule results for underwriter review.
    """
    return run_soft_checks(application_json)


@langchain_tool
def lc_lookup_policy_notes(question: str) -> str:
    """Look up policy guidance for a specific underwriting question.

    Falls back to built-in policy memo when the QAAgent is unavailable.
    """
    return lookup_policy_notes(question)


# ─── LLM + ReAct Agent ───────────────────────────────────────────────────────

_SYSTEM_INSTRUCTIONS = """\
You are a senior mortgage underwriting analyst with 20 years of experience.
You have already been given the results of deterministic rule checks.

Your task is to synthesise those results and produce a final pre-screening
verdict and a structured JSON report.

Rules for the verdict
---------------------
- APPROVED   : all hard checks passed, no unresolved risk flags
- DECLINED   : one or more hard checks failed that cannot be remediated
- NEEDS_REVIEW : hard checks pass (possibly via exceptions) but one or more
                  conditions require underwriter verification

Output — respond with ONLY valid JSON matching this schema:
{
  "verdict": "APPROVED" | "NEEDS_REVIEW" | "DECLINED",
  "reasoning_summary": "<2-4 sentence synthesis>",
  "compensating_factors": ["<factor1>", ...],
  "risk_flags": ["<flag1>", ...],
  "conditions": ["<condition for underwriter>", ...]
}

Do not include any text outside the JSON object.
"""


def _build_llm() -> AzureChatOpenAI:
    """Build an AzureChatOpenAI instance from environment variables."""
    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_AI_API_KEY"],
        azure_deployment=os.environ.get(
            "AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2-Thinking"
        ),
        api_version="2025-04-01-preview",
        temperature=0,
    )


# ─── OrchestratorAgent ────────────────────────────────────────────────────────


class OrchestratorAgent:
    """Wraps LangGraph ReAct agent + Kimi-K2 for loan validation."""

    def __init__(self) -> None:
        self._llm = _build_llm()
        self._tools = [lc_run_hard_checks, lc_run_soft_checks, lc_lookup_policy_notes]
        self._graph = create_react_agent(
            self._llm,
            tools=self._tools,
        )

    async def validate(self, application: LoanApplication) -> ValidationReport:
        """Run the full validation pipeline for one loan application."""
        app_json = json.dumps(application.to_dict())

        # Step 1 & 2: deterministic checks (no LLM)
        hard_results: list[dict] = json.loads(run_hard_checks(app_json))
        soft_results: list[dict] = json.loads(run_soft_checks(app_json))

        # Step 3: LLM reasoning via LangGraph ReAct
        prompt = _build_prompt(application, hard_results, soft_results)
        result = await self._graph.ainvoke(
            {"messages": [("system", _SYSTEM_INSTRUCTIONS), ("human", prompt)]}
        )

        # Extract final message text
        raw_text = ""
        if result.get("messages"):
            last_msg = result["messages"][-1]
            raw_text = getattr(last_msg, "content", str(last_msg))

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
        f"Based on the above, produce the final pre-screening verdict.\n"
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
