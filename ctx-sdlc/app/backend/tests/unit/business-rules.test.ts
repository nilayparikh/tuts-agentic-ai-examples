// ---------------------------------------------------------------------------
// Business Rules Tests
// ---------------------------------------------------------------------------

import { describe, it, expect } from "vitest";
import {
  validateLoanRules,
  requiredApprovalRoles,
  canApprove,
} from "../../src/rules/business-rules.js";
import type { LoanApplication } from "../../src/models/types.js";

const baseLoan: LoanApplication = {
  id: "test-1",
  borrowerName: "Test Corp",
  amount: 100000,
  loanState: "NY",
  status: "intake",
  assignedUnderwriter: "u-1",
  riskScore: null,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

describe("Business Rules", () => {
  it("passes for a valid standard loan", () => {
    expect(validateLoanRules(baseLoan)).toEqual([]);
  });

  it("rejects zero amount", () => {
    const violations = validateLoanRules({ ...baseLoan, amount: 0 });
    expect(violations).toHaveLength(1);
    expect(violations[0].rule).toBe("positive-amount");
  });

  it("rejects California loan below minimum", () => {
    const violations = validateLoanRules({
      ...baseLoan,
      loanState: "CA",
      amount: 10000,
    });
    expect(violations.some((v) => v.rule === "ca-min-amount")).toBe(true);
  });

  it("rejects California loan above maximum", () => {
    const violations = validateLoanRules({
      ...baseLoan,
      loanState: "CA",
      amount: 6_000_000,
    });
    expect(violations.some((v) => v.rule === "ca-max-amount")).toBe(true);
  });
});

describe("Approval Roles", () => {
  it("underwriter can approve loans up to $1M", () => {
    expect(canApprove("underwriter", 500000)).toBe(true);
  });

  it("underwriter cannot approve loans over $1M", () => {
    expect(canApprove("underwriter", 1_500_000)).toBe(false);
  });

  it("analyst-manager required for loans over $1M", () => {
    expect(requiredApprovalRoles(1_500_000)).toContain("analyst-manager");
  });

  it("compliance-reviewer required for loans over $2.5M", () => {
    expect(requiredApprovalRoles(3_000_000)).toContain("compliance-reviewer");
  });
});
