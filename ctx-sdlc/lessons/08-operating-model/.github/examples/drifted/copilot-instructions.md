# Loan Workbench — Project Context

> **This file demonstrates the repaired drifted example.**
> It follows the clean example's conventions while keeping lesson references valid.

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

1. **Routes** — HTTP handling, parameter extraction, delegation
2. **Rules** — pure business logic, no I/O
3. **Services** — persistence, external integrations, audit

Request flow: Route -> authenticate -> authorize -> validate -> Rule ->
Service -> respond.

Audit events are recorded BEFORE persistence. If audit logging fails, the write
does NOT proceed.

## Coding Conventions

- `const` over `let`; never `var`
- All route handlers are `async`
- All errors return structured JSON: `{ error: string, code: string }`
- No stack traces in error responses (security)
- Feature flags use 404 (not found), not 403 (forbidden)
- Structured JSON logging only — never `console.log()`
- Keep global instructions concise; move route, notification, and test
  implementation details into scoped instructions or dedicated docs
- Tests annotated with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable

## References

- Canonical project context: see `.github/copilot-instructions.md`
- Maintenance cadence: see `/docs/maintenance-schedule.md`
- Lesson scope and expected output: see `/docs/operating-model-example.md`
- Context audit script: see `.github/scripts/audit_context.py`
- Stale reference detector: see `.github/scripts/detect_stale_refs.py`
- Healthy reference example: see `.github/examples/clean/copilot-instructions.md`
