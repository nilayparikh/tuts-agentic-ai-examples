# Lesson 06 — Tools and Guardrails

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Hooks, MCP configuration, and runtime scripts that guard against unsafe operations.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Hooks intercept Copilot tool calls at runtime to enforce guardrails.

| Hook File | Event | Purpose |
| --- | --- | --- |
| `file-protection.json` | PreToolUse | Blocks edits to protected files |
| `post-save-format.json` | PostToolUse | Auto-formats files after writes |
| `pre-commit-validate.json` | PreToolUse | Validates changes before commit operations |

This lesson also includes MCP configuration for extending tool capabilities.

## Context Files

| Path | Purpose |
| --- | --- |
| `.github/hooks/file-protection.json` | PreToolUse hook |
| `.github/hooks/post-save-format.json` | PostToolUse hook |
| `.github/hooks/pre-commit-validate.json` | PreToolUse hook |
| `.github/scripts/check_protected_files.py` | File protection script |
| `.github/scripts/format_file.py` | Formatter script |
| `.github/scripts/validate_commit.py` | Commit validation script |
| `.github/mcp.json` | MCP server configuration |
| `docs/security-policy.md` | Security policy |
| `docs/tool-trust-boundaries.md` | Tool trust boundaries |

## Copilot CLI Workflow

The CLI does not execute VS Code hooks, so this lesson is mostly about understanding the guardrails rather than triggering them directly.

Inspect the files with:

```bash
copilot -p "Explain how the guardrails in .github/hooks/ and .github/scripts/ work together to protect this repository." --allow-all-tools
```

Expected outcome: the CLI can explain the policy, but runtime hook behavior is primarily a VS Code demonstration.

## VS Code Chat Workflow

Ask Copilot to perform edits that should trigger hooks.

Examples:

- ask it to edit a protected file and observe the block
- ask it to create or update a normal source file and observe post-save formatting
- inspect the GitHub Copilot output logs to confirm hook execution

Expected result: you can see the operational difference between static instructions and runtime guardrails.

## Cleanup

```bash
python util.py --clean
```
