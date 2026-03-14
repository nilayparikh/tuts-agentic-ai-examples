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
| `docs/operating-model-example.md` | Concrete lesson-08 demo target and assessment constraints |

## Example Goal

This lesson should demonstrate context-maintenance through direct drift repair.

For this example, the intended outcome is:

- inspect the maintenance scripts, clean example, drifted example, and schedule
- discover the relevant maintenance artifacts instead of relying on a hardcoded read list
- fix the drifted example by resolving all discovered drift issues directly in the file
- the changes are assessable via actual vs expected file and pattern comparison

## Copilot CLI Workflow

Fix the drifted example:

```bash
copilot -p "Inspect the lesson's context-maintenance artifacts before answering. Discover the relevant project instructions, audit scripts, clean and drifted examples, and maintenance docs that exist here rather than assuming a fixed file list. Then fix the drifted example at .github/examples/drifted/copilot-instructions.md by resolving all drift issues you find. Specifically: update stale technology references (Node.js version, logging library), remove contradictory rules (console.log vs structured logging), fix dead file path references (deleted helpers directory), remove over-specified inline code blocks that belong in scoped instructions, and align the drifted file with the clean example's conventions for accuracy and conciseness. Apply the fixes directly in the file. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
```

Expected result:

- the CLI fixes `.github/examples/drifted/copilot-instructions.md`
- stale Node.js and logging references are updated
- contradictory rules are resolved
- dead file references are removed
- `.output/change/demo.patch` contains the drift fixes
- `.output/change/comparison.md` shows actual vs expected file and pattern match results

## VS Code Chat Workflow

Ask the agent to:

- run the audit scripts
- interpret the findings
- compare clean and drifted examples
- propose a maintenance PR plan

Expected result: the model shifts from code generation to context maintenance and operational hygiene.

For the captured demo run, use `python util.py --demo --model gpt-5.4`.

## Cleanup

```bash
python util.py --clean
```
