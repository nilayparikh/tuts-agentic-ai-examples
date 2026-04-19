# Exercise 1 — Context Foundation

> **Lessons Applied:** L02 (Curate Project Context) + L03 (Instruction Architecture)
> **Estimated Time:** 30–45 minutes
> **Difficulty:** Beginner

## Objective

Audit the existing context layer (`.github/` and `/docs/`) for the Loan
Workbench capstone project. Identify gaps. Fill them so an AI agent can
accurately reason about the notification subsystem without hallucinating.

## Background

The Loan Workbench already has a baseline context layer:

- `.github/copilot-instructions.md` — project-wide conventions
- `.github/instructions/api.instructions.md` — backend API patterns
- `.github/instructions/frontend.instructions.md` — frontend SPA patterns
- `docs/architecture.md` — system architecture (partially complete)

But when you ask an AI agent about the notification subsystem, it hallucinates.
It invents channel types that don't exist. It gets the LEGAL-218 rule wrong.
It doesn't know which events are mandatory. The context layer has gaps.

## Tasks

### Task 1: Audit the Existing Context

Open the `.github/` and `docs/` directories. Read each file. Answer these
questions in a scratch note:

1. Which backend subsystems are documented in `architecture.md`?
2. Which subsystems are NOT documented?
3. Are there any domain terms used inconsistently across the instruction files?
4. Does the architecture doc explain the notification delivery pipeline?
5. Is the LEGAL-218 California SMS restriction documented anywhere?

### Task 2: Update architecture.md

Add the following sections to `docs/architecture.md`:

1. **Notification Subsystem** — describe the delivery pipeline:
   - State transition → mandatory event check → channel routing → delivery → audit
   - Reference the actual source files: `mandatory-events.ts`, `notification-service.ts`,
     `preference-event-channel-validator.ts`

2. **Event-Channel Validation** — describe both constraints:
   - Mandatory event protection (at least one channel must stay enabled)
   - LEGAL-218 (California decline SMS restriction)

3. **Notification Preferences Data Model** — document the `NotificationPreference`
   interface fields

4. **Route Authorization** — document which roles can read vs write preferences,
   and the delegated session restriction

### Task 3: Create docs/VOCAB.md

Create a vocabulary file that pins down domain terms. Include at minimum:

- All `NotificationEvent` values and what triggers each one
- All `NotificationChannel` values
- What "mandatory event" means in this codebase
- What "LEGAL-218" refers to
- What "California restricted context" means and why the validator defaults to it
- The three user roles and their preference access levels
- What "delegated session" means

Format: markdown table with columns `Term`, `Definition`, `Do NOT Use`.

## Success Criteria

Run this test after completing the exercise:

1. Open a new AI chat session with only the project context loaded
2. Ask: "Explain the notification delivery pipeline in this codebase"
3. Ask: "What happens if I try to disable both email and SMS for the approval event?"
4. Ask: "What is LEGAL-218 and when does it apply?"

**Pass condition:** The agent's answers are factually correct — matching the
actual source code — without hallucinating event types, channels, or rules
that don't exist.

## Hints

- Read `backend/src/rules/mandatory-events.ts` to understand which transitions
  trigger mandatory notifications
- Read `backend/src/rules/preference-event-channel-validator.ts` to understand
  both validation rules
- Read `backend/src/routes/notifications.ts` to understand the route authorization
  pattern
- Check `backend/src/models/types.ts` for the exact type definitions

## What You're Practicing

- **L02 pattern:** Curating shared knowledge context in `/docs/`
- **L03 pattern:** Understanding how instruction files scope to paths
- **Core skill:** Writing documentation that AI agents can consume accurately
