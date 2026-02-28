"""
Lesson 08 — Loan Application data structures and test fixtures.

Three synthetic applicants deliberately cover the full validation spectrum:
  - Alice Chen   → clean approve
  - Bob Kwan     → clear decline
  - Carol Martinez → edge case requiring reasoning (FHA exceptions, first-time
                     buyer programme, resolved medical collection)
"""

from __future__ import annotations

from dataclasses import dataclass


# ─── Data Model ──────────────────────────────────────────────────────────────


@dataclass
class LoanApplication:  # pylint: disable=too-many-instance-attributes
    """Structured loan application submitted for pre-screening."""

    applicant_id: str
    full_name: str
    credit_score: int
    annual_income_usd: float
    monthly_debt_payments_usd: float  # existing debt (excl. proposed payment)
    loan_amount: float
    property_value: float
    employment_months: int
    derogatory_marks: int
    derogatory_mark_notes: str  # free-text explanation
    loan_type: str  # "conventional" | "fha" | "va"
    first_time_homebuyer: bool
    has_letter_of_explanation: bool  # for any non-standard items
    proposed_monthly_payment: float  # principal + interest of new loan

    @property
    def monthly_income(self) -> float:
        """Gross monthly income."""
        return self.annual_income_usd / 12.0

    @property
    def dti_ratio(self) -> float:
        """Front-and-back debt-to-income ratio (with proposed payment)."""
        return (
            self.monthly_debt_payments_usd + self.proposed_monthly_payment
        ) / self.monthly_income

    @property
    def ltv_ratio(self) -> float:
        """Loan-to-value ratio."""
        return self.loan_amount / self.property_value

    def to_dict(self) -> dict:
        """Return a plain dict representation for JSON serialisation."""
        return {
            "applicant_id": self.applicant_id,
            "full_name": self.full_name,
            "credit_score": self.credit_score,
            "annual_income_usd": self.annual_income_usd,
            "monthly_debt_payments_usd": self.monthly_debt_payments_usd,
            "loan_amount": self.loan_amount,
            "property_value": self.property_value,
            "employment_months": self.employment_months,
            "derogatory_marks": self.derogatory_marks,
            "derogatory_mark_notes": self.derogatory_mark_notes,
            "loan_type": self.loan_type,
            "first_time_homebuyer": self.first_time_homebuyer,
            "has_letter_of_explanation": self.has_letter_of_explanation,
            "proposed_monthly_payment": self.proposed_monthly_payment,
            "computed": {
                "monthly_income": round(self.monthly_income, 2),
                "dti_ratio": round(self.dti_ratio, 4),
                "ltv_ratio": round(self.ltv_ratio, 4),
            },
        }


# ─── Test Fixtures ────────────────────────────────────────────────────────────

APPLICANTS: list[LoanApplication] = [
    # -------------------------------------------------------------------------
    # 1 — Alice Chen: textbook approve
    #     CS=730, DTI=0.28, LTV=0.80, 48 months employed
    # -------------------------------------------------------------------------
    LoanApplication(
        applicant_id="APP-2024-001",
        full_name="Alice Chen",
        credit_score=730,
        annual_income_usd=95_000.0,
        monthly_debt_payments_usd=420.0,  # car + student loan
        loan_amount=380_000.0,
        property_value=475_000.0,
        employment_months=48,
        derogatory_marks=0,
        derogatory_mark_notes="",
        loan_type="conventional",
        first_time_homebuyer=False,
        has_letter_of_explanation=False,
        proposed_monthly_payment=1_800.0,
    ),
    # -------------------------------------------------------------------------
    # 2 — Bob Kwan: textbook decline
    #     CS=545 (below floor), DTI=0.58 (far over limit), 8 months employed
    # -------------------------------------------------------------------------
    LoanApplication(
        applicant_id="APP-2024-002",
        full_name="Bob Kwan",
        credit_score=545,
        annual_income_usd=42_000.0,
        monthly_debt_payments_usd=1_100.0,  # credit cards + personal loan
        loan_amount=310_000.0,
        property_value=340_000.0,
        employment_months=8,
        derogatory_marks=4,
        derogatory_mark_notes=(
            "Late payments on two credit cards (2023), "
            "one collection (medical, unresolved), one judgement."
        ),
        loan_type="conventional",
        first_time_homebuyer=True,
        has_letter_of_explanation=False,
        proposed_monthly_payment=1_700.0,
    ),
    # -------------------------------------------------------------------------
    # 3 — Carol Martinez: genuine edge case requiring reasoning
    #
    #   Signal matrix (FHA loan, first-time buyer):
    #   HARD FAIL conventional: CS=612, LTV=0.965 (>0.95), emp=18m (<24)
    #   SOFT PASS under FHA:
    #     - FHA allows CS≥580 with 3.5% down (LTV ≤ 0.965)  ✓
    #     - FHA employment exception if stable field change with LOE ✓
    #   AMBIGUOUS:
    #     - DTI=0.41 (under 0.43 limit, but close — compensating factors needed)
    #     - 1 derogatory mark = medical collection, fully resolved 2022 ✓ (FHA exception)
    #     - First-time homebuyer down-payment assistance program
    #       qualifies for additional 1% DTI allowance → effective limit 0.44 ✓
    #   OUTCOME:  NEEDS_REVIEW with conditions (not auto-approve)
    #     underwriter must verify: (a) LOE on employment gap, (b) medical
    #     collection discharge letter, (c) DPA programme confirmation
    # -------------------------------------------------------------------------
    LoanApplication(
        applicant_id="APP-2024-003",
        full_name="Carol Martinez",
        credit_score=612,
        annual_income_usd=68_000.0,
        monthly_debt_payments_usd=520.0,  # one car loan
        loan_amount=255_000.0,
        property_value=264_250.0,  # LTV ≈ 0.965 (FHA 3.5% down)
        employment_months=18,
        derogatory_marks=1,
        derogatory_mark_notes=(
            "One medical collection ($1,800 dental surgery, Sep 2021) "
            "fully paid/discharged Jun 2022.  No other derogatory history."
        ),
        loan_type="fha",
        first_time_homebuyer=True,
        has_letter_of_explanation=True,
        proposed_monthly_payment=1_420.0,
    ),
]

APPLICANT_INDEX: dict[str, LoanApplication] = {a.applicant_id: a for a in APPLICANTS}
