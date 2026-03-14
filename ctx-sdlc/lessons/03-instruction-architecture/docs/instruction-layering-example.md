# Lesson 03 — Instruction Layering Example

This document defines the concrete example used in Lesson 03.

## Objective

Show that layered instruction files improve both where GitHub Copilot CLI edits and how it structures the generated code.

The example should touch two scoped surfaces:

- `src/backend/src/rules/notification-channel-rules.ts`
- `src/backend/tests/unit/notification-channel-rules.test.ts`

## Expected Change Shape

The preferred implementation for this lesson is:

- create a new pure business-rule module for notification channel changes
- create matching unit tests that mirror the source path
- keep the change local to the rule and its tests

## Required Constraints

These constraints are part of the example and must be preserved by the generated code:

1. The rule module must stay pure: no Express imports, no database access, no audit writes, no queue usage.
2. The rule module must return structured results rather than a bare boolean.
3. California-specific restriction text must include `LEGAL-218` in both the rule metadata and the human-readable reason.
4. The module header comments must document one false positive and one hard negative scenario.
5. The tests must cover happy path, boundary case, false positive, and hard negative scenarios.
6. The tests must use explicit assertions rather than snapshots.
7. Do not modify `src/backend/src/models/types.ts` for this lesson.
8. Do not run shell commands during the assessment run.
9. Discover and reuse the existing mandatory-event source of truth instead of creating a new hardcoded mandatory-events list or helper.

## Concrete Scenario

For this lesson, the rule should validate notification channel changes for mandatory events.

The intended hard case is:

- on California loans, decline notifications must not end up with every channel disabled
- disabling SMS is acceptable when email remains enabled
- disabling the last enabled channel for a California decline notification should fail with a structured `LEGAL-218` reason

Good output usually introduces a function like `validateNotificationChannelChange(...)` with a narrow input shape and a structured result object.

The preferred implementation should reuse the discovered mandatory-event source of truth rather than introducing a second source of truth.

## What Good Output Looks Like

Good output will usually:

- add one rule file and one matching test file
- keep all business logic inside the rule module
- keep tests close to the instruction language: false positive, hard negative, and boundary cases should be visible in test names or comments
- avoid inventing services, repositories, or new global domain types
- avoid duplicating mandatory-event definitions inside the new rule module