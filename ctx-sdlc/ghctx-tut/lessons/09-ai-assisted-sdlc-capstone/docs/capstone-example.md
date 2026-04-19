# Lesson 09 — Capstone Example

This document defines the concrete example used in Lesson 09.

## Objective

Show that a discovery-first capstone workflow can synthesize project-wide, backend-scoped, and frontend-scoped context into a cross-stack implementation slice — producing assessable code changes.

## Expected Output Shape

The demo must produce file changes:

1. Added: `backend/src/rules/preference-event-channel-validator.ts` — pure validation rule module
2. Added: `backend/tests/unit/preference-event-channel-validator.test.ts` — matching unit tests
3. Modified: `backend/src/routes/notifications.ts` — wired validator import

## Expected Change Artifacts

Assessment compares the actual `demo.patch` and `changed-files.json` against:

- `.output/change/expected-files.json` — expected added/modified/deleted files
- `.output/change/expected-patterns.json` — regex patterns that must appear in the patch

## Required Constraints

1. The validator must enforce that mandatory events cannot have all channels disabled.
2. The validator must respect LEGAL-218 California SMS restrictions from existing rules.
3. Unit tests must cover valid combinations, mandatory-event violations, and LEGAL-218 false positive and hard negative cases.
4. The validator must be wired into the existing notification preference write route.
5. The implementation must follow repository conventions discovered from the codebase.
6. The change must stay scoped to the backend rule, test, and route surfaces.
7. Do not run shell commands during the assessment run.
8. Do not use SQL during the assessment run.

## Concrete Scenario

Use the lesson's current instructions, architecture doc, and notification-preference backend/frontend surfaces to implement a cross-stack hardening slice for event-channel validation.

## What Good Output Looks Like

Good output will usually:

- create a pure validator module under `backend/src/rules/`
- create matching tests under `backend/tests/unit/`
- wire the validator into the existing route with a minimal import
- enforce mandatory-event channel protection
- enforce LEGAL-218 California SMS restriction
- include false positive and hard negative test coverage
- keep the capstone narrow enough to be actionable
