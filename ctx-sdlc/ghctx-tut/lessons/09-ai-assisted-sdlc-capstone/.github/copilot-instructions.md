# Loan Workbench — Capstone Project Context

> **Capstone**: This lesson combines all context-engineering surfaces learned
> in Lessons 01–08. The `.github/` folder demonstrates a complete, production-
> grade Copilot configuration for the Loan Workbench codebase.

## Project

Loan Workbench — TypeScript + Express REST API managing loan application
lifecycles with regulatory compliance (California SMS restriction), role-based
access, audit-first persistence, and an embedded message broker.

## Tech Stack

- Runtime: Node.js 20 LTS
- Language: TypeScript 5.x (strict mode)
- Framework: Express 4
- Tests: Vitest
- Modules: ESM only (`import`/`export` — no CommonJS `require()`)
- Database: SQLite via better-sqlite3
- Queue: Embedded in-process message broker
- Frontend: Vanilla TypeScript SPA (no framework)

## Architecture

Three-layer separation in `app/backend/src/`:

1. **Routes** (`app/backend/src/routes/`) — HTTP handling, parameter extraction, delegation
2. **Rules** (`app/backend/src/rules/`) — pure business logic, no I/O
3. **Services** (`app/backend/src/services/`) — persistence, external integrations, audit

Request flow: Route → authenticate → authorize → validate → Rule → Service → respond.

Audit events are recorded BEFORE persistence — if logging fails, the write
does NOT proceed (fail-closed semantics).

Domain types live in `app/backend/src/models/types.ts` — import from there, do not redeclare.

The queue broker (`app/backend/src/queue/broker.ts`) handles async events.
Message contracts in `app/backend/src/queue/contracts.ts` are a breaking-change surface.

Frontend: `app/frontend/src/` — Vanilla TypeScript SPA.

## Coding Conventions

### TypeScript

- Strict mode always
- `const` over `let`, never `var`
- ESM imports only — no CommonJS `require()`
- Structured JSON logging — never `console.log()`

### Express (Backend)

- Route handlers delegate to rules/services — no inline business logic
- All routes `async`
- Structured error responses: `{ error: string, code: string }` — no stack traces
- Feature flags return 404 (not 403) when disabled
- All mutating operations must be audited via the queue broker

### Testing

- Vitest for all tests
- `describe`/`it`/`expect` pattern
- Business rule tests: happy path, boundary, false positive, hard negative

## Error Handling

- Use the central error handler in `app/backend/src/middleware/error-handler.ts`.
- In route handlers: wrap async logic in try/catch and call `next(err)`.
- Never send stack traces or internal identifiers in API responses.

## References

- Architecture: `/docs/architecture.md`
