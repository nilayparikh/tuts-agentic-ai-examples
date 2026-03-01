"""
ComplianceAgent — Check regulatory compliance for loan applications.

Validates loan applications against FHA, VA, and conventional lending
regulations. Flags non-compliant aspects and notes applicable exceptions.
"""

from __future__ import annotations

import json
import logging

from telemetry import tracer

logger = logging.getLogger("compliance_agent")

# ── Compliance rule sets per loan type ────────────────────────────────────────

_COMPLIANCE_RULES = {
    "conventional": {
        "min_credit_score": 620,
        "max_ltv": 0.95,
        "pmi_required_above_ltv": 0.80,
        "max_dti_qualified": 0.43,
        "min_down_payment_pct": 0.05,
    },
    "fha": {
        "min_credit_score_3_5_down": 580,
        "min_credit_score_10_down": 500,
        "max_ltv_high_cs": 0.965,
        "max_ltv_low_cs": 0.90,
        "max_dti_qualified": 0.43,
        "dpa_dti_allowance": 0.01,
        "medical_collection_exception": True,
        "upfront_mip_pct": 1.75,
    },
    "va": {
        "min_credit_score": 580,
        "max_ltv": 1.00,
        "max_dti_qualified": 0.41,
        "funding_fee_first_use_pct": 2.15,
        "no_pmi_required": True,
    },
}


