---
description: Implement a feature using role-separated agents with TDD handoff.
---

# Implement Feature

## Context

You are implementing a feature for the Loan Workbench notification preference system.

**Read these files before starting:**

- `docs/notification-preferences-plan.md` for the implementation plan from Lesson 04
- `specs/product-spec-notification-preferences.md` for functional requirements
- `specs/non-functional-requirements.md` for NFR constraints
- `docs/implementation-playbook.md` for coding conventions
- `docs/architecture.md` for system shape and rule placement

## Feature: {{feature_description}}

### Acceptance Criteria

{{acceptance_criteria}}

## Workflow

1. **@tester** writes failing tests that define the acceptance criteria.
2. **@implementer** writes the minimal production code to pass them.
3. **@reviewer** validates the changes against specs and NFRs.

### Step 1 — Test First

@tester: Write failing tests for the acceptance criteria above. Each test should
target one specific behavior. Include at least one test for the "obvious" happy
path AND one test for a non-obvious edge case (check the specs for false-positive
and hard-negative patterns). For human-readable error or reason text, write
durable assertions that normalize text and check stable semantic markers instead
of exact sentence casing or punctuation, unless the exact literal token is part
of the contract (for example, `LEGAL-218`). For business-rule rejection status
codes on the current notification write path, prefer preserving existing route
semantics, but if the implementation lands on an equivalent `400` or `422`
response, tests should assert the invariant from the payload rather than fail on
that status distinction alone.

### Step 2 — Implement

@implementer: Make the tests pass. Follow the rules in your agent definition.
Do not touch test files.

### Step 3 — Review

@reviewer: Review all changes against `specs/non-functional-requirements.md`.
Flag any NFR violations or missing edge cases.
