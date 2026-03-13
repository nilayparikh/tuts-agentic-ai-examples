# Lesson 07 — Surface Strategy

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Tailoring context for different Copilot surfaces and ensuring portability across environments.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Different Copilot surfaces consume context differently.

| Surface | Context Access | Best For |
| --- | --- | --- |
| Agent mode (Chat) | Full `.github/`, agents, prompts, tools | Complex multi-step tasks |
| Inline completions | `.github/instructions/` auto-scoped by file | Line-by-line generation |
| CLI (`copilot`) | Baseline repo context plus what it discovers | Quick scripted prompting |
| Other IDEs | Portable baseline instructions | Cross-IDE consistency |

## Context Files

| Path | Purpose |
| --- | --- |
| `.github/copilot-instructions.md` | Universal baseline |
| `.github/instructions/api.instructions.md` | API-scoped rules |
| `.github/agents/reviewer.agent.md` | Review agent |
| `docs/cli-guide.md` | CLI usage reference |
| `docs/portability-matrix.md` | Surface compatibility reference |

## Copilot CLI Workflow

Run from the lesson root:

```bash
copilot -p "Explain which repository instructions are most portable across CLI, editor chat, inline completions, and other IDE surfaces." --allow-all-tools
```

Then test a generation prompt:

```bash
copilot -p "Review the notification preferences API and suggest one improvement that would still work across the widest range of Copilot surfaces." --allow-all-tools
```

Expected result: the CLI can reason about portability, but it does not demonstrate path-scoped activation the way the editor does.

## VS Code Chat Workflow

Compare the same repository ask across three surfaces:

- Agent mode for full multi-step assistance
- Inline completions inside an API file for scoped instruction activation
- Ask mode with explicit file attachments where needed

Use the portability matrix and ask which guidance belongs in the universal baseline versus scoped instructions.

Expected result: you see why some guidance must live in `copilot-instructions.md`, while more specialized rules should remain scoped.

## Cleanup

```bash
python util.py --clean
```
