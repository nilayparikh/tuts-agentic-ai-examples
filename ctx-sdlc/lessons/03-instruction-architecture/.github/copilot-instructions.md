# Loan Workbench — Project Instructions

This is a TypeScript Express REST API with an embedded message broker and
SQLite persistence for commercial loan processing.

## Conventions

- Use TypeScript strict mode — no `any` types in production code.
- Use ESM imports (`import ... from "..."`) — not CommonJS `require()`.
- All route handlers must pass errors to `next()` for central error handling.
- All mutating operations must be audited via the queue broker or direct DB write.
- Domain types live in `src/backend/src/models/types.ts` — import from there, do not redeclare.
- Business rules live in `src/backend/src/rules/` — do not embed rule logic in route handlers.
- Before changing business rules or tests, read `docs/architecture.md` and `docs/instruction-layering-example.md`.

## Architecture

- Read `docs/architecture.md` for system shape and component map.
- Backend: `src/backend/src/` — Express API + middleware + queue broker + SQLite DB.
- Frontend: `src/frontend/src/` — Vanilla TypeScript SPA.
- Loan applications follow a strict state machine — see `VALID_TRANSITIONS` in `src/backend/src/models/types.ts`.
- State transitions that are not in the valid set must be rejected with 422.

## Error Handling

- Use the central error handler in `src/backend/src/middleware/error-handler.ts`.
- In route handlers: wrap async logic in try/catch and call `next(err)`.
- Never send stack traces or internal identifiers in API responses.

## Testing

- Tests use Vitest and live in `src/backend/tests/`.
- Do not mock business rules — test them through their public API.
