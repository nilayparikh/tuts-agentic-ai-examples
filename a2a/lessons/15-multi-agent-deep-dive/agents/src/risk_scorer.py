"""
RiskScorerAgent — Compute a 0-100 risk score for loan applications.

Combines deterministic rule scoring (40% weight) with LLM-based reasoning
(60% weight) for a composite risk score.

The LLM provider is selected via the PROVIDER env var (see model_provider.py):
  - github           →  GitHub Models (Phi-4) — DEFAULT
  - MicrosoftFoundry →  Azure AI Foundry (Kimi-K2-Thinking)
  - LocalFoundry     →  Foundry Local (Qwen2.5, etc.)
"""

from __future__ import annotations

import json
import logging
import os

from model_provider import get_model_config
from telemetry import tracer

logger = logging.getLogger("risk_scorer")

# ── Deterministic rule thresholds ─────────────────────────────────────────────

_RULE_THRESHOLDS = {
    "conventional": {
        "min_credit_score": 620,
        "max_dti": 0.43,
        "max_ltv": 0.95,
        "min_employment_months": 24,
        "max_derogatory_marks": 2,
    },
    "fha": {
        "min_credit_score": 580,
        "max_dti": 0.43,
        "max_ltv": 0.965,
        "min_employment_months": 24,
        "max_derogatory_marks": 3,
    },
    "va": {
        "min_credit_score": 580,
        "max_dti": 0.41,
        "max_ltv": 1.00,
        "min_employment_months": 24,
        "max_derogatory_marks": 2,
    },
}

_LLM_SYSTEM_PROMPT = """\
You are an expert mortgage risk assessor. Given a loan application with its
deterministic rule check results, produce a risk assessment score from 0 to 100.

0 = no risk (perfect applicant), 100 = maximum risk (certain default).

Consider:
- Credit history and score relative to loan type requirements
- Debt-to-income ratio and its trajectory
- Employment stability
- Derogatory marks and explanations
- Compensating factors (reserves, first-time buyer programmes, LOE)

Respond with ONLY valid JSON:
{
  "llm_score": <0-100>,
  "reasoning": "<2-3 sentence explanation>",
  "risk_factors": ["<factor1>", ...],
  "compensating_factors": ["<factor1>", ...]
}
"""


