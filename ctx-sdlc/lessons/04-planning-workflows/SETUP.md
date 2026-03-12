# Lesson 04 — Planning Workflows — Setup

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

| Path                                             | Purpose                                              |
| ------------------------------------------------ | ---------------------------------------------------- |
| `.github/copilot-instructions.md`                | Project identity, state machine, queue broker        |
| `docs/architecture.md`                           | System shape diagram, queue contracts, state machine |
| `docs/adr/ADR-003-frontend-state.md`             | Architecture Decision Record                         |
| `specs/product-spec-notification-preferences.md` | Product specification                                |
| `specs/non-functional-requirements.md`           | NFR requirements                                     |
| `feature-request.md`                             | Feature request template                             |
| `bug-report.md`                                  | Bug report template                                  |

## Validation

```bash
# Run all scenarios
python validate.py --all

# Run a specific scenario
python validate.py --scenario shallow
python validate.py --scenario deep
python validate.py --scenario no-context
```

### Scenarios

| Key          | Description                                                           |
| ------------ | --------------------------------------------------------------------- |
| `shallow`    | Planning with custom instructions only — no specs attached            |
| `deep`       | Planning with specs, NFRs, architecture, and feature request attached |
| `no-context` | Baseline — no custom instructions at all                              |

Outputs are written to `output/`.
