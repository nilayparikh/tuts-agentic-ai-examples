# Lesson 03 — Instruction Architecture

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Writing layered custom instructions that scope rules to repos, paths, technologies, and concerns.

## Setup

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

## What This Demonstrates

A single global instruction file cannot address all coding conventions. This lesson shows **layered .instructions.md** files that activate based on the file being edited:

| Editing                              | Active Instructions                                                                      |
| ------------------------------------ | ---------------------------------------------------------------------------------------- |
| `src/backend/src/routes/*.ts`        | `copilot-instructions.md` + `backend.instructions.md`                                    |
| `src/backend/src/rules/*.ts`         | `copilot-instructions.md` + `backend.instructions.md` + `business-rules.instructions.md` |
| `src/backend/src/middleware/auth.ts` | `copilot-instructions.md` + `backend.instructions.md` + `security.instructions.md`       |
| `src/backend/tests/*.test.ts`        | `copilot-instructions.md` + `testing.instructions.md`                                    |

## Context Files

| Path                                                  | applyTo                          | Purpose                             |
| ----------------------------------------------------- | -------------------------------- | ----------------------------------- |
| `.github/copilot-instructions.md`                     | all files                        | Project-wide conventions            |
| `.github/instructions/backend.instructions.md`        | `src/backend/src/**/*.ts`        | Express API patterns                |
| `.github/instructions/business-rules.instructions.md` | `src/backend/src/rules/**`       | Business rule authoring conventions |
| `.github/instructions/security.instructions.md`       | `src/backend/src/middleware/**`   | Auth and security patterns          |
| `.github/instructions/testing.instructions.md`        | `src/backend/tests/**`           | Test conventions and anti-patterns  |
| `docs/architecture.md`                                | —                                | Referenced by instructions          |

## Cleanup

```bash
python util.py --clean
```
