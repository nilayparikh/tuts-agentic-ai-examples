# Lesson 01 — Why Context Engineering — Setup

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

| Path                              | Purpose                                     |
| --------------------------------- | ------------------------------------------- |
| `.github/copilot-instructions.md` | Global project identity and rules           |
| `docs/architecture.md`            | System shape, domain model, key constraints |

## Validation

```bash
# Run all scenarios
python validate.py --all

# Run a specific scenario
python validate.py --scenario without-context
python validate.py --scenario with-context
```

### Scenarios

| Key               | Description                                                          |
| ----------------- | -------------------------------------------------------------------- |
| `without-context` | Runs Copilot with `--no-custom-instructions` — no context files read |
| `with-context`    | Runs Copilot normally — reads `.github/` + `docs/`                   |

Outputs are written to `output/`.
