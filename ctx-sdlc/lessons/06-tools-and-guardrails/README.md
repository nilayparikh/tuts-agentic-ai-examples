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

| Hook File                  | Event       | Purpose                                    |
| -------------------------- | ----------- | ------------------------------------------ |
| `file-protection.json`     | PreToolUse  | Blocks edits to protected files            |
| `post-save-format.json`    | PostToolUse | Auto-formats files after writes            |
| `pre-commit-validate.json` | PreToolUse  | Validates changes before commit operations |

This lesson also includes MCP configuration for extending tool capabilities.

## Example Goal

This lesson should demonstrate guardrail analysis quality, not hook execution.

For this example, the intended outcome is:

- inspect the hook, MCP, and policy files in a read-only workflow
- identify mismatches between documented policy and actual enforcement
- call out what the CLI can analyze statically versus what only VS Code runtime hooks can demonstrate

## Context Files

| Path                                       | Purpose                                                   |
| ------------------------------------------ | --------------------------------------------------------- |
| `.github/hooks/file-protection.json`       | PreToolUse hook                                           |
| `.github/hooks/post-save-format.json`      | PostToolUse hook                                          |
| `.github/hooks/pre-commit-validate.json`   | PreToolUse hook                                           |
| `.github/scripts/check_protected_files.py` | File protection script                                    |
| `.github/scripts/format_file.py`           | Formatter script                                          |
| `.github/scripts/validate_commit.py`       | Commit validation script                                  |
| `.github/mcp.json`                         | MCP server configuration                                  |
| `docs/security-policy.md`                  | Security policy                                           |
| `docs/tool-trust-boundaries.md`            | Tool trust boundaries                                     |
| `docs/guardrail-audit-example.md`          | Concrete lesson-06 demo target and assessment constraints |

## Copilot CLI Workflow

The CLI does not execute VS Code hooks, so this lesson is mostly about understanding the guardrails rather than triggering them directly.

Inspect the files with:

```bash
copilot -p "Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Produce a read-only guardrail audit that names mismatches between docs and enforcement, hard negatives, false positives, prioritized fixes, residual risks, what the CLI cannot prove because VS Code hooks do not run here, and which artifact should be treated as canonical when policy and enforcement disagree." --allow-all-tools --deny-tool=sql
```

Expected outcome:

- the CLI returns a source-grounded audit without modifying files
- the audit spots real inconsistencies between policy docs and hook/script enforcement
- the audit explains which artifact should win when the documented policy and the enforced script behavior disagree
- the audit clearly distinguishes static config review from runtime hook behavior that only VS Code can demonstrate

## VS Code Chat Workflow

Ask Copilot to perform edits that should trigger hooks.

Examples:

- ask it to edit a protected file and observe the block
- ask it to create or update a normal source file and observe post-save formatting
- inspect the GitHub Copilot output logs to confirm hook execution

Expected result: you can see the operational difference between static instructions and runtime guardrails.

For the captured demo run, use `python util.py --demo --model gpt-5.4`.

## Cleanup

```bash
python util.py --clean
```
