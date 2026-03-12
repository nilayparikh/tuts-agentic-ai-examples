# Lesson 05 — Implementation Workflows — Setup

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

| Path                                   | Purpose                                                |
| -------------------------------------- | ------------------------------------------------------ |
| `.github/copilot-instructions.md`      | Project identity                                       |
| `.github/agents/*.agent.md`            | Role-separated agent definitions                       |
| `docs/architecture.md`                 | System shape                                           |
| `docs/implementation-playbook.md`      | Role boundaries, coding conventions, handoff protocols |
| `specs/non-functional-requirements.md` | NFR requirements                                       |

## Validation

```bash
# Run all scenarios
python validate.py --all

# Run a specific scenario
python validate.py --scenario single-agent
python validate.py --scenario tdd-first
python validate.py --scenario implementer
```

### Scenarios

| Key            | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| `single-agent` | No role separation — single agent does everything              |
| `tdd-first`    | Tester role writes failing tests first (references rules file) |
| `implementer`  | Implementer makes failing tests pass (references playbook)     |

Outputs are written to `output/`.
