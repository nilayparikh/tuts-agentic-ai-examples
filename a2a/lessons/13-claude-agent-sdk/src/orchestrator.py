"""
Lesson 13 — OrchestratorAgent using Claude-style agent patterns.

Demonstrates Anthropic's agent-building patterns (structured JSON schema tool
use, explicit conversation memory, iterative tool-call dispatch) applied to
the same loan validation problem as Lessons 08–12.

Unlike framework-native approaches, this lesson builds the agentic loop from
scratch using only the ``openai`` async client — showing what frameworks do
under the hood.  Kimi-K2-Thinking (Azure AI Foundry) is accessed via the
OpenAI-compatible endpoint.

Reuses ``loan_data.py`` and ``validation_rules.py`` from ``_common/src/``.

Environment variables required (loaded from ``_examples/.env``):
    AZURE_OPENAI_ENDPOINT
    AZURE_AI_API_KEY
    AZURE_AI_MODEL_DEPLOYMENT_NAME   (default: Kimi-K2-Thinking)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Literal

from openai import AsyncAzureOpenAI

from loan_data import LoanApplication
from validation_rules import lookup_policy_notes, run_hard_checks, run_soft_checks


# ─── Output Model ─────────────────────────────────────────────────────────────


@dataclass
class ValidationReport:
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
            f"{'─' * 60}",
            f"VALIDATION REPORT  {v_sym} {self.verdict}",
            f"Applicant  : {self.full_name} ({self.applicant_id})",
            f"{'─' * 60}",
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
                + [f"  {i + 1}. {c}" for i, c in enumerate(self.conditions)]
                + [""]
            )
        lines.append(f"{'─' * 60}")
        return "\n".join(lines)


# ─── JSON-Schema Tool Definitions (Claude-style) ─────────────────────────────

_TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "run_hard_checks",
            "description": (
                "Execute hard-fail business rules against a loan application. "
                "Hard fails are automatic disqualifiers. Returns JSON list of "
                "RuleResult dicts — any result with passed=false is a hard fail."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "application_json": {
                        "type": "string",
                        "description": (
                            "Full JSON string from LoanApplication.to_dict(). "
                            "Must include keys: credit_score, loan_type, "
                            "computed.dti_ratio, computed.ltv_ratio, "
                            "employment_months, derogatory_marks."
                        ),
                    },
                },
                "required": ["application_json"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_soft_checks",
            "description": (
                "Execute soft advisory checks against a loan application. "
                "Soft checks highlight risk factors or compensating factors "
                "for underwriter review. Returns JSON list of RuleResult dicts."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "application_json": {
                        "type": "string",
                        "description": "Full JSON string from LoanApplication.to_dict().",
                    },
                },
                "required": ["application_json"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_policy_notes",
            "description": (
                "Look up policy guidance for underwriting questions via the "
                "QAAgent (port 10001) or fallback to a structured policy memo."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": (
                            "A specific policy question about loan underwriting "
                            "rules or exceptions."
                        ),
                    },
                },
                "required": ["question"],
            },
        },
    },
]

# Map tool names to their implementations
_TOOL_DISPATCH: dict[str, callable] = {
    "run_hard_checks": lambda args: run_hard_checks(args["application_json"]),
    "run_soft_checks": lambda args: run_soft_checks(args["application_json"]),
    "lookup_policy_notes": lambda args: lookup_policy_notes(args["question"]),
}


# ─── System Prompt ────────────────────────────────────────────────────────────

_SYSTEM_INSTRUCTIONS = """\
You are a senior mortgage underwriter. Your task is to evaluate loan applications
by running deterministic business rules and synthesising a final verdict.

Workflow:
1. You will receive a loan application as structured data.
2. Call `run_hard_checks` with the full application JSON to get pass/fail results.
3. Call `run_soft_checks` with the full application JSON to get advisory results.
4. If any edge case or exception appears, call `lookup_policy_notes` for guidance.
5. Synthesise all results into a single JSON verdict.

Your final response MUST be a JSON object (no markdown fences) with these keys:
  "verdict": "APPROVED" | "NEEDS_REVIEW" | "DECLINED"
  "reasoning_summary": string explaining the decision
  "compensating_factors": list of strings
  "risk_flags": list of strings
  "conditions": list of strings (underwriter conditions for NEEDS_REVIEW)

Rules:
- Any hard-fail → automatic DECLINED unless an exception specifically applies
- All hard-pass + only soft flags → APPROVED with conditions if DTI/LTV is tight
- Exception applied → NEEDS_REVIEW (never auto-approve when exception was needed)
"""


# ─── OrchestratorAgent ────────────────────────────────────────────────────────


class OrchestratorAgent:
    """Claude-style agent: manual tool-call loop with conversation memory.

    Unlike framework-based approaches (ADK, LangGraph, CrewAI, OpenAI Agents),
    this implementation explicitly manages:
      • Tool definitions as JSON schemas (not decorators)
      • The tool-call → tool-result → next-turn loop
      • Conversation history accumulation
      • Per-request state isolation
    """

    def __init__(self) -> None:
        deployment = os.environ.get(
            "AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2-Thinking"
        )
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        api_key = os.environ["AZURE_AI_API_KEY"]

        self._client = AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2025-04-01-preview",
        )
        self._model = deployment

    async def validate(self, application: LoanApplication) -> ValidationReport:
        """Run the full validation pipeline for one loan application."""
        app_json = json.dumps(application.to_dict())

        # ── Step 1 & 2: deterministic checks (no LLM needed) ─────────────
        hard_results: list[dict] = json.loads(run_hard_checks(app_json))
        soft_results: list[dict] = json.loads(run_soft_checks(app_json))

        # ── Step 3: build initial prompt & conversation history ───────────
        prompt = _build_prompt(application, hard_results, soft_results)
        messages: list[dict] = [
            {"role": "system", "content": _SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": prompt},
        ]

        # ── Step 4: agentic tool-call loop (Claude-style) ────────────────
        max_iterations = 6  # safety limit
        for _ in range(max_iterations):
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=_TOOLS,
                temperature=0.2,
            )
            choice = response.choices[0]

            # If the model wants to call tools, execute them and continue
            if choice.finish_reason == "tool_calls" or (
                choice.message.tool_calls and len(choice.message.tool_calls) > 0
            ):
                # Append the assistant message (with tool_calls) to history
                messages.append(choice.message.model_dump())

                # Execute each tool call and append results
                for tc in choice.message.tool_calls:
                    fn_name = tc.function.name
                    fn_args = json.loads(tc.function.arguments)
                    handler = _TOOL_DISPATCH.get(fn_name)
                    if handler:
                        result = handler(fn_args)
                    else:
                        result = f"Unknown tool: {fn_name}"
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": (
                                result
                                if isinstance(result, str)
                                else json.dumps(result)
                            ),
                        }
                    )
                continue

            # No more tool calls — extract final text
            raw_text = choice.message.content or ""
            break
        else:
            raw_text = "(max tool-call iterations reached)"

        # ── Step 5: parse verdict ─────────────────────────────────────────
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
        f"Loan Application Pre-Screening\n{'=' * 50}\n"
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
        f"HARD CHECK RESULTS\n{'─' * 50}\n{hard_summary}\n\n"
        f"SOFT CHECK RESULTS\n{'─' * 50}\n{soft_summary}\n\n"
        f"If any edge cases, exceptions, or ambiguities appear in the results, "
        f"use lookup_policy_notes to check the relevant policy before deciding.\n\n"
        f"Produce the final pre-screening verdict as JSON.\n"
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
