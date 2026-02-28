"""
Lesson 09 — OrchestratorAgent using Google Agent Development Kit (ADK).

The OrchestratorAgent wraps the three validation tool functions using ADK's
FunctionTool and LlmAgent.  Kimi-K2 (Azure AI Foundry) is accessed via the
LiteLlm adapter — no Vertex AI or Google Cloud dependency.

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

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool

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
    conditions: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
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


# ─── ADK Tool Wrappers ───────────────────────────────────────────────────────
# ADK discovers param names and docstrings automatically from type hints.


def adk_run_hard_checks(application_json: str) -> str:
    """Execute hard-fail business rules against a loan application.

    Pass the full JSON string from LoanApplication.to_dict().
    Returns JSON list of rule results — any with passed=False is
    an automatic disqualifier.
    """
    return run_hard_checks(application_json)


def adk_run_soft_checks(application_json: str) -> str:
    """Execute soft advisory checks against a loan application.

    Pass the full JSON string from LoanApplication.to_dict().
    Returns JSON list of advisory rule results for underwriter review.
    """
    return run_soft_checks(application_json)


def adk_lookup_policy_notes(question: str) -> str:
    """Look up policy guidance for a specific underwriting question.

    Falls back to built-in policy memo when the QAAgent is unavailable.
    """
    return lookup_policy_notes(question)


# ─── LLM Configuration ──────────────────────────────────────────


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


def _azure_model_string() -> str:
    """Build the ``azure/<deployment>`` model string for LiteLlm."""
    deployment = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2-Thinking")
    return f"azure/{deployment}"


def _configure_litellm_env() -> None:
    """Map project env vars to the names that litellm expects."""
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.environ.get("AZURE_AI_API_KEY", "")
    if endpoint:
        os.environ.setdefault("AZURE_API_BASE", endpoint)
    if api_key:
        os.environ.setdefault("AZURE_API_KEY", api_key)
    os.environ.setdefault("AZURE_API_VERSION", "2025-04-01-preview")


def _build_agent() -> LlmAgent:
    """Construct the LlmAgent with FunctionTool wrappers."""
    _configure_litellm_env()
    model = LiteLlm(model=_azure_model_string())

    return LlmAgent(
        name="LoanValidatorADK",
        description=(
            "Pre-screens residential mortgage applications using deterministic "
            "business rules and LLM reasoning to produce APPROVED / NEEDS_REVIEW "
            "/ DECLINED verdicts with full justification."
        ),
        model=model,
        instruction=_SYSTEM_INSTRUCTIONS,
        tools=[
            FunctionTool(func=adk_run_hard_checks),
            FunctionTool(func=adk_run_soft_checks),
            FunctionTool(func=adk_lookup_policy_notes),
        ],
    )


# ─── OrchestratorAgent ────────────────────────────────────────────────────────


class OrchestratorAgent:
    """Wraps Google ADK LlmAgent + Kimi-K2 for loan validation."""

    def __init__(self) -> None:
        self._agent = _build_agent()
        self._session_service = InMemorySessionService()
        self._runner = Runner(
            agent=self._agent,
            app_name="loan_validator_adk",
            session_service=self._session_service,
        )

    @property
    def agent(self) -> LlmAgent:
        """Return the underlying LlmAgent (for to_a2a())."""
        return self._agent

    async def validate(self, application: LoanApplication) -> ValidationReport:
        """Run the full validation pipeline for one loan application.

        Steps:
        1. Run deterministic hard checks (no LLM)
        2. Run deterministic soft checks (no LLM)
        3. Ask Kimi-K2 via ADK Runner to synthesise a verdict
        4. Parse the JSON verdict and build a ValidationReport
        """
        app_json = json.dumps(application.to_dict())

        # ── Step 1 & 2: deterministic checks ─────────────────────
        hard_results: list[dict] = json.loads(run_hard_checks(app_json))
        soft_results: list[dict] = json.loads(run_soft_checks(app_json))

        # ── Step 3: LLM reasoning via ADK Runner ─────────────────
        prompt = _build_prompt(application, hard_results, soft_results)
        session = await self._session_service.create_session(
            app_name="loan_validator_adk",
            user_id="system",
        )
        from google.genai import types as genai_types

        content = genai_types.Content(
            role="user",
            parts=[genai_types.Part(text=prompt)],
        )

        raw_text = ""
        async for event in self._runner.run_async(
            user_id="system",
            session_id=session.id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    raw_text = "".join(p.text for p in event.content.parts if p.text)

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
            "conditions": [
                "Manual underwriter review required — structured output parsing failed."
            ],
            "risk_flags": [],
            "compensating_factors": [],
        }
