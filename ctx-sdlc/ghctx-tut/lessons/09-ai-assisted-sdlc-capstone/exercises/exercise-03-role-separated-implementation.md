# Exercise 3 — Role-Separated Implementation

> **Lessons Applied:** L05 (Implementation Workflows) + L07 (Surface Strategy)
> **Estimated Time:** 45–60 minutes
> **Difficulty:** Intermediate

## Objective

Create two custom agent files with enforced role boundaries — a planner and a
tester — then use them with TDD to implement an audit-trail enhancement for
notification preference changes.

## Background

In Lesson 5 you learned that a single agent doing everything leads to drift.
It plans loosely, tests as an afterthought, and writes code that doesn't match
the codebase patterns. Role separation fixes this.

Three roles, three boundaries:

| Role        | Can Do                        | Cannot Do                      |
| ----------- | ----------------------------- | ------------------------------ |
| Planner     | Read files, output spec       | Write code                     |
| Tester      | Read spec, write tests        | Read or modify production code |
| Implementer | Read spec + tests, write code | Modify test expectations       |

The flow: planner produces a spec → tester writes tests from the spec →
implementer writes code to pass the tests.

## Tasks

### Task 1: Create the Planner Agent

Create `.github/agents/planner.agent.md`:

````markdown
---
name: planner
description: "Read-only planning agent — produces implementation specs"
---

# Planner Agent

You are a read-only planning agent. Your job is to analyze the codebase and
produce a detailed implementation specification.

## Rules

1. You MUST read the architecture doc and relevant instruction files first.
2. You MUST discover affected source files by searching — do not assume paths.
3. You MUST output a structured specification document — NEVER code.
4. Your spec must include:
   - Files to create (with purpose and location rationale)
   - Files to modify (with specific change descriptions in words)
   - Test requirements (what to test, expected behavior)
   - Relevant patterns discovered from the codebase
5. If a file you need doesn't exist, describe what it should contain — don't create it.

## Output Format

```markdown
# Implementation Spec: [Feature Name]

## Discovery Summary

[List every file you read and what you learned from it]

## Affected Surfaces

[Backend routes, rules, services, models, frontend pages]

## Implementation Steps

[Ordered steps in natural language — no code]

## Test Requirements

[What to test, expected inputs and outputs, edge cases]

## Risks

[What could go wrong, open questions]
```
````

````

### Task 2: Create the Tester Agent

Create `.github/agents/tester.agent.md`:

```markdown
---
name: tester
description: "Test-first agent — writes tests from implementation specs"
---

# Tester Agent

You are a test-first agent. You write test files from implementation
specifications. You do NOT read or modify production source code.

## Rules

1. You receive an implementation spec as input — not source code.
2. You write test files using Vitest (`describe`, `it`, `expect`).
3. You MUST NOT read files under `backend/src/` — only `backend/tests/`.
4. You MUST NOT write production code — only test code.
5. Import the module under test by path — the implementation doesn't exist yet.
6. Follow the existing test conventions discovered from `backend/tests/unit/`.

## Output

A complete test file ready to run. Tests will fail initially — that's correct.
The implementer makes them pass.
````

### Task 3: Run the TDD Flow — Audit Trail Enhancement

**Feature:** Every notification preference change must produce an audit trail
entry recording who changed what, when, and why.

**Step 1 — Plan** (using planner agent):

Ask the planner to create a spec for the audit trail enhancement. It should
discover:

- The audit service pattern in `backend/src/services/audit-service.ts`
- The preference write route in `backend/src/routes/notifications.ts`
- The existing audit conventions from the architecture doc
- The `NotificationPreference` type shape

Verify the spec is code-free and references actual files.

**Step 2 — Test** (using tester agent):

Give the tester the planner's spec. It should write a test file at
`backend/tests/unit/preference-audit.test.ts` that covers:

- [ ] Preference creation produces an audit entry
- [ ] Preference update (enable → disable) produces an audit entry with both values
- [ ] Audit entry includes actor ID, timestamp, and event details
- [ ] Audit entry includes the preference's event and channel
- [ ] Delegated sessions are not allowed to write (caught before audit)

The tests should fail when first run — the implementation doesn't exist yet.

**Step 3 — Implement** (you or a third agent):

Write the production code to make all tests pass. The implementation should:

- Wire audit calls into the preference write route
- Follow the fail-closed audit pattern (audit must succeed before persistence)
- Use the existing `auditAction` function signature

### Task 4: Verify Role Boundaries

Review the session for boundary violations:

- [ ] Did the planner produce any code? (Should be no)
- [ ] Did the tester read any production source files? (Should be no)
- [ ] Did the implementer change any test expectations? (Should be no)
- [ ] Do all tests pass after implementation?

## Success Criteria

1. `.github/agents/planner.agent.md` and `.github/agents/tester.agent.md` exist
2. The planner produced a code-free implementation spec
3. The tester produced a test file without reading production code
4. The implementation passes all tests
5. The audit trail captures all required fields
6. Each role stayed within its boundary throughout the flow

## Hints

- Look at `backend/tests/unit/business-rules.test.ts` for test file conventions
- The audit service uses `auditAction({ action, actor, target, details })` —
  the tester should know the signature from the spec, not from reading the source
- The preference route already calls `auditAction` for some operations — the
  implementation extends this pattern
- If an agent breaks its boundary, add stronger constraints to the agent file
  and re-run

## What You're Practicing

- **L05 pattern:** Role-separated agents with enforced boundaries
- **L07 pattern:** Context portability — agent files work across Copilot surfaces
- **Core skill:** TDD with AI agents, where plan → test → implement is the workflow
