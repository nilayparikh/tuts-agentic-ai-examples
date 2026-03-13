# Lesson 09 — AI-Assisted SDLC Capstone

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Full SDLC synthesis — combining all context engineering techniques from Lessons 01-08.

## Setup

```bash
python util.py --setup
cd src && npm install
```

## What This Demonstrates

This capstone exercise combines every context engineering surface into a single end-to-end workflow:

- **Instructions** (scoped by file type) — Lesson 03
- **Agents and prompts** (planning + implementation) — Lessons 04-05
- **Hooks and guardrails** — Lesson 06
- **Surface strategy** (portability) — Lesson 07
- **Maintenance** (keeping context fresh) — Lesson 08

The workspace has both API and frontend instruction files, simulating a full-stack project where different areas need different guidance.

## Context Files

| Path                                            | Purpose                            |
| ----------------------------------------------- | ---------------------------------- |
| `.github/copilot-instructions.md`               | Project-wide conventions           |
| `.github/instructions/api.instructions.md`      | API-specific patterns              |
| `.github/instructions/frontend.instructions.md` | Frontend-specific patterns         |
| `docs/architecture.md`                          | System architecture reference      |

## Cleanup

```bash
python util.py --clean
```
