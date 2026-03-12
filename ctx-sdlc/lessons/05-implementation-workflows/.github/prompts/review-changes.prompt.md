---
mode: agent
description: Review recent code changes against specs and NFRs.
---

# Review Changes

## Context

Review the most recent code changes in this workspace.

**Read these files before reviewing:**

- `specs/non-functional-requirements.md` — NFR compliance checklist
- `specs/product-spec-notification-preferences.md` — functional requirements
- `docs/implementation-playbook.md` — coding conventions

## Review Scope

Examine all files modified since the last known-good state. For each change:

1. **Correctness**: Does it satisfy the requirement? Are edge cases covered?
2. **NFR compliance**: Walk through NFR-1 to NFR-7 and flag violations.
3. **Business rules**: Are California SMS, mandatory events, role defaults, and
   delegated session rules respected?
4. **Security**: Audit-first pattern, error message safety, role scoping.

## False-Positive and Hard-Negative Check

Specifically look for:

- **False positives**: Cases where the code blocks something it should allow
  (e.g., California SMS restriction applied to non-decline events).
- **Hard negatives**: Cases where the code allows something it should block
  (e.g., delegated session bypassing write restrictions due to missing check).

Reference the `FALSE POSITIVE` and `HARD NEGATIVE` annotations in the specs
to identify patterns the implementation might have missed.

## Output

Use the reviewer agent's output format:

- Review Summary with verdict
- Issues Found with severity, location, and spec reference
- Observations for non-blocking notes
