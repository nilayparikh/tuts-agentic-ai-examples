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

This lesson should demonstrate context-maintenance analysis quality, not script execution.

For this example, the intended outcome is:

- inspect the maintenance scripts, clean example, drifted example, and schedule in a read-only workflow
- discover the relevant maintenance artifacts instead of relying on a hardcoded read list
- explain which kinds of context drift the lesson is trying to catch
- identify the most dangerous drift patterns without editing files
- map each major drift risk back to the specific artifact or artifact pair that shows it

## Copilot CLI Workflow

Use the CLI to reason about drift and maintenance:

```bash
copilot -p "Inspect the lesson's context-maintenance artifacts before answering. Discover the relevant project instructions, audit scripts, clean and drifted examples, and maintenance docs that exist here rather than assuming a fixed file list. Produce a read-only operating-model analysis covering drift types, the most dangerous clean-versus-drifted differences, one false positive, one hard negative, maintenance cadence recommendations, prioritized fixes, and map each major drift risk back to the specific artifact or artifact pair that shows it." --allow-all-tools --deny-tool=sql
```

Then compare the clean and drifted examples:

```bash
copilot -p "Compare .github/examples/clean/ and .github/examples/drifted/. Identify the most dangerous context drift issues." --allow-all-tools
```

Expected result:

- the CLI returns a source-grounded maintenance analysis without modifying files
- the analysis explains copy-paste drift, stale references, contradictory rules, over-specification, and under-specification
- the analysis ties its main conclusions back to the exact clean, drifted, or script artifacts that demonstrate them
- the analysis distinguishes static drift detection from the richer workflow you would get by actually running the scripts in an editor-assisted flow

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
