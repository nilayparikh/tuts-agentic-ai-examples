"""
Shared loan application data structures and test fixtures.

Used by all framework lessons (08–14) — kept in ``_common/src/`` so
every lesson can import without code duplication.

Eight synthetic applicants cover the full validation spectrum:

  ┌──────────────────────┬──────────────────────────────────────┬─────────────────┐
  │ Applicant            │ Profile                              │ Expected        │
  ├──────────────────────┼──────────────────────────────────────┼─────────────────┤
  │ Alice Chen           │ CS=730, DTI=0.28, conventional       │ APPROVED        │
  │ Bob Kwan             │ CS=545, DTI=0.58, 4 dero marks       │ DECLINED        │
  │ Carol Martinez       │ CS=612, FHA, 1st-time, med collect.  │ NEEDS_REVIEW    │
  │ David Park           │ CS=780, VA, 0% down, vet             │ APPROVED        │
  │ Elena Volkov         │ CS=595, conv., 10m emp, high DTI     │ DECLINED        │
  │ Frank Osei           │ CS=655, FHA, borderline LTV          │ NEEDS_REVIEW    │
  │ Grace Tanaka         │ CS=710, jumbo, excellent reserves     │ APPROVED        │
  │ Hassan Ali           │ CS=560, FHA, low-CS bracket           │ NEEDS_REVIEW    │
  └──────────────────────┴──────────────────────────────────────┴─────────────────┘
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
    # ─────────────────────────────────────────────────────────────────────────
    # 1 — Alice Chen: textbook approve
    #     CS=730, DTI≈0.28, LTV=0.80, 48 months employed, conventional
    # ─────────────────────────────────────────────────────────────────────────
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
    # ─────────────────────────────────────────────────────────────────────────
    # 2 — Bob Kwan: textbook decline
    #     CS=545 (below floor), DTI≈0.58 (far over limit), 8m employed
    # ─────────────────────────────────────────────────────────────────────────
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
    # ─────────────────────────────────────────────────────────────────────────
    # 3 — Carol Martinez: genuine edge case requiring reasoning
    #
    #   Signal matrix (FHA loan, first-time buyer):
    #   HARD FAIL conventional: CS=612, LTV=0.965 (>0.95), emp=18m (<24)
    #   SOFT PASS under FHA:
    #     - FHA allows CS≥580 with 3.5% down (LTV ≤ 0.965)  ✓
    #     - FHA employment exception if stable field change with LOE ✓
    #   AMBIGUOUS:
    #     - DTI=0.41 (under 0.43 limit, but close — compensating factors)
    #     - 1 derog = medical collection, fully resolved (FHA exception)
    #     - FTHB DPA programme → effective DTI limit 0.44 ✓
    #   OUTCOME: NEEDS_REVIEW with conditions
    # ─────────────────────────────────────────────────────────────────────────
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
    # ─────────────────────────────────────────────────────────────────────────
    # 4 — David Park: VA loan, strong approve
    #     CS=780, DTI≈0.22, LTV=1.00 (0% down — VA benefit), 120m employed
    #     Test: VA max_ltv=1.00 allows 0% down; excellent credit negates
    #     any soft DTI concern; long employment is compensating factor.
    # ─────────────────────────────────────────────────────────────────────────
    LoanApplication(
        applicant_id="APP-2024-004",
        full_name="David Park",
        credit_score=780,
        annual_income_usd=110_000.0,
        monthly_debt_payments_usd=300.0,  # car lease only
        loan_amount=420_000.0,
        property_value=420_000.0,  # LTV = 1.00 (VA zero-down)
        employment_months=120,
        derogatory_marks=0,
        derogatory_mark_notes="",
        loan_type="va",
        first_time_homebuyer=False,
        has_letter_of_explanation=False,
        proposed_monthly_payment=1_700.0,
    ),
    # ─────────────────────────────────────────────────────────────────────────
    # 5 — Elena Volkov: multiple hard fails — decline
    #     CS=595 (below 620 conv floor), DTI≈0.52 (way over), emp=10m
    #     Conventional loan with no exceptions available.
    #     Test: stacks multiple fails; model must cite ALL of them.
    # ─────────────────────────────────────────────────────────────────────────
    LoanApplication(
        applicant_id="APP-2024-005",
        full_name="Elena Volkov",
        credit_score=595,
        annual_income_usd=54_000.0,
        monthly_debt_payments_usd=950.0,  # student loans + credit cards
        loan_amount=270_000.0,
        property_value=300_000.0,
        employment_months=10,
        derogatory_marks=2,
        derogatory_mark_notes=(
            "Two 30-day late payments on student loan (2024-Q1, 2024-Q2)."
        ),
        loan_type="conventional",
        first_time_homebuyer=False,
        has_letter_of_explanation=False,
        proposed_monthly_payment=1_500.0,
    ),
    # ─────────────────────────────────────────────────────────────────────────
    # 6 — Frank Osei: FHA borderline — needs review
    #     CS=655 (above FHA min), DTI≈0.42 (just under), LTV≈0.965,
    #     emp=24m (exactly on boundary), 1 derog (resolved utility dispute)
    #     Test: everything barely passes; model should flag conditions
    #     for the tight margins on multiple dimensions.
    # ─────────────────────────────────────────────────────────────────────────
    LoanApplication(
        applicant_id="APP-2024-006",
        full_name="Frank Osei",
        credit_score=655,
        annual_income_usd=72_000.0,
        monthly_debt_payments_usd=600.0,
        loan_amount=290_000.0,
        property_value=300_518.0,  # LTV ≈ 0.965
        employment_months=24,
        derogatory_marks=1,
        derogatory_mark_notes=(
            "Utility company billing dispute (resolved May 2023). "
            "Previously reported as collection, now removed from bureau."
        ),
        loan_type="fha",
        first_time_homebuyer=True,
        has_letter_of_explanation=True,
        proposed_monthly_payment=1_520.0,
    ),
    # ─────────────────────────────────────────────────────────────────────────
    # 7 — Grace Tanaka: strong approve, high income
    #     CS=710, DTI≈0.24, LTV=0.70, 60m employed, conv.
    #     Test: clean conventional with excellent reserves indicator
    #     (30% down payment). Model should note strong equity as
    #     compensating factor.
    # ─────────────────────────────────────────────────────────────────────────
    LoanApplication(
        applicant_id="APP-2024-007",
        full_name="Grace Tanaka",
        credit_score=710,
        annual_income_usd=145_000.0,
        monthly_debt_payments_usd=800.0,  # car + investment property
        loan_amount=490_000.0,
        property_value=700_000.0,  # LTV = 0.70
        employment_months=60,
        derogatory_marks=0,
        derogatory_mark_notes="",
        loan_type="conventional",
        first_time_homebuyer=False,
        has_letter_of_explanation=False,
        proposed_monthly_payment=2_100.0,
    ),
    # ─────────────────────────────────────────────────────────────────────────
    # 8 — Hassan Ali: FHA low-CS bracket — needs review
    #     CS=560 (500–579 bracket → max LTV 0.90, 10% down required)
    #     LTV=0.89 (passes low-CS bracket), DTI=0.38 (passes),
    #     emp=36m, 0 deros. The tricky part: model must recognise the
    #     lower CS bracket triggers stricter LTV rules even though
    #     the score is above the 500 minimum.
    # ─────────────────────────────────────────────────────────────────────────
    LoanApplication(
        applicant_id="APP-2024-008",
        full_name="Hassan Ali",
        credit_score=560,
        annual_income_usd=62_000.0,
        monthly_debt_payments_usd=350.0,  # personal loan
        loan_amount=222_500.0,
        property_value=250_000.0,  # LTV = 0.89
        employment_months=36,
        derogatory_marks=0,
        derogatory_mark_notes="",
        loan_type="fha",
        first_time_homebuyer=True,
        has_letter_of_explanation=False,
        proposed_monthly_payment=1_280.0,
    ),
]

APPLICANT_INDEX: dict[str, LoanApplication] = {a.applicant_id: a for a in APPLICANTS}
