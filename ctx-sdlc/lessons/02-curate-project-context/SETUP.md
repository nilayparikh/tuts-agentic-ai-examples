# Lesson 02 — Curate Project Context — Setup

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

| Path                              | Purpose                                                               |
| --------------------------------- | --------------------------------------------------------------------- |
| `.github/copilot-instructions.md` | Notification preferences, UPSERT semantics, compliance-reviewer rules |
| `docs/architecture.md`            | System shape, domain model, key constraints                           |
| `docs/api-conventions.md`         | Endpoint patterns, error handling, auth model                         |

## Validation

```bash
# Run all scenarios
python validate.py --all

# Run a specific scenario
python validate.py --scenario no-context
python validate.py --scenario behavior-only
python validate.py --scenario both-halves
```

### Scenarios

| Key             | Description                                              |
| --------------- | -------------------------------------------------------- |
| `no-context`    | Baseline — no custom instructions                        |
| `behavior-only` | `.github/` only (copilot-instructions), no docs attached |
| `both-halves`   | `.github/` + explicit `#file:docs/` references in prompt |

Outputs are written to `output/`.