class RiskScorerAgent:
    """Score loan applications using rules + LLM reasoning."""

    def __init__(self) -> None:
        config = get_model_config()
        self._client = config.client
        self._model = config.model
        self._provider_name = config.display_name
        logger.info("RiskScorerAgent initialised with %s", self._provider_name)

    async def score(self, application_json: str) -> str:
        """Compute risk score for a normalized loan application.

        Returns JSON with composite score, rule score, LLM score, and reasoning.
        """
        with tracer.start_as_current_span("compute_risk_score") as span:
            app = json.loads(application_json)
            app_id = app.get("applicant_id", "unknown")
            span.set_attribute("applicant_id", app_id)
            logger.info(
                "[%s] ── Risk Scoring Started ──────────────────────────",
                app_id,
            )
            logger.info(
                "[%s] Provider: %s | Credit: %s | DTI: %s | LTV: %s",
                app_id,
                self._provider_name,
                app.get("credit_score"),
                app.get("dti_ratio"),
                app.get("ltv_ratio"),
            )

            # Deterministic rule scoring (40% weight)
            with tracer.start_as_current_span("rule_evaluation"):
                rule_score = self._compute_rule_score(app)
                span.set_attribute("rule_score", rule_score)
                logger.info("[%s] Rule score: %d/100", app_id, rule_score)

            # LLM reasoning score (60% weight)
            with tracer.start_as_current_span("llm_reasoning"):
                logger.info(
                    "[%s] Calling LLM (%s) for risk assessment…",
                    app_id,
                    self._provider_name,
                )
                llm_result = await self._llm_assess(app, rule_score)
                llm_score = llm_result.get("llm_score", 50)
                span.set_attribute("llm_score", llm_score)
                logger.info("[%s] LLM score: %d/100", app_id, llm_score)
                logger.info(
                    "[%s] LLM reasoning: %s",
                    app_id,
                    llm_result.get("reasoning", "N/A"),
                )

            # Composite
            final_score = int(rule_score * 0.4 + llm_score * 0.6)
            category = self._categorize(final_score)

            span.set_attribute("final_score", final_score)
            span.set_attribute("category", category)

            logger.info(
                "[%s] Composite: %d (rule=%d×0.4 + llm=%d×0.6) → %s",
                app_id,
                final_score,
                rule_score,
                llm_score,
                category,
            )
            logger.info(
                "[%s] Risk factors: %s",
                app_id,
                llm_result.get("risk_factors", []),
            )
            logger.info(
                "[%s] Compensating: %s",
                app_id,
                llm_result.get("compensating_factors", []),
            )

            return json.dumps(
                {
                    "applicant_id": app_id,
                    "score": final_score,
                    "rule_score": rule_score,
                    "llm_score": llm_score,
                    "category": category,
                    "reasoning": llm_result.get("reasoning", ""),
                    "risk_factors": llm_result.get("risk_factors", []),
                    "compensating_factors": llm_result.get("compensating_factors", []),
                }
            )

    def _compute_rule_score(self, app: dict) -> int:
        """Score 0-100 based on deterministic rules. Higher = more risk."""
        loan_type = app.get("loan_type", "conventional")
        thresholds = _RULE_THRESHOLDS.get(loan_type, _RULE_THRESHOLDS["conventional"])

        score = 0
        total_checks = 5

        # Credit score check
        cs = app.get("credit_score", 0)
        min_cs = thresholds["min_credit_score"]
        if cs < min_cs:
            score += 25  # Hard fail
        elif cs < min_cs + 50:
            score += 10  # Marginal

        # DTI check
        dti = app.get("dti_ratio", 0)
        max_dti = thresholds["max_dti"]
        if dti > max_dti:
            score += 25
        elif dti > max_dti - 0.05:
            score += 10

        # LTV check
        ltv = app.get("ltv_ratio", 0)
        max_ltv = thresholds["max_ltv"]
        if ltv > max_ltv:
            score += 20
        elif ltv > max_ltv - 0.05:
            score += 8

        # Employment check
        emp = app.get("employment_months", 0)
        if emp < thresholds["min_employment_months"]:
            score += 15
        elif emp < thresholds["min_employment_months"] + 6:
            score += 5

        # Derogatory marks
        marks = app.get("derogatory_marks", 0)
        if marks > thresholds["max_derogatory_marks"]:
            score += 15
        elif marks > 0:
            score += 5

        return min(score, 100)

    async def _llm_assess(self, app: dict, rule_score: int) -> dict:
        """Ask LLM to assess risk and provide reasoning."""
        prompt = (
            f"Loan Application Risk Assessment\n"
            f"================================\n"
            f"Applicant: {app.get('full_name', 'N/A')} ({app.get('applicant_id', 'N/A')})\n"
            f"Loan Type: {app.get('loan_type', 'N/A')}\n"
            f"Credit Score: {app.get('credit_score', 'N/A')}\n"
            f"DTI Ratio: {app.get('dti_ratio', 'N/A')}\n"
            f"LTV Ratio: {app.get('ltv_ratio', 'N/A')}\n"
            f"Employment: {app.get('employment_months', 'N/A')} months\n"
            f"Derogatory Marks: {app.get('derogatory_marks', 'N/A')}\n"
            f"Mark Notes: {app.get('derogatory_mark_notes', 'None')}\n"
            f"First-time Homebuyer: {app.get('first_time_homebuyer', False)}\n"
            f"Letter of Explanation: {app.get('has_letter_of_explanation', False)}\n"
            f"\nDeterministic Rule Score: {rule_score}/100 (higher = more risk)\n"
        )

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": _LLM_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=250,
                timeout=45,
            )
            raw = response.choices[0].message.content or "{}"
            logger.debug("[LLM] Raw response: %s", raw[:500])
            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
            return json.loads(raw)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error(
                "LLM assessment failed (%s): %s — using fallback score=50",
                type(exc).__name__,
                exc,
            )
            return {
                "llm_score": 50,
                "reasoning": f"LLM assessment unavailable ({type(exc).__name__})",
            }

    @staticmethod
    def _categorize(score: int) -> str:
        """Map composite score to decision category."""
        if score <= 40:
            return "AUTO_APPROVE"
        if score >= 80:
            return "AUTO_DECLINE"
        return "ESCALATE"
