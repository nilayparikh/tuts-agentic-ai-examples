# Loan Workbench — Project Context

> **Auto-loaded** by all Copilot surfaces that support repository-level instructions.
> This is the most portable context artifact — it works in VS Code Chat,
> VS Code Inline, GitHub CLI, Copilot Coding Agent, and Code Review suggestions.

## Project

Loan Workbench API — TypeScript + Express REST service managing loan
application lifecycles with regulatory compliance (California SMS restriction),
role-based access, and audit-first persistence.

## Tech Stack

- Runtime: Node.js 20 LTS
- Language: TypeScript 5.x (strict mode)
- Framework: Express 4, better-sqlite3 for persistence
- Queue: In-process event broker for async side-effects
- Tests: Vitest (see ADR-002 — do NOT suggest Jest)
- Modules: ESM only (see ADR-003 — no CommonJS)
- Logging: structured JSON via pino

## Architecture

Four-layer separation:

1. **Routes** (`backend/src/routes/`) — HTTP handling, parameter extraction, delegation
2. **Rules** (`backend/src/rules/`) — pure business logic, no I/O
3. **Services** (`backend/src/services/`) — persistence, external integrations, audit
4. **Queue** (`backend/src/queue/`) — async event handling (notifications, audit)

Request flow: Route → authenticate → authorize → validate → Rule → Service → respond.

Audit events are emitted BEFORE persistence — if the audit fails, the write
does NOT proceed (fail-closed semantics).

## Coding Conventions

- `const` over `let`; never `var`
- All route handlers are `async`
- All errors return structured JSON: `{ error: string, code: string }`
- No stack traces in error responses (security)
- Feature flags use 404 (feature not found), not 403 (forbidden)
- Logging: structured JSON, never `console.log()`
- Tests annotated with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable

## References

- Full architecture: see `/docs/architecture.md`
- API conventions: see `/docs/api-conventions.md`
- Technology decisions: see `/docs/adr/`
