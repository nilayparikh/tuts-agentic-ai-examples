---
applyTo: "app/backend/src/rules/**"
---

# Business Rules Instructions

Rules for authoring and modifying business rule modules in `app/backend/src/rules/`.

## Authoring Standards

- Each rule module focuses on one concern: state restrictions, mandatory events, or role defaults.
- Rule functions must be **pure** — they receive data and return a result. No side effects, no database calls, no audit writes.
- All rule functions must return structured results (not just booleans) with human-readable `reason` strings for the UI.
- Add block comments at the top of each module documenting **false positive** and **hard negative** patterns.

## False Positives and Hard Negatives

When adding a new rule, always document:

- **False positive**: A scenario that looks like a rule violation but is actually correct behavior.
  Example: Disabling SMS for mandatory events is valid when email remains enabled.
- **Hard negative**: A scenario that looks like valid behavior but actually violates a rule.
  Example: Enabling decline SMS on a California loan looks like a normal toggle but violates LEGAL-218.

## State-Specific Rules

- State restrictions reference legal tracking tickets (e.g. `LEGAL-218`).
- Always include the ticket ID in the restriction definition AND the user-facing reason string.
- Use uppercase state codes internally; accept case-insensitive input.
- Multi-state portfolio views must aggregate restrictions, not flatten them.

## Mandatory Event Rules

- The mandatory events set is defined in `mandatory-events.ts`.
- Validation checks the proposed change against ALL current preferences for the user+event combination.
- Enabling a channel is always allowed; only disabling is guarded.

## Role Defaults

- Default matrices are per-role, not per-user.
- Compliance reviewers have NO defaults (read-only role).
- Default generation must be idempotent — calling it twice must not duplicate records.
