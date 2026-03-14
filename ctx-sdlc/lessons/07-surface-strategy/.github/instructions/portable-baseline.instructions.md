---
applyTo: "**"
---

# Portable Baseline Instructions

This file mirrors the subset of guidance from `.github/copilot-instructions.md`
that remains valid across CLI, Chat, inline completions, coding agent, and code
review surfaces.

If this file and `.github/copilot-instructions.md` ever disagree, treat
`.github/copilot-instructions.md` as canonical because it is the repository-level
baseline instruction file.

## Project

Loan Workbench API is a TypeScript and Express REST service that manages loan
application lifecycles with regulatory compliance, role-based access, and
audit-first persistence.

## Tech Stack

- Runtime: Node.js 20 LTS
- Language: TypeScript 5.x in strict mode
- Framework: Express 4 with `better-sqlite3`
- Queue: in-process event broker for async side-effects
- Tests: Vitest, not Jest
- Modules: ESM only, not CommonJS
- Logging: structured JSON via pino

## Architecture

Use the established four-layer split:

1. Routes handle HTTP concerns, parameter extraction, and delegation.
2. Rules contain pure business logic and do not perform I/O.
3. Services handle persistence, audit, and external integrations.
4. Queue code handles asynchronous side-effects.

Request flow should remain: Route -> authenticate -> authorize -> validate ->
Rule -> Service -> respond.

Audit events must be emitted before persistence. If audit recording fails, the
write must not proceed.

## Coding Conventions

- Prefer `const` over `let`; never use `var`.
- Keep route handlers `async`.
- Return structured JSON errors shaped like `{ error: string, code: string }`.
- Do not expose stack traces in error responses.
- Use 404 for feature-flag-disabled behavior instead of 403.
- Use structured logging and never `console.log()`.
- Keep test annotations such as `// FALSE POSITIVE` and `// HARD NEGATIVE`
  when the case warrants them.

## References

Use the existing docs for deeper detail:

- `docs/architecture.md`
- `docs/api-conventions.md`
- `docs/adr/`
