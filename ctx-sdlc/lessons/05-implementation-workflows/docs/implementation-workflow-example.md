# Lesson 05 — Implementation Workflow Example

This document defines the concrete example used in Lesson 05.

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

## Concrete Scenario

Harden notification preference writes so the existing route cannot:

- disable the last available channel for `manual-review-escalation`
- enable decline SMS for California loan context

Good output should keep the change local and avoid sprawling refactors.

It should also make the intentional scope boundary visible: this lesson is about hardening the current notification write path, not implementing every preference mutation surface in the repository at once.

## What Good Output Looks Like

Good output will usually:

- create a pure rule file and a matching unit test file
- wire the route to call the rule rather than embedding the full policy inline
- preserve existing delegated-session and permission checks
- cite or encode the false-positive case where escalation SMS is disabled but escalation email remains enabled
- encode the hard-negative case where all escalation channels end up disabled
- explain which test cases would fail before the production change and which should pass after it
