# Loan Workbench — Project Instructions

This is a TypeScript Express REST API with an embedded message broker and
SQLite persistence for commercial loan processing.

## Conventions

- Use TypeScript strict mode — no `any` types in production code.
- Use ESM imports (`import ... from "..."`) — not CommonJS `require()`.
- All route handlers must pass errors to `next()` for central error handling.
- All mutating operations must be audited via the queue broker or direct DB write.
- Domain types live in `app/backend/src/models/types.ts` — import from there, do not redeclare.
- Business rules live in `app/backend/src/rules/` — do not embed rule logic in route handlers.

## Architecture

- Backend: `app/backend/src/` — Express API + middleware + queue broker + SQLite DB.
- Frontend: `app/frontend/src/` — Vanilla TypeScript SPA.
- Loan applications follow a strict state machine — see `VALID_TRANSITIONS` in `app/backend/src/models/types.ts`.
- State transitions not in the valid set must be rejected with 422.
- The queue broker (`app/backend/src/queue/broker.ts`) handles async events (notifications, audit).
- Message contracts in `app/backend/src/queue/contracts.ts` are a breaking-change surface.

## Error Handling

- Use the central error handler in `app/backend/src/middleware/error-handler.ts`.
- In route handlers: wrap async logic in try/catch and call `next(err)`.
- Never send stack traces or internal identifiers in API responses.
