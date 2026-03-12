# Lesson 08 — Operating Model — Setup

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

| Path                       | Purpose                            |
| -------------------------- | ---------------------------------- |
| `checklists/`              | Onboarding and review checklists   |
| `examples/`                | Drifted and clean context examples |
| `scripts/audit_context.py` | Context audit script               |

## Validation

```bash
# Run all scenarios
python validate.py --all

# Run a specific scenario
python validate.py --scenario audit-drifted
python validate.py --scenario stale-tech
python validate.py --scenario contradictory
```

### Scenarios

| Key             | Description                                               |
| --------------- | --------------------------------------------------------- |
| `audit-drifted` | Runs audit script against drifted context example         |
| `stale-tech`    | Tests Copilot's response with stale technology references |
| `contradictory` | Tests Copilot's response with contradictory rules         |

Outputs are written to `output/`.
