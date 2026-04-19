# Loan Workbench — Project Instructions

This is a TypeScript Express REST API with an embedded message broker and
SQLite persistence for commercial loan processing.

## Conventions

- Use TypeScript strict mode — no `any` types in production code.
- Use ESM imports (`import ... from "..."`) — not CommonJS `require()`.
- All route handlers must pass errors to `next()` for central error handling.
- Domain types live in `src/backend/src/models/types.ts` — import from there, do not redeclare.
- Business rules live in `src/backend/src/rules/` — do not embed rule logic in route handlers.
- All mutating operations must emit audit events via the queue broker.
- Before changing backend routes, read `docs/architecture.md`, `docs/api-conventions.md`, and `docs/preference-management-example.md`.

## Architecture

- Backend: `src/backend/src/` — Express API + middleware + queue broker + SQLite DB.
- Frontend: `src/frontend/src/` — Vanilla TypeScript SPA.
- Loan applications follow a strict state machine — see `VALID_TRANSITIONS`.
- The embedded broker (`src/backend/src/queue/broker.ts`) decouples notification and audit side-effects.
- Message contracts in `src/backend/src/queue/contracts.ts` are a breaking-change surface.

## Error Handling

- Use the central error handler in `src/backend/src/middleware/error-handler.ts`.
- Error prefixes (`FORBIDDEN:`, `VALIDATION:`, `NOT_FOUND:`) map to HTTP status codes.

## Notification Preferences

- Preferences are stored per-user with UPSERT semantics.
- Users can set preferences for their own account only.
- Compliance reviewers may read (but NOT write) other users' preferences.
- SMS → email fallback activates when the SMS provider is unhealthy.
- Lesson 02 example target: harden the existing notification preference write routes in `src/backend/src/routes/notifications.ts` so they all follow the same repository rules.
- Keep the existing generic route and the existing channel-specific routes for email and SMS.
- The change should normalize all write paths around owner-only writes, delegated-session blocking, compliance-reviewer read-only behavior, audit logging, and central `FORBIDDEN:` error-prefix handling.
