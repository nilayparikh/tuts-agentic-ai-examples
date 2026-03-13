---
applyTo: "app/backend/tests/**"
---

# Testing Instructions

Rules for writing and maintaining Vitest test suites.

## Test Structure

- Test files mirror source paths: `app/backend/src/rules/state-machine.ts` → `app/backend/tests/unit/state-machine.test.ts`.
- Use `describe()` blocks to group related scenarios.
- Each test should have a clear intent documented in its name.
- Annotate edge-case tests with comments explaining WHY the case matters.

## Business Rule Tests

- Test rules through their public function APIs — do NOT mock rule internals.
- Every rule function must have tests for:
  - Happy path (allowed/valid)
  - Boundary case (exactly at the threshold)
  - False positive (looks wrong, is actually correct)
  - Hard negative (looks correct, is actually forbidden)
- Use inline comments to label which category each test covers.

## Anti-Patterns — Do Not Generate

- Do not mock the in-memory store for unit tests — seed it with test data instead.
- Do not use `any` type assertions in tests.
- Do not write tests that depend on execution order.
- Do not use snapshots for business rule validations — use explicit assertions.

## Naming Convention

- Describe behavior in test names: `"blocks SMS for decline events on California loans"`.
- Avoid: `"test state rules"`, `"should work"`, `"handles edge case"`.

## Coverage Expectations

- All business rules in `app/backend/src/rules/` must have > 90% branch coverage.
- Service-level tests should cover the audit fail-closed path.
- Route-level tests are integration tests — they can be thinner.
