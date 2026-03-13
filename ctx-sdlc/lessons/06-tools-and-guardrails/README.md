# Lesson 06 — Tools and Guardrails

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Hooks (PreToolUse/PostToolUse), MCP servers, and scripts that guard against unsafe operations.

## Setup

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

## What This Demonstrates

Hooks intercept Copilot tool calls at runtime to enforce guardrails:

| Hook File                   | Event       | Purpose                                             |
| --------------------------- | ----------- | --------------------------------------------------- |
| `file-protection.json`      | PreToolUse  | Blocks edits to protected files (.env, config, db)  |
| `post-save-format.json`     | PostToolUse | Auto-formats files after Copilot writes them        |
| `pre-commit-validate.json`  | PreToolUse  | Validates changes before commit operations          |

Plus an **MCP server** configuration (`mcp.json`) for extending tool capabilities.

## Context Files

| Path                                        | Purpose                          |
| ------------------------------------------- | -------------------------------- |
| `.github/hooks/file-protection.json`        | PreToolUse hook — blocks edits   |
| `.github/hooks/post-save-format.json`       | PostToolUse hook — auto-format   |
| `.github/hooks/pre-commit-validate.json`    | PreToolUse hook — pre-commit     |
| `.github/scripts/check_protected_files.py`  | File protection check script     |
| `.github/scripts/format_file.py`            | Post-save formatter script       |
| `.github/scripts/validate_commit.py`        | Commit validation script         |
| `.github/mcp.json`                          | MCP server configuration         |
| `docs/security-policy.md`                   | Security policy reference        |
| `docs/tool-trust-boundaries.md`             | Tool trust boundary docs         |

## Cleanup

```bash
python util.py --clean
```
