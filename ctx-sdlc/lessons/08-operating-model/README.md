# Lesson 08 — Operating Model

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Maintaining context over time — audit scripts, drift detection, clean vs drifted examples.

## Setup

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

## What This Demonstrates

Context files drift as codebases evolve. This lesson shows how to detect and fix staleness:

| Tool                        | Purpose                                      |
| --------------------------- | -------------------------------------------- |
| `scripts/audit_context.py`  | Audits .github/ for completeness and quality |
| `scripts/detect_stale_refs.py`| Finds broken file references in instructions|
| `examples/clean/`           | A well-maintained .github/ (reference)       |
| `examples/drifted/`         | A stale .github/ with issues to find         |

## Context Files

| Path                                          | Purpose                           |
| --------------------------------------------- | --------------------------------- |
| `.github/copilot-instructions.md`             | Project-level instructions        |
| `.github/scripts/audit_context.py`            | Context audit script              |
| `.github/scripts/detect_stale_refs.py`        | Stale reference detector          |
| `.github/examples/clean/copilot-instructions.md`| Clean reference example         |
| `.github/examples/drifted/copilot-instructions.md`| Drifted example to diagnose   |
| `docs/maintenance-schedule.md`                | Maintenance cadence docs          |

## Cleanup

```bash
python util.py --clean
```
