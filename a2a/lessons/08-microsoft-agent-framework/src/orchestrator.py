"""
Lesson 08 — OrchestratorAgent using Microsoft Agent Framework.

The OrchestratorAgent wraps the three validation tool functions and calls
Kimi-K2-Thinking (Azure AI Foundry) to reason through the combined evidence
and produce a structured ValidationReport.

Authentication
--------------
Uses AZURE_OPENAI_ENDPOINT + AZURE_AI_API_KEY from the environment.
No az login required — suitable for CI / shared environments.

Environment variables required
-------------------------------
  AZURE_OPENAI_ENDPOINT          e.g. https://<name>.openai.azure.com
  AZURE_AI_API_KEY               API key for the Azure OpenAI resource
  AZURE_AI_MODEL_DEPLOYMENT_NAME e.g. Kimi-K2-Thinking  (default: Kimi-K2-Thinking)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Literal

from agent_framework import Agent
from agent_framework.azure import AzureOpenAIChatClient  # type: ignore[attr-defined]  # pylint: disable=no-name-in-module

from loan_data import LoanApplication
from validation_rules import lookup_policy_notes, run_hard_checks, run_soft_checks


# ─── Output Model ─────────────────────────────────────────────────────────────


@dataclass
class ValidationReport:  # pylint: disable=too-many-instance-attributes
    """Structured output produced by the OrchestratorAgent."""

    applicant_id: str
    full_name: str
    verdict: Literal["APPROVED", "NEEDS_REVIEW", "DECLINED"]

    # Deterministic rule results (populated before LLM call)
    hard_check_results: list[dict] = field(default_factory=list)
    soft_check_results: list[dict] = field(default_factory=list)

    # LLM-generated content
    reasoning_summary: str = ""
    conditions: list[str] = field(default_factory=list)  # underwriter conditions
    risk_flags: list[str] = field(default_factory=list)  # actionable flags
    compensating_factors: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        """Human-readable report card."""
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


# ─── OrchestratorAgent ────────────────────────────────────────────────────────

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
Think step-by-step before writing the JSON — consider every rule result,
every exception, and every compensating factor.
"""


class OrchestratorAgent:  # pylint: disable=too-few-public-methods
    """Wraps Microsoft Agent Framework + Kimi-K2-Thinking for loan validation."""

    def __init__(self) -> None:
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        api_key = os.environ["AZURE_AI_API_KEY"]
        model = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2-Thinking")

        # AzureOpenAIChatClient uses the Chat Completions API,
        # which Kimi-K2-Thinking supports (Responses API is not
        # available for all model deployments).
        self._chat_client = AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=model,
        )

        self._agent: Agent = self._chat_client.as_agent(
            name="LoanValidatorOrchestrator",
            instructions=_SYSTEM_INSTRUCTIONS,
            tools=[run_hard_checks, run_soft_checks, lookup_policy_notes],
        )

    async def validate(self, application: LoanApplication) -> ValidationReport:
        """Run the full validation pipeline for one loan application.

        Steps
        -----
        1. Run deterministic hard checks (tool call — no LLM needed)
        2. Run deterministic soft checks (tool call — no LLM needed)
        3. Ask Kimi-K2-Thinking to synthesise all evidence into a verdict
        4. Parse the JSON verdict and build a ValidationReport
        """
        app_json = json.dumps(application.to_dict())

        # ── Step 1 & 2: deterministic checks ─────────────────────
        hard_results: list[dict] = json.loads(run_hard_checks(app_json))
        soft_results: list[dict] = json.loads(run_soft_checks(app_json))

        # ── Step 3: LLM reasoning ─────────────────────────────────
        prompt = _build_prompt(application, hard_results, soft_results)
        raw = await self._agent.run(prompt)
        raw_text = str(raw)

        # ── Step 4: parse verdict ─────────────────────────────────
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


# ─── Prompt builder ───────────────────────────────────────────────────────────


def _build_prompt(
    app: LoanApplication,
    hard: list[dict],
    soft: list[dict],
) -> str:
    """Construct the reasoning prompt including all check results."""
    hard_summary = _format_results(hard)
    soft_summary = _format_results(soft)

    return (
        f"Loan Application Pre-Screening\n"
        f"{'='*50}\n"
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
        f"Has LOE    : {app.has_letter_of_explanation}\n"
        f"\n"
        f"HARD CHECK RESULTS\n"
        f"{'─'*50}\n"
        f"{hard_summary}\n"
        f"\n"
        f"SOFT CHECK RESULTS\n"
        f"{'─'*50}\n"
        f"{soft_summary}\n"
        f"\n"
        f"Based on the above, produce the final pre-screening verdict.\n"
        f"Think carefully about FHA-specific exceptions, compensating factors, "
        f"and what conditions the underwriter must verify before approval.\n"
    )


def _format_results(results: list[dict]) -> str:
    """Format rule results for the prompt."""
    lines = []
    for r in results:
        status = "PASS ✓" if r["passed"] else f"FAIL ✗ [{r['severity'].upper()}]"
        lines.append(f"  {r['rule']:30s}  {status}")
        lines.append(f"    → {r['message']}")
    return "\n".join(lines)


def _parse_verdict(raw: str) -> dict:
    """Extract the JSON verdict from the model's raw response text."""
    # Strip markdown code fences if present
    text = raw.strip()
    if "```" in text:
        start = text.find("{", text.find("```"))
        end = text.rfind("}") + 1
        text = text[start:end] if start >= 0 and end > 0 else text
    # Find outermost JSON object
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        # Graceful fallback — preserve raw reasoning as summary
        return {
            "verdict": "NEEDS_REVIEW",
            "reasoning_summary": text[:800],
            "conditions": [
                "Manual underwriter review required — structured output parsing failed."
            ],
            "risk_flags": [],
            "compensating_factors": [],
        }
