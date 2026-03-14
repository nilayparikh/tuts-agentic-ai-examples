# Loan Workbench — Project Context

> **This file shows the corrected version of the drifted example.**
> It now follows the clean example's structure and keeps references valid.

## Project

Loan Workbench API — TypeScript + Express REST service managing loan
application lifecycles with regulatory compliance, role-based access, and
audit-first persistence.

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

Audit events are recorded before persistence. Mutating operations should use
structured logging only; do not use `console.log()`.

## Coding Conventions

- `const` over `let`; never `var`
- All route handlers are `async`
- All errors return structured JSON: `{ error: string, code: string }`
- No stack traces in error responses
- Feature flags use 404, not 403
- Keep global instructions concise; detailed route, notification, and test
  patterns belong in scoped instructions or dedicated docs
- Annotate tests with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable

## References

- Canonical project context: see `.github/copilot-instructions.md`
- Clean example: see `.github/examples/clean/copilot-instructions.md`
- Maintenance cadence: see `/docs/maintenance-schedule.md`
- Lesson scope and expected output: see `/docs/operating-model-example.md`
- Context audit: see `.github/scripts/audit_context.py`
- Stale reference detector: see `.github/scripts/detect_stale_refs.py`
