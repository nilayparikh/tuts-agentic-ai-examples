# Lesson 08 — Operating Model

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Maintaining context over time with audit scripts, drift detection, and clean versus drifted examples.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Context files drift as codebases evolve. This lesson shows how to detect and fix staleness.

| Tool | Purpose |
| --- | --- |
| `scripts/audit_context.py` | Audits `.github/` for completeness and quality |
| `scripts/detect_stale_refs.py` | Finds broken file references |
| `examples/clean/` | Well-maintained reference example |
| `examples/drifted/` | Drifted example to diagnose |

## Context Files

| Path | Purpose |
| --- | --- |
| `.github/copilot-instructions.md` | Project-level instructions |
| `.github/scripts/audit_context.py` | Context audit script |
| `.github/scripts/detect_stale_refs.py` | Stale reference detector |
| `.github/examples/clean/copilot-instructions.md` | Clean example |
| `.github/examples/drifted/copilot-instructions.md` | Drifted example |
| `docs/maintenance-schedule.md` | Maintenance cadence |

## Copilot CLI Workflow

Use the CLI to reason about drift and maintenance:

```bash
copilot -p "Read .github/scripts/audit_context.py and .github/scripts/detect_stale_refs.py. Explain what kinds of context drift this repository is trying to catch." --allow-all-tools
```

Then compare the clean and drifted examples:

```bash
copilot -p "Compare .github/examples/clean/ and .github/examples/drifted/. Identify the most dangerous context drift issues." --allow-all-tools
```

Expected result: the CLI can explain the maintenance model, but the strongest experience is still in the editor with codebase navigation.

## VS Code Chat Workflow

Ask the agent to:

- run the audit scripts
- interpret the findings
- compare clean and drifted examples
- propose a maintenance PR plan

Expected result: the model shifts from code generation to context maintenance and operational hygiene.

## Cleanup

```bash
python util.py --clean
```
