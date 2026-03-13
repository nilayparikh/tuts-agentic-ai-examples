# Lesson 09 — AI-Assisted SDLC Capstone

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Full SDLC synthesis combining the context-engineering techniques from Lessons 01-08.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

This capstone combines every major context surface into a single end-to-end workflow:

- instructions scoped by file type
- agents and prompts for planning and implementation
- hooks and guardrails
- cross-surface portability strategy
- maintenance and context freshness

The workspace includes both API and frontend instruction files, simulating a full-stack project with different guidance needs by area.

## Context Files

| Path | Purpose |
| --- | --- |
| `.github/copilot-instructions.md` | Project-wide conventions |
| `.github/instructions/api.instructions.md` | API-specific patterns |
| `.github/instructions/frontend.instructions.md` | Frontend-specific patterns |
| `docs/architecture.md` | System architecture reference |

## Copilot CLI Workflow

Use the CLI for a baseline cross-stack prompt:

```bash
copilot -p "Plan and implement the next increment of the Loan Workbench application across backend and frontend, following the repository conventions you discover." --allow-all-tools
```

Expected result: the CLI can produce a broad full-stack answer, but it will not match the richness of the specialized agent workflow.

## VS Code Chat Workflow

Suggested capstone flow:

1. Use planning context to outline the change.
2. Switch to an implementation agent for backend work where API instructions activate.
3. Move to frontend files where frontend instructions activate.
4. Run review or tester agents for follow-up validation.
5. Reflect on which lessons contributed which context surface.

Expected result: learners see how all earlier lessons combine into a practical SDLC workflow.

## Cleanup

```bash
python util.py --clean
```
