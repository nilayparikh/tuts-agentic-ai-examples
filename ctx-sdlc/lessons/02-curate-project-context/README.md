# Lesson 02 — Curate Project Context

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Building the shared context layer — .github/ for behavioral guidance and /docs/ for knowledge context.

## Setup

```bash
python util.py --setup
cd src && npm install
```

## What This Demonstrates

Context has two halves that complement each other:

| Layer     | Location   | Contains                                     | Activation             |
| --------- | ---------- | -------------------------------------------- | ---------------------- |
| Behavior  | .github/   | HOW the AI should behave (rules, style)      | Auto-loaded by Copilot |
| Knowledge | /docs/     | WHAT the AI should know (architecture, ADRs) | Referenced or searched |

## Context Files

| Path                              | Purpose                           |
| --------------------------------- | --------------------------------- |
| .github/copilot-instructions.md   | Project-level behavioral guidance |
| docs/architecture.md              | System architecture knowledge     |
| docs/api-conventions.md           | API design standards              |

## Cleanup

```bash
python util.py --clean
```
