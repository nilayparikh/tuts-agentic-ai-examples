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
| `docs/instruction-layering-example.md` | — | Concrete lesson-03 demo target and constraints |

## Example Goal

This lesson should demonstrate scoped instruction layering, not just a random backend change.

For this example, the intended change is:

- create a pure rule module at `src/backend/src/rules/notification-channel-rules.ts`
- add matching tests at `src/backend/tests/unit/notification-channel-rules.test.ts`
- make the rule and tests reflect the scoped instruction files for `rules/` and `tests/`
- preserve the repository's expectations around structured rule results, LEGAL-218 references, and explicit test categories

## Copilot CLI Workflow

Use the installed CLI from the lesson root:

```bash
copilot -p "Create a pure business-rule module for notification channel restrictions and add matching unit tests. Follow the repository conventions you discover." --allow-all-tools
```

Expected outcome:

- the CLI can still discover repository-wide rules and scoped instruction files when it edits both `src/backend/src/rules/` and `src/backend/tests/`
- the generated rule module should stay pure, use structured results, and include LEGAL-218 in the California restriction
- the generated tests should mirror the new source file and cover happy path, boundary, false positive, and hard negative scenarios

The editor remains the clearest place to observe file-scoped activation, but this CLI demo is now strong enough to assess whether layered instructions were applied.

## VS Code Chat Workflow

Rules layer:

- open `src/backend/src/rules/notification-channel-rules.ts`
- ask for a pure validation rule for notification channel changes

Test layer:

- open `src/backend/tests/unit/notification-channel-rules.test.ts`
- ask for tests covering false positives and hard negatives

Security layer:

- open `src/backend/src/middleware/auth.ts`
- ask for auth or rate-limiting changes

Expected result: each location activates a different instruction stack automatically.

## Cleanup

```bash
python util.py --clean
```
