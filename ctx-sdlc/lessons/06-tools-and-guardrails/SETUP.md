# Lesson 06 — Tools and Guardrails — Setup

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

| Path                              | Purpose                                       |
| --------------------------------- | --------------------------------------------- |
| `.github/copilot-instructions.md` | Project identity, SQLite, backend paths       |
| `.github/mcp.json`                | MCP server config (sqlite, filesystem scopes) |
| `docs/security-policy.md`         | Protected files table, audit requirements     |
| `docs/tool-trust-boundaries.md`   | Trust levels, server inventory, agent matrix  |
| `scripts/`                        | Audit and hook scripts                        |

## Validation

```bash
# Run all scenarios
python validate.py --all

# Run a specific scenario
python validate.py --scenario read-only-mcp
python validate.py --scenario write-blocked
python validate.py --scenario file-protection
```

### Scenarios

| Key               | Description                                               |
| ----------------- | --------------------------------------------------------- |
| `read-only-mcp`   | MCP read-only query — should succeed                      |
| `write-blocked`   | MCP write attempt — should be blocked by trust boundaries |
| `file-protection` | Attempts to modify a protected file — tests guardrails    |

Outputs are written to `output/`.
