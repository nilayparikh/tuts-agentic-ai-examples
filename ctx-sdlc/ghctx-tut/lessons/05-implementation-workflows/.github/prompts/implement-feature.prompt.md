---
description: Implement a feature using role-separated agents with TDD handoff.
---

# Implement Feature

## Context

You are implementing a feature for the Loan Workbench notification preference system.

**Read these files before starting:**

- `specs/product-spec-notification-preferences.md` for functional requirements
- `specs/non-functional-requirements.md` for NFR constraints
- `docs/implementation-playbook.md` for coding conventions

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
and hard-negative patterns).

### Step 2 — Implement

@implementer: Make the tests pass. Follow the rules in your agent definition.
Do not touch test files.

### Step 3 — Review

@reviewer: Review all changes against `specs/non-functional-requirements.md`.
Flag any NFR violations or missing edge cases.
