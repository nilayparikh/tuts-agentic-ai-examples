# Loan Workbench — Project Context

> **This file shows the repaired version of the Lesson 08 drifted example.**

## Project

Loan Workbench API — TypeScript + Express REST service managing loan
application lifecycles with regulatory compliance (California SMS restriction),
role-based access, and audit-first persistence.

## Tech Stack

- Runtime: Node.js 20 LTS
- Language: TypeScript 5.x (strict mode)
- Framework: Express 4
- Tests: Vitest
- Modules: ESM only
- Logging: structured JSON via pino
- Database: Prisma ORM
- Deploy: Azure Container Apps

## Architecture

Three-layer separation:

1. **Routes** (`app/backend/src/routes/`) — HTTP handling, parameter extraction, delegation
2. **Rules** (`app/backend/src/rules/`) — pure business logic, no I/O
3. **Services** (`app/backend/src/services/`) — persistence, external integrations, audit

Request flow: Route -> authenticate -> authorize -> validate -> Rule -> Service -> respond.

Audit events are recorded BEFORE persistence — if logging fails, the write
does NOT proceed (fail-closed semantics).

## Coding Conventions

- `const` over `let`; never `var`
- All route handlers are `async`
- All errors return structured JSON: `{ error: string, code: string }`
- No stack traces in error responses
- Feature flags use 404, not 403
- Structured JSON logging only — never `console.log()`
- Keep global instructions concise; route-level examples belong in scoped instruction files

## References

- Canonical project context: see `.github/copilot-instructions.md`
- Maintenance cadence: see `/docs/maintenance-schedule.md`
- Lesson scope and expected output: see `/docs/operating-model-example.md`
- Context audit script: see `.github/scripts/audit_context.py`
- Stale reference detector: see `.github/scripts/detect_stale_refs.py`
- Healthy reference example: see `.github/examples/clean/copilot-instructions.md`
