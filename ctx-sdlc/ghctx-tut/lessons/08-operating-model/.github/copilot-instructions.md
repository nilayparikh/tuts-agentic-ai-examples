# Loan Workbench — Operating Model Context

This is a TypeScript Express REST API with an embedded message broker and
SQLite persistence for commercial loan processing.

## Context Maintenance Rules

- All context files (`.github/`, `docs/`) must stay in sync with the codebase.
- Stale references (wrong file paths, outdated technology names, removed APIs)
  degrade AI assistant output quality progressively over time.
- Run `.github/scripts/audit_context.py` periodically to detect drift.
- Run `.github/scripts/detect_stale_refs.py` to find broken references.

## Anti-Patterns to Avoid

1. **Copy-paste drift**: Instructions duplicated across files that diverge over time.
2. **Stale technology references**: Mentioning libraries or APIs no longer in use.
3. **Contradictory rules**: Instructions that conflict with each other across files.
4. **Over-specification**: Rules so detailed they break on minor refactors.
5. **Under-specification**: Vague guidance that provides no actionable constraint.

## Architecture

- Backend: `app/backend/src/` — Express API + middleware + queue broker + SQLite DB.
- Frontend: `app/frontend/src/` — Vanilla TypeScript SPA.
- Loan applications follow a strict state machine: submitted → under_review → approved/denied → funded/closed.
- Business rules live in `app/backend/src/rules/` — pure functions, no side effects.
- Audit logging is mandatory for all mutating operations.
