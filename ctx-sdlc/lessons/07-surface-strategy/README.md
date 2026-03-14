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
| `docs/surface-strategy-example.md` | Concrete lesson-07 demo target and assessment constraints |

## Example Goal

This lesson should demonstrate surface-portability analysis through produced artifacts.

For this example, the intended outcome is:

- inspect the lesson's baseline instructions, scoped instructions, agent, and docs
- discover the relevant portability artifacts instead of relying on a hardcoded read list
- create a portable-baseline instruction file extracting the cross-surface-portable subset
- create a surface-portability notes document with risk taxonomy and recommendations
- the changes are assessable via actual vs expected file and pattern comparison

## Copilot CLI Workflow

Run from the lesson root:

```bash
copilot -p "Inspect the lesson's surface-strategy artifacts before answering. Discover the relevant baseline instructions, scoped instructions, agents, prompts, MCP, hooks, and docs that exist here rather than assuming a fixed file list. Then create two new files based on your analysis: 1. Create .github/instructions/portable-baseline.instructions.md containing the extracted cross-surface-portable subset of the existing instructions that works on CLI, Chat, inline completions, coding agent, and code review surfaces. Use applyTo: '**' scope. 2. Create docs/surface-portability-notes.md documenting which features are portable vs surface-specific, one concrete portability risk, one false positive, one hard negative, and recommendations for where each kind of guidance should live. Follow the discovered instruction architecture conventions. Apply the changes directly in files. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
```

Expected result:

- the CLI creates `.github/instructions/portable-baseline.instructions.md` and `docs/surface-portability-notes.md`
- the portable baseline instruction contains only cross-surface guidance
- the portability notes document includes risk taxonomy with false positive and hard negative
- `.output/change/demo.patch` contains the new files
- `.output/change/comparison.md` shows actual vs expected file and pattern match results

## VS Code Chat Workflow

Compare the same repository ask across three surfaces:

- Agent mode for full multi-step assistance
- Inline completions inside an API file for scoped instruction activation
- Ask mode with explicit file attachments where needed

Use the portability matrix and ask which guidance belongs in the universal baseline versus scoped instructions.

Expected result: you see why some guidance must live in `copilot-instructions.md`, while more specialized rules should remain scoped.

For the captured demo run, use `python util.py --demo --model gpt-5.4`.

## Cleanup

```bash
python util.py --clean
```
