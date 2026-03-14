# Lesson 02 — Preference Management Example

This document defines the concrete example used in Lesson 02.

## Objective

Show that curated repository context helps GitHub Copilot CLI make a route-level refactor that is not just syntactically valid, but also aligned with project standards and constraints.

## Expected Change Shape

The preferred implementation for this lesson is:

- keep existing notification preference routes in `src/backend/src/routes/notifications.ts`
- keep the existing bulk email-preference route
- keep the existing bulk SMS-preference route
- make all notification preference write handlers follow the same rules for authorization, delegated sessions, audit behavior, and central error handling

Relevant endpoints:

- `PUT /api/notifications/preferences`
- `PUT /api/notifications/preferences/:userId/email`
- `PUT /api/notifications/preferences/:userId/sms`

## Required Constraints

These constraints are part of the example and must be preserved by the generated code:

1. Users can modify only their own preferences.
2. Delegated sessions cannot modify preferences.
3. Compliance reviewers are read-only.
4. Authorization failures should use `throw new Error("FORBIDDEN: ...")` and pass the error to `next()` so the central error handler maps them consistently.
5. Every changed preference must preserve audit behavior.
6. No new queue contracts.
7. No new domain types.
8. No shell-command dependency during the assessment run.
9. Prefer extracting a small local helper inside `notifications.ts` if it removes repeated authorization code.
10. Discover the current write-path conventions from the existing route surface instead of assuming them from the prompt.

## Standard Notification Events

For this example, the channel-specific routes should update these events:

- `approval`
- `decline`
- `document-request`
- `manual-review-escalation`

## What Good Output Looks Like

Good output will usually:

- modify `backend/src/routes/notifications.ts`
- reuse `prefRepo.findPreference`, `prefRepo.setPreference`, and `auditAction`
- avoid inventing a new service or schema unless the prompt explicitly requires that
- keep the change small and local to the preference-routing surface
- replace ad-hoc `res.status(403).json(...)` write-path responses with central `FORBIDDEN:` error flow
