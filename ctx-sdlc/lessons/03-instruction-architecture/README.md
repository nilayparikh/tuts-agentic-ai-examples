# Lesson 03 — Instruction Architecture

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Layered custom instructions scoped by file path, concern, and implementation surface.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

A single global instruction file is not enough. This lesson shows layered
`.instructions.md` files that activate based on the file being edited.

| Editing | Active Instructions |
| --- | --- |
| `src/backend/src/routes/*.ts` | `copilot-instructions.md` + `backend.instructions.md` |
| `src/backend/src/rules/*.ts` | `copilot-instructions.md` + `backend.instructions.md` + `business-rules.instructions.md` |
| `src/backend/src/middleware/auth.ts` | `copilot-instructions.md` + `backend.instructions.md` + `security.instructions.md` |
| `src/backend/tests/*.test.ts` | `copilot-instructions.md` + `testing.instructions.md` |

## Context Files

| Path | `applyTo` | Purpose |
| --- | --- | --- |
| `.github/copilot-instructions.md` | all files | Project-wide conventions |
| `.github/instructions/backend.instructions.md` | `src/backend/src/**/*.ts` | Express API patterns |
| `.github/instructions/business-rules.instructions.md` | `src/backend/src/rules/**` | Business-rule authoring conventions |
| `.github/instructions/security.instructions.md` | `src/backend/src/middleware/**` | Auth and security patterns |
| `.github/instructions/testing.instructions.md` | `src/backend/tests/**` | Test conventions and anti-patterns |
| `docs/architecture.md` | — | Referenced by instructions |

## Copilot CLI Workflow

Use the installed CLI from the lesson root:

```bash
copilot -p "Add a DELETE /notifications/preferences/:event endpoint that resets to defaults." --allow-all-tools
```

Expected outcome:

- the CLI can discover general project rules
- it does not demonstrate fine-grained path-scoped activation as clearly as the editor

That limitation is the point of the lesson.

## VS Code Chat Workflow

Routes layer:

- open `src/backend/src/routes/notifications.ts`
- ask for a DELETE endpoint that resets preferences to defaults

Rules layer:

- open `src/backend/src/rules/state-rules.ts`
- ask for a validation rule for notification channels by role

Security layer:

- open `src/backend/src/middleware/auth.ts`
- ask for auth or rate-limiting changes

Test layer:

- open `src/backend/tests/`
- ask for tests for the reset endpoint

Expected result: each location activates a different instruction stack automatically.

## Cleanup

```bash
python util.py --clean
```
