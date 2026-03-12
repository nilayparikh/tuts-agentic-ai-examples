# Lesson 03 — Instruction Architecture — Setup

## Prerequisites

- Node.js 20+
- Python 3.11+
- GitHub Copilot CLI (`copilot` v1.0.4+)

## Workspace Setup

```bash
python default.py --clean
cd src && npm install
```

This copies the **complex** template (Loan Workbench) into `src/` and removes
any previous workspace artifacts.

## Context Files

| Path                                                  | Purpose                                   |
| ----------------------------------------------------- | ----------------------------------------- |
| `.github/copilot-instructions.md`                     | Global project identity                   |
| `.github/instructions/backend.instructions.md`        | Scoped to `src/backend/src/**/*.ts`       |
| `.github/instructions/business-rules.instructions.md` | Scoped to `src/backend/src/rules/**`      |
| `.github/instructions/security.instructions.md`       | Scoped to `src/backend/src/middleware/**` |
| `.github/instructions/testing.instructions.md`        | Scoped to `src/backend/tests/**`          |
| `docs/architecture.md`                                | System shape, instruction scoping table   |

## Validation

```bash
# Run all scenarios
python validate.py --all

# Run a specific scenario
python validate.py --scenario route-layer
python validate.py --scenario business-rule
python validate.py --scenario test-layer
```

### Scenarios

| Key             | Description                                                    |
| --------------- | -------------------------------------------------------------- |
| `route-layer`   | Adds a DELETE endpoint — tests route-layer instruction scoping |
| `business-rule` | Adds a NY restriction — tests business-rule layer scoping      |
| `test-layer`    | Adds a test — tests testing instruction scoping                |

Outputs are written to `output/`.
