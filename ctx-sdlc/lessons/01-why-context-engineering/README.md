# Lesson 01 — Why Context Engineering

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** The same prompt produces different code depending on what context the repository provides.

## Setup

```bash
python util.py --setup
cd src && npm install
```

## What This Demonstrates

Run the same prompt with and without project context to see how .github/copilot-instructions.md and docs/architecture.md change AI output.

| Scenario          | Context                         | Expected Quality                      |
| ----------------- | ------------------------------- | ------------------------------------- |
| Without context   | Nothing auto-loaded             | Generic code, misses domain rules     |
| With context      | .github/ + docs/ available  | Architecturally correct, domain-aware |

## Context Files

| Path                              | Purpose                                     |
| --------------------------------- | ------------------------------------------- |
| `.github/copilot-instructions.md` | Global project identity and rules           |
| `docs/architecture.md`            | System shape, domain model, key constraints |

## Cleanup

```bash
python util.py --clean
```