class ComplianceAgent:
    """Check regulatory compliance for loan applications."""

    async def check(self, application_json: str) -> str:
        """Run compliance checks and return results as JSON.

        Returns JSON with ``compliant`` boolean, list of ``flags``,
        applicable ``exceptions``, and any ``conditions``.
        """
        with tracer.start_as_current_span("check_compliance") as span:
            app = json.loads(application_json)
            app_id = app.get("applicant_id", "unknown")
            loan_type = app.get("loan_type", "conventional")
            span.set_attribute("applicant_id", app_id)
            span.set_attribute("loan_type", loan_type)

            logger.info(
                "[%s] ── Compliance Check Started ────────────────────",
                app_id,
            )
            logger.info(
                "[%s] Loan type: %s | Credit: %s | DTI: %s | LTV: %s",
                app_id,
                loan_type.upper(),
                app.get("credit_score"),
                app.get("dti_ratio"),
                app.get("ltv_ratio"),
            )

            flags: list[dict] = []
            exceptions: list[str] = []
            conditions: list[str] = []

            if loan_type == "fha":
                self._check_fha(app, flags, exceptions, conditions)
            elif loan_type == "va":
                self._check_va(app, flags, exceptions, conditions)
            else:
                self._check_conventional(app, flags, exceptions, conditions)

            # An application is non-compliant only if there are hard flags
            hard_flags = [f for f in flags if f["severity"] == "hard"]
            compliant = len(hard_flags) == 0

            span.set_attribute("compliance.compliant", compliant)
            span.set_attribute("compliance.flag_count", len(flags))

            for flag in flags:
                log_fn = logger.warning if flag["severity"] == "hard" else logger.info
                log_fn(
                    "[%s]   FLAG [%s] %s: %s",
                    app_id,
                    flag["severity"].upper(),
                    flag["rule"],
                    flag["message"],
                )
            for exc in exceptions:
                logger.info("[%s]   EXCEPTION: %s", app_id, exc)
            for cond in conditions:
                logger.info("[%s]   CONDITION: %s", app_id, cond)

            status_str = "✅ COMPLIANT" if compliant else "❌ NON-COMPLIANT"
            logger.info(
                "[%s] Result: %s (%d flags, %d hard)",
                app_id,
                status_str,
                len(flags),
                len(hard_flags),
            )

            return json.dumps(
                {
                    "applicant_id": app_id,
                    "compliant": compliant,
                    "flags": flags,
                    "exceptions": exceptions,
                    "conditions": conditions,
                }
            )

    def _check_fha(
        self,
        app: dict,
        flags: list[dict],
        exceptions: list[str],
        conditions: list[str],
    ) -> None:
        """FHA-specific compliance checks."""
        with tracer.start_as_current_span("fha_rules"):
            rules = _COMPLIANCE_RULES["fha"]
            cs = app.get("credit_score", 0)
            ltv = app.get("ltv_ratio", 0)

            # Credit score vs LTV
            if cs >= 580:
                if ltv > rules["max_ltv_high_cs"]:
                    flags.append(
                        {
                            "rule": "fha_ltv_high_cs",
                            "severity": "hard",
                            "message": f"LTV {ltv:.1%} exceeds FHA max {rules['max_ltv_high_cs']:.1%} for CS≥580",
                        }
                    )
            elif cs >= 500:
                if ltv > rules["max_ltv_low_cs"]:
                    flags.append(
                        {
                            "rule": "fha_ltv_low_cs",
                            "severity": "hard",
                            "message": f"LTV {ltv:.1%} exceeds FHA max {rules['max_ltv_low_cs']:.1%} for CS 500-579",
                        }
                    )
            else:
                flags.append(
                    {
                        "rule": "fha_min_cs",
                        "severity": "hard",
                        "message": f"Credit score {cs} below FHA floor of 500",
                    }
                )

            # DTI check with DPA allowance
            dti = app.get("dti_ratio", 0)
            max_dti = rules["max_dti_qualified"]
            if app.get("first_time_homebuyer", False):
                max_dti += rules["dpa_dti_allowance"]
                exceptions.append("First-time homebuyer DPA: +1% DTI allowance")
            if dti > max_dti:
                flags.append(
                    {
                        "rule": "fha_dti",
                        "severity": "soft",
                        "message": f"DTI {dti:.1%} exceeds FHA max {max_dti:.1%}",
                    }
                )

            # Medical collection exception
            notes = app.get("derogatory_mark_notes", "").lower()
            if "medical" in notes and rules["medical_collection_exception"]:
                exceptions.append("FHA medical collection exception applies")

            conditions.append(f"Upfront MIP of {rules['upfront_mip_pct']}% required")

    def _check_va(
        self,
        app: dict,
        flags: list[dict],
        exceptions: list[str],
        conditions: list[str],
    ) -> None:
        """VA-specific compliance checks."""
        with tracer.start_as_current_span("va_rules"):
            rules = _COMPLIANCE_RULES["va"]
            cs = app.get("credit_score", 0)

            if cs < rules["min_credit_score"]:
                flags.append(
                    {
                        "rule": "va_min_cs",
                        "severity": "hard",
                        "message": f"Credit score {cs} below VA lender overlay of {rules['min_credit_score']}",
                    }
                )

            dti = app.get("dti_ratio", 0)
            if dti > rules["max_dti_qualified"]:
                flags.append(
                    {
                        "rule": "va_dti",
                        "severity": "soft",
                        "message": f"DTI {dti:.1%} exceeds VA max {rules['max_dti_qualified']:.1%}",
                    }
                )

            exceptions.append("VA: No PMI required")
            conditions.append(
                f"VA funding fee of {rules['funding_fee_first_use_pct']}% applies (first use)"
            )

    def _check_conventional(
        self,
        app: dict,
        flags: list[dict],
        exceptions: list[str],
        conditions: list[str],
    ) -> None:
        """Conventional loan compliance checks."""
        with tracer.start_as_current_span("conventional_rules"):
            rules = _COMPLIANCE_RULES["conventional"]
            cs = app.get("credit_score", 0)

            if cs < rules["min_credit_score"]:
                flags.append(
                    {
                        "rule": "conv_min_cs",
                        "severity": "hard",
                        "message": f"Credit score {cs} below conventional min of {rules['min_credit_score']}",
                    }
                )

            ltv = app.get("ltv_ratio", 0)
            if ltv > rules["max_ltv"]:
                flags.append(
                    {
                        "rule": "conv_ltv",
                        "severity": "hard",
                        "message": f"LTV {ltv:.1%} exceeds conventional max of {rules['max_ltv']:.1%}",
                    }
                )
            elif ltv > rules["pmi_required_above_ltv"]:
                conditions.append("PMI required (LTV > 80%)")

            dti = app.get("dti_ratio", 0)
            if dti > rules["max_dti_qualified"]:
                flags.append(
                    {
                        "rule": "conv_dti",
                        "severity": "soft",
                        "message": f"DTI {dti:.1%} exceeds conventional max of {rules['max_dti_qualified']:.1%}",
                    }
                )

            marks = app.get("derogatory_marks", 0)
            if marks > 2:
                flags.append(
                    {
                        "rule": "conv_derogatory",
                        "severity": "soft",
                        "message": f"{marks} derogatory marks exceeds conventional guideline of 2",
                    }
                )
