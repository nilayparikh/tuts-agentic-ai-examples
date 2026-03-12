# Implementation Playbook

This document defines role boundaries, coding conventions, and handoff protocols
for the Loan Workbench implementation workflow.

## Role Boundaries

| Role        | Can Read                | Can Write                           | Can Execute            |
| ----------- | ----------------------- | ----------------------------------- | ---------------------- |
| Implementer | All source, specs, docs | `backend/src/**`, `frontend/src/**` | Terminal (build, lint) |
| Tester      | All source, specs, docs | `backend/tests/**` only             | Terminal + test runner |
| Reviewer    | All source, specs, docs | Nothing                             | Nothing                |

### Why These Boundaries Exist

- **Implementer cannot run tests**: Forces explicit handoff to the tester.
  Prevents "I'll just fix the test to match my code" shortcuts.
- **Reviewer cannot write**: Maintains independence. A reviewer who can "just
  fix it" is no longer reviewing — they're co-implementing.
- **Tester owns the test runner**: Only the tester decides when tests pass.
  The implementer provides code; the tester validates it.

## Coding Conventions

### Route Handlers (`backend/src/routes/`)

1. Extract business logic to `backend/src/rules/` or `backend/src/services/` — routes should
   orchestrate, not decide.
2. Use `requireRole()` middleware for role checks.
3. Use `blockDelegatedWrites` middleware for mutation endpoints.
4. Audit events via the queue broker or direct DB write before persisting changes.

### Business Rules (`backend/src/rules/`)

1. Pure functions that take data and return decisions.
2. No side effects (no I/O, no audit writes, no HTTP responses).
3. Document the legal or business source in a comment (e.g., `// LEGAL-218`).
4. Annotate edge cases with `// FALSE POSITIVE` or `// HARD NEGATIVE`.

### Services (`backend/src/services/`)

1. Handle I/O and external integrations.
2. Fail-closed for security-critical operations (audit).
3. Degrade gracefully for non-critical operations (notification delivery).
4. Never modify stored user preferences as a side effect of delivery.

### Middleware (`backend/src/middleware/`)

1. Thin and composable — one concern per middleware.
2. Auth middleware sets `req.session`, nothing else.
3. Guard middleware (like `blockDelegatedWrites`) returns 403 on violation.
4. Error handler masks internal details — no stack traces in production.

### Tests (`backend/tests/`)

1. Use `describe`/`it` with behavior-focused names.
2. One assertion per `it()` block.
3. Test through route handlers using supertest-style requests.
4. Annotate false-positive and hard-negative tests with comments.
5. Do not mock business rule functions — test them through real call paths.

## Handoff Protocols

### Tester → Implementer

```
Failing tests:
  - test name: "expected behavior description"
  - file: backend/tests/unit/xxx.test.ts

Files that need changes:
  - backend/src/rules/xxx.ts — add/modify rule
  - backend/src/routes/xxx.ts — wire in rule check

Relevant specs:
  - NFR-X: requirement summary
  - FR-X: functional requirement
```

### Implementer → Reviewer

```
Changed files:
  - backend/src/rules/xxx.ts — what changed
  - backend/src/routes/xxx.ts — what changed

Tests that should pass:
  - "test name" in backend/tests/unit/xxx.test.ts

NFRs touched:
  - NFR-X: how it's addressed
```

### Reviewer → Team

```
Review Summary:
  Verdict: APPROVE | REQUEST_CHANGES
  Files: list
  Issues: count

Issues (if any):
  1. [SEVERITY] description — file — spec reference
```

## Anti-Patterns

| Anti-Pattern               | Why It's Wrong                                   | Correct Approach                  |
| -------------------------- | ------------------------------------------------ | --------------------------------- |
| One agent does everything  | No independent validation                        | Three-agent role separation       |
| Implementer runs own tests | "Tests pass" because they were adjusted to match | Tester owns execution             |
| Reviewer pushes fixes      | No independent review trail                      | Reviewer flags, implementer fixes |
| Skipping the red step      | No proof the test catches the defect             | Always start with a failing test  |
| Batching unrelated changes | Review scope explosion                           | One feature per TDD cycle         |
