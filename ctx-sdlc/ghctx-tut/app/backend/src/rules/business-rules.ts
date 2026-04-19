// ---------------------------------------------------------------------------
// Business Rules
// ---------------------------------------------------------------------------
// Domain-specific validation rules.  These are checked by services BEFORE
// persisting changes.
//
// CALIFORNIA RULES — REGULATORY REQUIREMENT:
//   Loans in California (loan_state = "CA") have additional requirements:
//   - Minimum loan amount: $50,000
//   - Maximum loan amount: $5,000,000
//   - Mandatory 3-day cooling-off period between "review" → "underwriting"
//   - Additional disclosure document required before finalization
//
//   These rules are gated behind the `californiaRules` feature flag.
//   When disabled, California loans follow standard rules.
//
// AMOUNT THRESHOLDS:
//   - Loans over $1,000,000 require analyst-manager approval (not just underwriter)
//   - Loans over $2,500,000 require compliance-reviewer sign-off
// ---------------------------------------------------------------------------

import { featureFlags } from "../config/feature-flags.js";
import type { LoanApplication, UserRole } from "../models/types.js";

export interface RuleViolation {
  rule: string;
  message: string;
}

/**
 * Validate a loan application against all business rules.
 * Returns an empty array if all rules pass.
 */
export function validateLoanRules(loan: LoanApplication): RuleViolation[] {
  const violations: RuleViolation[] = [];

  // Standard rules
  if (loan.amount <= 0) {
    violations.push({
      rule: "positive-amount",
      message: "Loan amount must be positive.",
    });
  }

  // California-specific rules
  if (featureFlags.californiaRules && loan.loanState === "CA") {
    if (loan.amount < 50_000) {
      violations.push({
        rule: "ca-min-amount",
        message: "California loans must be at least $50,000.",
      });
    }
    if (loan.amount > 5_000_000) {
      violations.push({
        rule: "ca-max-amount",
        message: "California loans cannot exceed $5,000,000.",
      });
    }
  }

  return violations;
}

/**
 * Determine which roles are required to approve a loan at the given amount.
 */
export function requiredApprovalRoles(amount: number): UserRole[] {
  if (amount > 2_500_000) {
    return ["analyst-manager", "compliance-reviewer"];
  }
  if (amount > 1_000_000) {
    return ["analyst-manager"];
  }
  return ["underwriter"];
}

/**
 * Check if a role is authorized to approve a loan of the given amount.
 */
export function canApprove(role: UserRole, amount: number): boolean {
  const required = requiredApprovalRoles(amount);
  return required.includes(role);
}
