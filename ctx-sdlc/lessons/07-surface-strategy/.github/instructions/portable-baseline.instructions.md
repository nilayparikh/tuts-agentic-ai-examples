---
applyTo: "**"
---

# Portable Baseline Instructions

This file mirrors the cross-surface-portable subset of the lesson's existing
baseline guidance.

Use `.github/copilot-instructions.md` as the canonical universal baseline,
because that repository-level file is the artifact explicitly designed to load
across CLI, Chat, inline completions, coding agent, and code review surfaces.
Keep narrower or stronger rules in scoped instructions, agents, or docs.

## Project

Loan Workbench API — TypeScript + Express REST service managing loan
application lifecycles with regulatory compliance (California SMS restriction),
role-based access, and audit-first persistence.

## Tech Stack

- Runtime: Node.js 20 LTS
- Language: TypeScript 5.x (strict mode)
- Framework: Express 4 with better-sqlite3 for persistence
- Queue: in-process event broker for async side-effects
- Tests: Vitest, not Jest
- Modules: ESM only, not CommonJS
- Logging: structured JSON via pino

## Architecture

Preserve the four-layer separation:

1. Routes handle HTTP concerns and delegation.
2. Rules contain pure business logic with no I/O.
3. Services handle persistence and external integrations.
4. Queue handles async side-effects.

Follow this request flow:

Route -> authenticate -> authorize -> validate -> Rule -> Service -> respond.

Audit events must be emitted before persistence. If audit recording fails, the
write must not proceed.

## Cross-Surface Conventions

- Prefer `const` over `let`; never use `var`.
- Keep route handlers `async`.
- Return structured JSON errors shaped as `{ error: string, code: string }`.
- Do not return stack traces in error responses.
- Treat disabled features as 404, not 403.
- Use structured logging; do not use `console.log()`.
- When applicable, annotate tests with `// FALSE POSITIVE` or
  `// HARD NEGATIVE`.

## References

- `/docs/architecture.md`
- `/docs/api-conventions.md`
- `/docs/adr/`
