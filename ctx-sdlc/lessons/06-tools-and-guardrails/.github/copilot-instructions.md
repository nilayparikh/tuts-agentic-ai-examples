# Loan Workbench — Copilot Instructions (Guardrails Focus)

## Project

TypeScript Express API with embedded message broker and SQLite persistence
for loan application workflow management. This workspace uses MCP servers and
hooks for capability expansion and enforcement.

## Tool Policy

### MCP Servers

This project configures MCP servers in `.github/mcp.json`. Follow these rules:

1. **Database access is read-only.** Never attempt to write to the database via
   MCP. All mutations go through the Express API routes with audit trail.
2. **Filesystem access is scoped.** The MCP filesystem server can only read
   `app/backend/src/`, `app/backend/tests/`, and `docs/`. It cannot access
   `.env`, `node_modules`, or config files with secrets.
3. **Do not add MCP servers** without updating `docs/tool-trust-boundaries.md`
   with the new server's trust classification.

### Hooks

Hooks in `.github/hooks/` enforce deterministic rules. Do not try to bypass them:

1. **Pre-commit validation** (`pre-commit-validate.json`): Runs lint and tests.
   If they fail, the commit is blocked. Fix the issues — do not disable the hook.
2. **Post-save formatting** (`post-save-format.json`): Prettier runs after every
   `.ts` file save. Do not add manual formatting code.
3. **File protection** (`file-protection.json`): Certain files cannot be edited
   by AI assistance. See `docs/security-policy.md` for the approval process.

## Security Rules

- Audit events must succeed before mutations persist (fail-closed).
- Error responses must not leak internal state or stack traces.
- Delegated sessions cannot perform write operations.
- Feature flags use 404 (not 403) for non-pilot users.
- Protected files require manual approval for changes.

## Code Conventions

- TypeScript strict mode, ESM imports.
- Business rules in `app/backend/src/rules/` — pure functions, no side effects.
- Services in `app/backend/src/services/` — I/O and external integrations.
- Routes in `app/backend/src/routes/` — orchestration only, delegate to rules and services.
- Queue broker in `app/backend/src/queue/` — async event handling (notifications, audit).
- All tests in `app/backend/tests/` using Vitest.
