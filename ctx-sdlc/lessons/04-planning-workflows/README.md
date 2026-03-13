# Lesson 04 — Planning Workflows

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Custom agents and prompt files for investigation, planning, and triage workflows.

## Setup

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

## What This Demonstrates

Planning workflows use **read-only agents** and **prompt files** that combine context from docs/, specs/, and the codebase to produce structured plans — without editing code.

| File                                      | Type   | Purpose                                          |
| ----------------------------------------- | ------ | ------------------------------------------------ |
| `.github/agents/planner.agent.md`         | Agent  | Read-only investigator (codebase, problems, usages) |
| `.github/prompts/investigate-bug.prompt.md`| Prompt | Bug investigation workflow                        |
| `.github/prompts/plan-feature.prompt.md`   | Prompt | Feature planning workflow                         |
| `.github/prompts/triage-incident.prompt.md`| Prompt | Production incident triage                        |

## Context Files

| Path                                           | Purpose                        |
| ---------------------------------------------- | ------------------------------ |
| `docs/architecture.md`                         | System architecture reference  |
| `docs/adr/ADR-003-frontend-state.md`           | Architecture decision record   |
| `specs/product-spec-notification-preferences.md`| Product specification          |
| `specs/non-functional-requirements.md`          | NFR constraints                |
| `specs/bug-report.md`                           | Sample bug report for triage   |
| `specs/feature-request.md`                      | Sample feature request         |

## Cleanup

```bash
python util.py --clean
```
