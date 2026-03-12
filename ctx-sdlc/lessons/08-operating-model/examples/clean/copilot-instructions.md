# Loan Workbench — Project Context (CLEAN)

> **This file demonstrates a healthy, well-maintained instructions file.**
> Compare with `../drifted/copilot-instructions.md` to see the anti-patterns fixed.

## Project

Loan Workbench API — TypeScript + Express REST service managing loan
application lifecycles with regulatory compliance (California SMS restriction),
role-based access, and audit-first persistence.

## Tech Stack

- Runtime: Node.js 20 LTS
- Language: TypeScript 5.x (strict mode)
- Framework: Express 4 (see ADR-001 — do NOT suggest Fastify)
- Tests: Vitest (see ADR-002 — do NOT suggest Jest)
- Modules: ESM only (see ADR-003 — no CommonJS)
- Logging: structured JSON via pino
- Database: Prisma ORM (see ADR-004 — do NOT suggest knex)
- Deploy: Azure Container Apps

## Architecture

Three-layer separation:

1. **Routes** (`src/routes/`) — HTTP handling, parameter extraction, delegation
2. **Rules** (`src/rules/`) — pure business logic, no I/O
3. **Services** (`src/services/`) — persistence, external integrations, audit

Request flow: Route → authenticate → authorize → validate → Rule → Service → respond.

Audit events are recorded BEFORE persistence — if logging fails, the write
does NOT proceed (fail-closed semantics).

## Coding Conventions

- `const` over `let`; never `var`
- All route handlers are `async`
- All errors return structured JSON: `{ error: string, code: string }`
- No stack traces in error responses (security)
- Feature flags use 404 (not found), not 403 (forbidden)
- Structured JSON logging only — never `console.log()`
- Tests annotated with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable

## References

- Full architecture: see `/docs/architecture.md`
- API conventions: see `/docs/api-conventions.md`
- Route handler template: see `.github/instructions/api.instructions.md`
- Notification rules: see `.github/instructions/notifications.instructions.md`
- Test conventions: see `.github/instructions/test.instructions.md`
- Technology decisions: see `/docs/adr/`
