# Lesson 05 — Implementation Workflow Example

This document defines the concrete example used in Lesson 05.

## Prerequisite Context

This lesson consumes `docs/notification-preferences-plan.md`, the structured
implementation plan produced by the Lesson 04 planning workflow. The plan maps
out all backend, frontend, audit, and observability surfaces for the full
notification-preferences feature. Lesson 05 implements only **one focused slice**
of that plan — hardening the notification-preference write path.

## Objective

Show that a constrained implementation workflow can make a focused production change with matching tests instead of attempting the entire notification-preferences feature at once.

## Expected Change Shape

The preferred output for this lesson is a small change set with:

1. One new pure rule module under `src/backend/src/rules/`
2. One matching unit test file under `src/backend/tests/unit/`
3. One targeted wiring change to `src/backend/src/routes/notifications.ts`
4. No edits to protected config or database files

## Required Constraints

1. The workflow must implement code, not only describe it.
2. The new rule must use explicit inputs and existing domain types instead of direct database access.
3. The change must preserve delegated-session and role guards already present in the route.
4. The implementation must cover a mandatory-event rule and the California `LEGAL-218` restriction.
5. The implementation must call out at least one false positive and one hard negative in the new rule module comments.
6. The run must not execute shell commands.
7. The run must not edit protected files such as feature flags, schema, or seed data.
8. The run must not use SQL or task/todo write tools.
9. The final handoff should explain the expected red/green test behavior and name any deferred follow-up surfaces that remain intentionally out of scope.
10. The workflow should discover the current notification-preference write surfaces before editing and make the chosen slice boundary explicit.
11. The write path must keep `loanState` as the direct request input for this route. Do not replace it with a new `loanId` lookup contract.
12. The lesson is not complete until `python util.py --test` passes after the demo or manual implementation.

## Concrete Scenario

Harden notification preference writes so the existing route cannot:

- disable the last available channel for `manual-review-escalation`
- enable decline SMS for California loan context

Good output should keep the change local and avoid sprawling refactors.

It should also make the intentional scope boundary visible: this lesson is about hardening the current notification write path, not implementing every preference mutation surface in the repository at once.

Good output should explicitly name the deferred write surfaces in the handoff instead of silently implying that the whole notification-preferences domain is now complete.

## What Good Output Looks Like

Good output will usually:

- create a pure rule file and a matching unit test file
- wire the route to call the rule rather than embedding the full policy inline
- preserve existing delegated-session and permission checks
- keep the route contract direct and explicit by passing `loanState` into the rule instead of adding loan repository lookups
- cite or encode the false-positive case where escalation SMS is disabled but escalation email remains enabled
- encode the hard-negative case where all escalation channels end up disabled
- explain which test cases would fail before the production change and which should pass after it
- survive the end-to-end `python util.py --test` gate after the code change is produced

## Test Authoring Quality Bar

Generated tests must be durable across semantically equivalent implementations.
That matters in this lesson because `python util.py --demo` recreates `src/` from
the app baseline before each run, so any test fix that lives only in generated
source will be lost on the next demo.

When a rule returns a human-readable reason string:

- assert the invariant, not one exact sentence or capitalization pattern
- normalize text before matching, such as lowercasing the reason
- prefer checking stable business terms like `manual-review-escalation`,
  `at least one`, or `LEGAL-218`
- avoid brittle exact-string checks for explanatory prose unless the exact text
  is part of the contract

For this lesson, the mandatory-event tests should prove that the rejection
mentions the escalation invariant and the "at least one channel" rule, even if
the final sentence shape differs.

The `LEGAL-218` checks may assert the literal token `LEGAL-218`, because that
identifier is a stable contract signal rather than free-form wording.

When the current route rejects a business-rule violation, stable semantics matter
more than one exact HTTP code. In this lesson, a semantically equivalent
implementation may surface the rejection as `400` or `422` while still returning
the correct business explanation. Unless the lesson is explicitly about HTTP
status design, tests should accept either status for these rule rejections and
assert the business invariant from the payload.

If the implementation can preserve the route's existing rejection style without
extra complexity, prefer `400` for this lesson so the API remains aligned with
the rest of the simple validation surfaces.
