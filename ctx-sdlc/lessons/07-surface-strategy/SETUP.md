# Lesson 07 — Surface Strategy — Setup

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

| Path                                       | Purpose                               |
| ------------------------------------------ | ------------------------------------- |
| `.github/copilot-instructions.md`          | 4-layer architecture, backend paths   |
| `.github/instructions/api.instructions.md` | Scoped to `src/backend/src/routes/**` |
| `cli/`                                     | CLI-specific context files            |
| `portability-matrix.md`                    | Surface portability comparison        |

## Validation

```bash
# Run all scenarios
python validate.py --all

# Run a specific scenario
python validate.py --scenario full-context
python validate.py --scenario foundation-only
python validate.py --scenario no-context
```

### Scenarios

| Key               | Description                                     |
| ----------------- | ----------------------------------------------- |
| `full-context`    | Full context (VS Code equivalent) — heavy model |
| `foundation-only` | Foundation only (CLI equivalent) — light model  |
| `no-context`      | Baseline — no custom instructions               |

Outputs are written to `output/`.
