# Lesson 07 — Surface Strategy

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Tailoring context for different Copilot surfaces (Chat, Inline, CLI) and ensuring portability across IDEs.

## Setup

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

## What This Demonstrates

Different Copilot surfaces consume context differently. This lesson shows how to write instructions that work across:

| Surface           | Context Access                              | Best For                    |
| ----------------- | ------------------------------------------- | --------------------------- |
| Agent mode (Chat) | Full .github/, agents, prompts, tools       | Complex multi-step tasks    |
| Inline completions| .github/instructions/ (auto-scoped by file) | Line-by-line code generation|
| CLI (gh copilot)  | copilot-instructions.md only                | Quick explanations, suggests|
| Other IDEs        | copilot-instructions.md + instructions/     | Cross-IDE portability       |

## Context Files

| Path                                        | Purpose                                   |
| ------------------------------------------- | ----------------------------------------- |
| `.github/copilot-instructions.md`           | Universal baseline (works everywhere)     |
| `.github/instructions/api.instructions.md`  | API-scoped rules (editor surfaces only)   |
| `.github/agents/reviewer.agent.md`          | Review agent (VS Code Agent mode only)    |
| `docs/cli-guide.md`                         | CLI usage documentation                   |
| `docs/portability-matrix.md`                | Surface compatibility reference           |

## Cleanup

```bash
python util.py --clean
```
