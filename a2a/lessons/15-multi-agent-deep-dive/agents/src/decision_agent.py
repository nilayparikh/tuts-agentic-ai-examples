"""
DecisionAgent — Route loan applications based on risk score.

Auto-approves low-risk applications (score ≤ threshold), auto-declines
high-risk applications (score ≥ threshold), and flags borderline cases
for human review escalation.

Environment variables
---------------------
  AUTO_APPROVE_THRESHOLD   Score at or below = auto-approve (default: 40)
  AUTO_DECLINE_THRESHOLD   Score at or above = auto-decline (default: 80)
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

from telemetry import tracer

logger = logging.getLogger("decision_agent")


class DecisionAgent:
    """Make approve/decline/escalate decisions based on composite scores."""

    def __init__(self) -> None:
        self._approve_threshold = int(os.getenv("AUTO_APPROVE_THRESHOLD", "40"))
        self._decline_threshold = int(os.getenv("AUTO_DECLINE_THRESHOLD", "80"))
        logger.info(
            "DecisionAgent initialised — approve ≤%d | decline ≥%d | escalate %d–%d",
            self._approve_threshold,
            self._decline_threshold,
            self._approve_threshold + 1,
            self._decline_threshold - 1,
        )

    async def decide(self, pipeline_data_json: str) -> str:
        """Make a decision on the loan application.

        Expects JSON with keys: applicant_id, application, score, category,
        compliant, flags, reasoning.
        """
        with tracer.start_as_current_span("make_decision") as span:
            data = json.loads(pipeline_data_json)
            app_id = data.get("applicant_id", "unknown")
            score = data.get("score", 50)
            compliant = data.get("compliant", True)

            span.set_attribute("applicant_id", app_id)
            span.set_attribute("risk_score", score)
            span.set_attribute("compliant", compliant)

            logger.info(
                "[%s] ── Decision Routing Started ────────────────────",
                app_id,
            )
            logger.info(
                "[%s] Score: %d | Compliant: %s | Thresholds: approve≤%d, decline≥%d",
                app_id,
                score,
                compliant,
                self._approve_threshold,
                self._decline_threshold,
            )

            # Non-compliant applications with hard flags are auto-declined
            hard_flags = [
                f for f in data.get("flags", []) if f.get("severity") == "hard"
            ]
            if hard_flags:
                decision = "DECLINED"
                action = "AUTO_DECLINE"
                reason = (
                    f"Non-compliant: {len(hard_flags)} hard flag(s) — "
                    + "; ".join(f["message"] for f in hard_flags)
                )
            elif score <= self._approve_threshold:
                decision = "APPROVED"
                action = "AUTO_APPROVE"
                reason = (
                    f"Risk score {score} ≤ {self._approve_threshold} threshold. "
                    f"Auto-approved based on strong application profile."
                )
            elif score >= self._decline_threshold:
                decision = "DECLINED"
                action = "AUTO_DECLINE"
                reason = (
                    f"Risk score {score} ≥ {self._decline_threshold} threshold. "
                    f"Auto-declined due to high risk indicators."
                )
            else:
                decision = "PENDING_REVIEW"
                action = "ESCALATE"
                reason = (
                    f"Risk score {score} in escalation range "
                    f"({self._approve_threshold}–{self._decline_threshold}). "
                    f"Requires human review."
                )

            span.set_attribute("decision", decision)
            span.set_attribute("action", action)

            decision_symbol = {
                "APPROVED": "✅",
                "DECLINED": "❌",
                "PENDING_REVIEW": "👤",
            }.get(decision, "❓")
            logger.info(
                "[%s] Decision: %s %s — %s",
                app_id,
                decision_symbol,
                decision,
                reason,
            )

            return json.dumps(
                {
                    "applicant_id": app_id,
                    "decision": decision,
                    "action": action,
                    "reason": reason,
                    "score": score,
                    "compliant": compliant,
                    "flags": data.get("flags", []),
                    "reasoning": data.get("reasoning", ""),
                    "risk_factors": data.get("risk_factors", []),
                    "compensating_factors": data.get("compensating_factors", []),
                    "decided_at": datetime.now(timezone.utc).isoformat(),
                    "thresholds": {
                        "auto_approve": self._approve_threshold,
                        "auto_decline": self._decline_threshold,
                    },
                }
            )
