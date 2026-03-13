# Loan Workbench — Project Instructions

This is a TypeScript Express REST API with an embedded message broker and
SQLite persistence for commercial loan processing.

## Conventions

- Use TypeScript strict mode — no `any` types in production code.
- Use ESM imports (`import ... from "..."`) — not CommonJS `require()`.
- All route handlers must pass errors to `next()` for central error handling.
- Domain types live in `app/backend/src/models/types.ts` — import from there, do not redeclare.
- Business rules live in `app/backend/src/rules/` — do not embed rule logic in route handlers.
- All mutating operations must emit audit events via the queue broker.

## Architecture

- Backend: `app/backend/src/` — Express API + middleware + queue broker + SQLite DB.
- Frontend: `app/frontend/src/` — Vanilla TypeScript SPA.
- Loan applications follow a strict state machine — see `VALID_TRANSITIONS`.
- The embedded broker (`app/backend/src/queue/broker.ts`) decouples notification and audit side-effects.
- Message contracts in `app/backend/src/queue/contracts.ts` are a breaking-change surface.

## Error Handling

- Use the central error handler in `app/backend/src/middleware/error-handler.ts`.
- Error prefixes (`FORBIDDEN:`, `VALIDATION:`, `NOT_FOUND:`) map to HTTP status codes.

## Notification Preferences

- Preferences are stored per-user with UPSERT semantics.
- Users can set preferences for their own account only.
- Compliance reviewers may read (but NOT write) other users' preferences.
- SMS → email fallback activates when the SMS provider is unhealthy.
