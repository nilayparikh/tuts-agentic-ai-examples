# Lesson 02 — Curate Project Context

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Building the shared context layer: `.github/` for behavior and `docs/` for knowledge.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Context has two complementary halves:

| Layer | Location | Contains | Activation |
| --- | --- | --- | --- |
| Behavior | `.github/` | How the model should behave | Auto-loaded by Copilot |
| Knowledge | `docs/` | What the model should know | Read or searched as needed |

## Context Files

| Path | Purpose |
| --- | --- |
| `.github/copilot-instructions.md` | Project-level behavioral guidance |
| `docs/architecture.md` | System architecture knowledge |
| `docs/api-conventions.md` | API design standards |

## Copilot CLI Workflow

Ask for architectural understanding and generation from the lesson root:

```bash
copilot -p "What is the architecture of this project, and what coding conventions should I follow for backend route changes?" --allow-all-tools
```

Then ask for generation:

```bash
copilot -p "Add a route handler for preference management with email and SMS channels. Follow the repository conventions you discover." --allow-all-tools
```

Expected outcome:

- behavior guidance comes through strongly from `.github/`
- knowledge from `docs/` is available only if the model chooses to read it

## VS Code Chat Workflow

Compare three modes.

Behavior only:

```text
Add a route for preference management. Users save notification channel preferences (email, SMS) per event type.
```

Knowledge only:

- explicitly attach `docs/architecture.md`
- ask the same prompt

Both together:

- keep `.github/copilot-instructions.md` in the workspace
- expose `docs/architecture.md` and `docs/api-conventions.md`
- ask the same prompt again

Expected result: the model becomes both style-consistent and architecturally correct.

## Cleanup

```bash
python util.py --clean
```
