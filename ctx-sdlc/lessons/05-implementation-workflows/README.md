# Lesson 05 — Implementation Workflows

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Specialized agents for implementation, review, and testing — each with different tool access and instructions.

## Setup

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

## What This Demonstrates

Three agents with different capabilities form an implementation workflow:

| Agent          | Tools                                          | Role                              |
| -------------- | ---------------------------------------------- | --------------------------------- |
| `implementer`  | editFiles, runInTerminal, codebase, problems   | Writes and runs code              |
| `reviewer`     | codebase, problems, usages (read-only)         | Reviews without editing           |
| `tester`       | editFiles, runInTerminal, runTests, testFailure| Writes and runs tests             |

Plus a **TDD workflow skill** and **prompt files** for structured implementation and review.

## Context Files

| Path                                        | Purpose                         |
| ------------------------------------------- | ------------------------------- |
| `.github/agents/implementer.agent.md`       | Implementation agent definition |
| `.github/agents/reviewer.agent.md`          | Code review agent definition    |
| `.github/agents/tester.agent.md`            | Testing agent definition        |
| `.github/prompts/implement-feature.prompt.md`| Feature implementation workflow |
| `.github/prompts/review-changes.prompt.md`   | Code review workflow            |
| `.github/skills/tdd-workflow/SKILL.md`       | Test-driven development skill   |
| `docs/implementation-playbook.md`            | Implementation standards        |
| `specs/non-functional-requirements.md`       | NFR constraints                 |

## Cleanup

```bash
python util.py --clean
```
