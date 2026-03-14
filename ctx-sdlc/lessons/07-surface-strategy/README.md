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

This lesson should demonstrate surface-portability analysis quality, not code generation.

For this example, the intended outcome is:

- inspect the lesson's baseline instructions, scoped instructions, agent, and docs in a read-only workflow
- discover the relevant portability artifacts instead of relying on a hardcoded read list
- explain what guidance is portable across CLI, chat, inline, coding agent, and review surfaces
- identify one portability risk, one false positive, and one hard negative without editing code
- resolve which artifact should be treated as canonical if the lesson materials disagree

## Copilot CLI Workflow

Run from the lesson root:

```bash
copilot -p "Inspect the lesson's surface-strategy artifacts before answering. Discover the relevant baseline instructions, scoped instructions, agents, prompts, MCP, hooks, and docs that exist here rather than assuming a fixed file list. Produce a read-only surface-strategy analysis covering portability across CLI, chat, inline, coding agent, and code review. Include one portability risk, one false positive, one hard negative, prioritized recommendations, and identify which artifact should be treated as canonical if the lesson materials disagree." --allow-all-tools --deny-tool=sql
```

Then test a generation prompt:

```bash
copilot -p "Review the notification preferences API and suggest one improvement that would still work across the widest range of Copilot surfaces." --allow-all-tools
```

Expected result:

- the CLI returns a source-grounded portability analysis without modifying files
- the analysis distinguishes universal baseline guidance from VS Code-only context layers
- the analysis resolves which artifact should be treated as canonical when portability guidance conflicts
- the analysis explicitly notes where CLI cannot demonstrate path-scoped activation or agent behavior directly

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
