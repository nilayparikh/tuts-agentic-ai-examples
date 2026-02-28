"""
Shared business-rule validation tools for loan-validation agents.

Each public function is decorated with @tool so agent frameworks (Microsoft
Agent Framework, ADK, LangGraph, CrewAI, OpenAI Agents, etc.) can use it
during agent reasoning.

Rule sets
---------
Conventional loan
  min_credit_score        : 620
  max_dti                 : 0.43
  max_ltv                 : 0.95
  min_employment_months   : 24  (continuous at same employer or field)
  max_derogatory_marks    : 2

FHA loan
  min_credit_score        : 580  (3.5 % down); 500–579 (10 % down only)
  max_dti                 : 0.43 (+0.01 if first-time buyer w/ DPA programme)
  max_ltv                 : 0.965 if CS ≥ 580; 0.90 if CS 500–579
  min_employment_months   : 24  (LOE accepted for career change in same field)
  medical_collection_ok   : True  (if resolved/discharged, ignored by FHA)

VA loan
  min_credit_score        : 580  (lender overlay; VA itself has no floor)
  max_dti                 : 0.41  (residual income requirement applies)
  max_ltv                 : 1.00  (no down payment required)
  min_employment_months   : 24  (same rules as FHA)
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Annotated

from pydantic import Field

try:
    from agent_framework import tool  # type: ignore[import-not-found]

    _HAS_AF = True
except ImportError:  # pragma: no cover
    _HAS_AF = False

    def tool(fn=None, **_kw):  # type: ignore[misc,no-redef]
        """Stub when agent-framework is not installed."""
        return fn if fn is not None else lambda f: f


# ─── Rule lookup tables ───────────────────────────────────────────────────────

_RULES: dict[str, dict] = {
    "conventional": {
        "min_credit_score": 620,
        "max_dti": 0.43,
        "max_ltv": 0.95,
        "min_employment_months": 24,
        "max_derogatory_marks": 2,
        "medical_collection_exception": False,
        "dpa_dti_allowance": 0.0,
    },
    "fha": {
        "min_credit_score": 580,
        "min_credit_score_high_ltv": 580,
        "min_credit_score_low_ltv": 500,
        "max_dti": 0.43,
        "max_ltv_high_cs": 0.965,
        "max_ltv_low_cs": 0.90,
        "min_employment_months": 24,
        "max_derogatory_marks": 3,
        "medical_collection_exception": True,
        "dpa_dti_allowance": 0.01,  # first-time buyer DPA programme adds 1 %
        "loe_employment_exception": True,
    },
    "va": {
        "min_credit_score": 580,
        "max_dti": 0.41,
        "max_ltv": 1.00,
        "min_employment_months": 24,
        "max_derogatory_marks": 2,
        "medical_collection_exception": False,
        "dpa_dti_allowance": 0.0,
    },
}


# ─── Result dataclass ─────────────────────────────────────────────────────────


@dataclass
class RuleResult:
    """Outcome of a single rule evaluation."""

    rule_name: str
    passed: bool
    severity: str  # "hard_fail" | "soft_fail" | "info" | "exception_applied"
    actual: float | int | str
    threshold: float | int | str
    message: str

    def to_dict(self) -> dict:
        """Serialise to plain dict."""
        return {
            "rule": self.rule_name,
            "passed": self.passed,
            "severity": self.severity,
            "actual": self.actual,
            "threshold": self.threshold,
            "message": self.message,
        }


# ─── Tool functions ───────────────────────────────────────────────────────────


@tool
def run_hard_checks(  # pylint: disable=too-many-locals
    application_json: Annotated[
        str,
        Field(
            description=(
                "JSON string of the full LoanApplication.to_dict() output. "
                "Must include keys: credit_score, loan_type, computed.dti_ratio, "
                "computed.ltv_ratio, employment_months, derogatory_marks."
            )
        ),
    ],
) -> str:
    """Execute hard-fail business rules against a loan application.

    Hard fails are automatic disqualifiers that cannot be overridden by
    compensating factors.  Returns JSON list of RuleResult dicts.  Any result
    with passed=False is a hard disqualifier.
    """
    app = json.loads(application_json)
    loan_type = app.get("loan_type", "conventional")
    rules = _RULES.get(loan_type, _RULES["conventional"])
    results: list[dict] = []

    cs = app["credit_score"]
    dti = app["computed"]["dti_ratio"]
    ltv = app["computed"]["ltv_ratio"]
    emp = app["employment_months"]
    dero = app["derogatory_marks"]

    # ── Credit score ─────────────────────────────────────────────
    min_cs = rules["min_credit_score"]
    results.append(
        RuleResult(
            rule_name="credit_score",
            passed=cs >= min_cs,
            severity="hard_fail",
            actual=cs,
            threshold=min_cs,
            message=(
                f"Credit score {cs} meets minimum {min_cs}."
                if cs >= min_cs
                else f"Credit score {cs} is below minimum {min_cs} for {loan_type} loan."
            ),
        ).to_dict()
    )

    # ── DTI ratio ────────────────────────────────────────────────
    max_dti = rules["max_dti"]
    if app.get("first_time_homebuyer") and rules.get("dpa_dti_allowance", 0):
        max_dti += rules["dpa_dti_allowance"]
    dti_passed = dti <= max_dti
    results.append(
        RuleResult(
            rule_name="dti_ratio",
            passed=dti_passed,
            severity="hard_fail",
            actual=round(dti, 4),
            threshold=round(max_dti, 4),
            message=(
                f"DTI {dti:.1%} is within limit {max_dti:.1%}."
                if dti_passed
                else f"DTI {dti:.1%} exceeds limit {max_dti:.1%} for {loan_type} loan."
            ),
        ).to_dict()
    )

    # ── LTV ratio ────────────────────────────────────────────────
    if loan_type == "fha":
        max_ltv = (
            rules["max_ltv_high_cs"]
            if cs >= rules["min_credit_score_high_ltv"]
            else rules["max_ltv_low_cs"]
        )
    else:
        max_ltv = rules["max_ltv"]
    ltv_passed = ltv <= max_ltv
    results.append(
        RuleResult(
            rule_name="ltv_ratio",
            passed=ltv_passed,
            severity="hard_fail",
            actual=round(ltv, 4),
            threshold=round(max_ltv, 4),
            message=(
                f"LTV {ltv:.1%} is within limit {max_ltv:.1%}."
                if ltv_passed
                else f"LTV {ltv:.1%} exceeds limit {max_ltv:.1%} for {loan_type} (CS={cs})."
            ),
        ).to_dict()
    )

    # ── Employment ───────────────────────────────────────────────
    min_emp = rules["min_employment_months"]
    emp_passed = emp >= min_emp
    emp_exception = (
        not emp_passed
        and rules.get("loe_employment_exception")
        and app.get("has_letter_of_explanation")
    )
    results.append(
        RuleResult(
            rule_name="employment_history",
            passed=emp_passed or bool(emp_exception),
            severity=(
                "exception_applied"
                if emp_exception
                else ("hard_fail" if not emp_passed else "info")
            ),
            actual=emp,
            threshold=min_emp,
            message=(
                f"Employment {emp}m meets minimum {min_emp}m."
                if emp_passed
                else (
                    f"Employment {emp}m is below {min_emp}m, "
                    f"but LOE exception applies for {loan_type}."
                    if emp_exception
                    else (
                        f"Employment {emp}m is below minimum {min_emp}m. "
                        f"No LOE exception available."
                    )
                )
            ),
        ).to_dict()
    )

    # ── Derogatory marks ─────────────────────────────────────────
    max_dero = rules["max_derogatory_marks"]
    dero_notes = app.get("derogatory_mark_notes", "")
    medical_ok = rules.get("medical_collection_exception", False)
    # If medical exception applies and the note is only medical, effective count may be lower
    effective_dero = dero
    if (
        medical_ok
        and dero > 0
        and "medical" in dero_notes.lower()
        and "resolved" in dero_notes.lower()
    ):
        effective_dero = max(0, dero - 1)
    dero_passed = effective_dero <= max_dero
    results.append(
        RuleResult(
            rule_name="derogatory_marks",
            passed=dero_passed,
            severity=(
                "hard_fail"
                if not dero_passed
                else ("exception_applied" if effective_dero < dero else "info")
            ),
            actual=effective_dero,
            threshold=max_dero,
            message=(
                (
                    f"Effective derogatory count {effective_dero} "
                    f"(raw {dero}, medical collection "
                    f"excluded by FHA rule) "
                    f"is within limit {max_dero}."
                )
                if effective_dero < dero
                else (
                    f"Derogatory marks {dero} "
                    f"{'within' if dero_passed else 'exceeds'} "
                    f"limit {max_dero}."
                )
            ),
        ).to_dict()
    )

    return json.dumps(results, indent=2)


@tool
def run_soft_checks(
    application_json: Annotated[
        str,
        Field(description="JSON string of the full LoanApplication.to_dict() output."),
    ],
) -> str:
    """Execute soft advisory checks against a loan application.

    Soft checks highlight risk factors or compensating factors for underwriter
    review. They do not independently disqualify an application.
    Returns JSON list of RuleResult dicts.
    """
    app = json.loads(application_json)
    loan_type = app.get("loan_type", "conventional")
    results: list[dict] = []

    cs = app["credit_score"]
    _dti = app["computed"][
        "dti_ratio"
    ]  # extracted for completeness; not used in soft checks  # noqa: F841
    ltv = app["computed"]["ltv_ratio"]
    emp = app["employment_months"]
    income = app["annual_income_usd"]
    loan_amt = app["loan_amount"]

    # ── Credit score band ────────────────────────────────────────
    if cs >= 740:
        band, note = "excellent", "Qualifies for best-tier interest rates."
    elif cs >= 700:
        band, note = (
            "good",
            "Qualifies for competitive rates with minimal risk premium.",
        )
    elif cs >= 660:
        band, note = "fair", "Mid-tier rates; compensating factors recommended."
    elif cs >= 620:
        band, note = (
            "borderline",
            "Near-minimum for conventional; compensating factors required.",
        )
    else:
        band, note = (
            "subprime",
            "Below conventional floor; restrict to FHA/VA evaluation.",
        )
    results.append(
        RuleResult(
            rule_name="credit_score_band",
            passed=True,
            severity="info",
            actual=f"{cs} ({band})",
            threshold="credit band classification",
            message=note,
        ).to_dict()
    )

    # ── Income adequacy ──────────────────────────────────────────
    income_ratio = loan_amt / income  # debt-to-income (gross, simplified)
    results.append(
        RuleResult(
            rule_name="income_adequacy",
            passed=income_ratio <= 4.5,
            severity="soft_fail" if income_ratio > 4.5 else "info",
            actual=round(income_ratio, 2),
            threshold=4.5,
            message=(
                f"Loan-to-income ratio {income_ratio:.2f}× is "
                + (
                    "within advisory limit 4.5×."
                    if income_ratio <= 4.5
                    else "above advisory limit 4.5×; flag for review."
                )
            ),
        ).to_dict()
    )

    # ── Employment stability ─────────────────────────────────────
    results.append(
        RuleResult(
            rule_name="employment_stability",
            passed=emp >= 36,
            severity="info",
            actual=emp,
            threshold=36,
            message=(
                f"Long employment history ({emp}m) — positive compensating factor."
                if emp >= 36
                else f"Employment history {emp}m is adequate (≥24m) but not long (< 36m)."
            ),
        ).to_dict()
    )

    # ── First-time buyer programme eligibility ───────────────────
    if app.get("first_time_homebuyer"):
        dpa_eligible = loan_type in ("fha", "conventional") and income <= 120_000
        results.append(
            RuleResult(
                rule_name="dpa_programme_eligibility",
                passed=dpa_eligible,
                severity="info",
                actual=f"first_time_homebuyer=True, income=${income:,.0f}",
                threshold="eligibility: FHA/conventional + income ≤ $120k",
                message=(
                    "Eligible for Down Payment Assistance "
                    "programme — DTI limit +1% and grant "
                    "available."
                    if dpa_eligible
                    else (
                        "FTHB flag set but income or loan type "
                        "may not qualify for DPA programme; "
                        "verify."
                    )
                ),
            ).to_dict()
        )

    # ── Cash reserves (proxy via LTV) ────────────────────────────
    down_payment_pct = 1.0 - ltv
    results.append(
        RuleResult(
            rule_name="down_payment_adequacy",
            passed=down_payment_pct >= 0.05,
            severity="info" if down_payment_pct >= 0.10 else "soft_fail",
            actual=f"{down_payment_pct:.1%}",
            threshold="≥10% preferred",
            message=(
                f"Down payment {down_payment_pct:.1%} indicates"
                + (
                    " strong equity position."
                    if down_payment_pct >= 0.20
                    else (
                        " adequate equity."
                        if down_payment_pct >= 0.10
                        else " minimal equity — PMI will be required."
                    )
                )
            ),
        ).to_dict()
    )

    return json.dumps(results, indent=2)


@tool
def lookup_policy_notes(
    question: Annotated[
        str,
        Field(
            description="A specific policy question about loan underwriting rules or exceptions."
        ),
    ],
) -> str:
    """Look up policy guidance via the QAAgent running on port 10001.

    Falls back to a structured policy memo when the server is unavailable.
    Never raises — always returns a string answer.
    """
    import asyncio  # pylint: disable=import-outside-toplevel

    try:
        return asyncio.get_event_loop().run_until_complete(_query_qa_agent(question))
    except Exception:  # pylint: disable=broad-exception-caught
        # QAAgent not running — return canonical policy memo
        return _POLICY_MEMO.get(
            _best_match(question),
            (
                "Policy memo not available for that specific question.  "
                "Default rule: follow handbook section 4.3 (conventional) or "
                "HUD 4000.1 (FHA) for edge-case resolution."
            ),
        )


async def _query_qa_agent(question: str) -> str:
    """Send question to QAAgent on port 10001 via A2A SDK."""
    import httpx  # pylint: disable=import-outside-toplevel
    from uuid import uuid4  # pylint: disable=import-outside-toplevel
    from a2a.client import (  # pylint: disable=import-outside-toplevel
        A2ACardResolver,
        A2AClient,
    )
    from a2a.types import (  # pylint: disable=import-outside-toplevel
        MessageSendParams,
        SendMessageRequest,
    )

    async with httpx.AsyncClient(timeout=10.0) as hc:
        resolver = A2ACardResolver(httpx_client=hc, base_url="http://localhost:10001")
        card = await resolver.get_agent_card()
        client = A2AClient(httpx_client=hc, agent_card=card)
        req = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                **{  # type: ignore[arg-type]
                    "message": {
                        "role": "user",
                        "parts": [{"kind": "text", "text": question}],
                        "messageId": uuid4().hex,
                    }
                }
            ),
        )
        resp = await client.send_message(req)
        msg = resp.root.result  # type: ignore[union-attr]
        parts = [
            p.root.text  # type: ignore[union-attr]
            for p in msg.parts  # type: ignore[union-attr]
            if getattr(p.root, "kind", None) == "text"
        ]
        return "\n".join(parts) if parts else "(no text in QAAgent response)"


def _best_match(question: str) -> str:
    """Return the most relevant policy key for the given question text."""
    q = question.lower()
    if "medical" in q and "collection" in q:
        return "medical_collection"
    if "employment" in q and ("gap" in q or "history" in q or "month" in q):
        return "employment_exception"
    if "fha" in q and ("ltv" in q or "down" in q or "loan-to-value" in q):
        return "fha_ltv"
    if "first" in q and ("home" in q or "buyer" in q):
        return "first_time_buyer"
    return "general"


_POLICY_MEMO: dict[str, str] = {
    "medical_collection": (
        "FHA Policy (HUD 4000.1 §II.A.1.b.iii): Medical collections and charge-offs "
        "are excluded from derogatory mark counts.  A fully paid/discharged medical "
        "collection does NOT constitute a derogatory event for FHA purposes and must "
        "not be included in the adverse credit count.  Documentation: copy of "
        "discharge letter or zero-balance statement required."
    ),
    "employment_exception": (
        "FHA Employment History (HUD 4000.1 §II.A.1.b.ii): Two-year employment "
        "history is required but need not be continuous.  A gap less than 6 months "
        "is acceptable with a Letter of Explanation (LOE).  Career changes within "
        "the same field are accepted provided the borrower demonstrates increased "
        "earning potential.  The underwriter must verify the LOE is credible and "
        "consistent with the application narrative."
    ),
    "fha_ltv": (
        "FHA LTV limits: For credit scores ≥ 580, maximum LTV is 96.5% (3.5% down). "
        "For credit scores 500–579, maximum LTV is 90% (10% down).  Applying the "
        "correct LTV limit requires confirming the credit score bracket first."
    ),
    "first_time_buyer": (
        "FHA First-Time Homebuyer Down Payment Assistance (DPA) programmes: Many "
        "state HFAs offer DPA grants that can reduce the effective down payment "
        "requirement.  When a borrower uses a qualifying DPA programme, the effective "
        "DTI ceiling may be raised by 1 percentage point (to 44% under FHA) as a "
        "compensating factor.  Underwriter must confirm the DPA programme is on the "
        "approved HUD list."
    ),
    "general": (
        "General underwriting guidance: When in doubt, refer to the current "
        "Fannie Mae Selling Guide (conventional) or HUD 4000.1 (FHA).  Document "
        "all compensating factors explicitly in the loan file."
    ),
}
