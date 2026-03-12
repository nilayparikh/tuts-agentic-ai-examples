# TDD Workflow Skill

A structured test-driven development workflow for the Loan Workbench API.

## When to Use

Use this skill when implementing a new feature, fixing a bug, or adding a
business rule. It enforces the red→green→refactor cycle with explicit handoffs
between testing and implementation roles.

## Workflow Steps

### 1. Understand the Requirement

Read the relevant specification:

- `specs/product-spec-notification-preferences.md` for functional requirements
- `specs/non-functional-requirements.md` for NFR constraints
- The specific feature request or bug report

Identify:

- The happy-path behavior
- At least one edge case from the false-positive/hard-negative annotations
- Which files will need to change (route, rule, service, middleware)

### 2. Write Failing Tests (Red)

Create tests in `tests/` using Vitest:

```typescript
describe("feature-name", () => {
  it("happy path behavior", async () => {
    // Arrange: set up request with valid data
    // Act: call the endpoint
    // Assert: verify expected response
  });

  it("edge case — annotated pattern from specs", async () => {
    // FALSE POSITIVE or HARD NEGATIVE test
    // Arrange: set up the subtle scenario
    // Act: call the endpoint
    // Assert: verify the non-obvious correct behavior
  });
});
```

Run `npx vitest run` to confirm the tests fail for the right reason.

### 3. Implement (Green)

Hand off to the implementer with:

- Which tests are failing
- Which files need changes
- The relevant spec section

The implementer makes the minimal change to pass the tests.

### 4. Verify

Run `npx vitest run` again:

- If all tests pass → proceed to step 5.
- If tests fail → describe the failure and hand back to the implementer.

### 5. Review (Refactor)

Hand off to the reviewer with:

- The list of changed files
- The NFRs that apply

The reviewer checks for:

- NFR violations
- Missing edge cases
- Code convention compliance

### 6. Report

Summarize the TDD cycle:

- Tests added (count and descriptions)
- Files changed
- NFRs verified
- False-positive/hard-negative patterns covered

## Rules

- Never skip the failing-test step. If you cannot write a failing test, the
  requirement is not clear enough — ask for clarification.
- Tests must fail for the RIGHT reason (missing implementation, not syntax errors).
- The implementer must not modify test files.
- The reviewer must not modify any files.
- Each cycle targets ONE requirement or bug. Do not batch unrelated changes.
