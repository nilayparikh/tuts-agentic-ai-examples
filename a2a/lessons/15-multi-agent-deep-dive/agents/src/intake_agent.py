"""
IntakeAgent — Validates and normalizes incoming loan applications.

First agent in the pipeline. Checks that all required fields are present,
values are within sane ranges, and normalizes the data for downstream agents.
"""

from __future__ import annotations

import json
import logging

from telemetry import tracer

logger = logging.getLogger("intake_agent")


class IntakeAgent:
    """Validate and normalize raw loan application data."""

    REQUIRED_FIELDS = [
        "applicant_id",
        "full_name",
        "credit_score",
        "annual_income_usd",
        "monthly_debt_payments_usd",
        "loan_amount",
        "property_value",
        "employment_months",
        "derogatory_marks",
        "loan_type",
        "proposed_monthly_payment",
    ]

    async def validate(self, application_json: str) -> str:
        """Validate a loan application and return normalized JSON.

        Returns JSON with ``valid`` boolean and either normalized data
        or a list of validation errors.
        """
        with tracer.start_as_current_span("intake_validate") as span:
            try:
                app = json.loads(application_json)
            except json.JSONDecodeError:
                span.set_attribute("intake.valid", False)
                logger.error("Invalid JSON received by IntakeAgent")
                return json.dumps({"valid": False, "errors": ["Invalid JSON"]})

            app_id = app.get("applicant_id", "unknown")
            span.set_attribute("applicant_id", app_id)
            logger.info(
                "[%s] ── Intake Validation Started ─────────────────────",
                app_id,
            )
            logger.info(
                "[%s] Applicant: %s | Loan: $%s | Type: %s",
                app_id,
                app.get("full_name", "N/A"),
                f"{app.get('loan_amount', 0):,.0f}",
                app.get("loan_type", "N/A"),
            )

            errors = self._check_required_fields(app)
            errors.extend(self._check_value_ranges(app))

            if errors:
                span.set_attribute("intake.valid", False)
                span.set_attribute("intake.error_count", len(errors))
                logger.warning(
                    "[%s] Validation FAILED — %d error(s): %s",
                    app_id,
                    len(errors),
                    errors,
                )
                return json.dumps(
                    {
                        "valid": False,
                        "applicant_id": app_id,
                        "errors": errors,
                    }
                )

            # Normalize: compute derived fields
            monthly_income = app["annual_income_usd"] / 12.0
            dti_ratio = (
                app["monthly_debt_payments_usd"] + app["proposed_monthly_payment"]
            ) / monthly_income
            ltv_ratio = app["loan_amount"] / app["property_value"]

            normalized = {
                **app,
                "monthly_income": round(monthly_income, 2),
                "dti_ratio": round(dti_ratio, 4),
                "ltv_ratio": round(ltv_ratio, 4),
            }

            span.set_attribute("intake.valid", True)
            span.set_attribute("intake.dti_ratio", normalized["dti_ratio"])
            span.set_attribute("intake.ltv_ratio", normalized["ltv_ratio"])

            logger.info(
                "[%s] Validation PASSED — DTI: %.4f | LTV: %.4f | Income/mo: $%,.2f",
                app_id,
                normalized["dti_ratio"],
                normalized["ltv_ratio"],
                normalized["monthly_income"],
            )

            return json.dumps({"valid": True, "application": normalized})

    def _check_required_fields(self, app: dict) -> list[str]:
        """Check all required fields are present and non-null."""
        missing = [f for f in self.REQUIRED_FIELDS if f not in app or app[f] is None]
        return [f"Missing required field: {f}" for f in missing]

    def _check_value_ranges(self, app: dict) -> list[str]:
        """Check values are within logical ranges."""
        errors: list[str] = []

        cs = app.get("credit_score", 0)
        if not 300 <= cs <= 850:
            errors.append(f"Credit score {cs} out of range [300, 850]")

        income = app.get("annual_income_usd", 0)
        if income <= 0:
            errors.append("Annual income must be positive")

        loan_amt = app.get("loan_amount", 0)
        if loan_amt <= 0:
            errors.append("Loan amount must be positive")

        prop_val = app.get("property_value", 0)
        if prop_val <= 0:
            errors.append("Property value must be positive")

        loan_type = app.get("loan_type", "")
        if loan_type not in ("conventional", "fha", "va"):
            errors.append(f"Unknown loan type: {loan_type}")

        return errors
