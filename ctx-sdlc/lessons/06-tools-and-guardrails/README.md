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

### Available Hook Event Types

As of early 2026, VS Code Copilot exposes eight lifecycle events:

| Event            | Fires When                             | Common Use Cases                                |
| ---------------- | -------------------------------------- | ----------------------------------------------- |
| SessionStart     | A new chat or agent session begins     | Log session metadata, set environment variables |
| UserPromptSubmit | The user submits a message to chat     | Validate prompt content, inject boilerplate     |
| PreToolUse       | Before an agent invokes a tool         | Deny protected paths, block destructive cmds    |
| PostToolUse      | After a tool completes                 | Auto-format edited files, lint, schema checks   |
| PreCompact       | Before the context window is compacted | Preserve critical context entries               |
| SubagentStart    | Before a subagent is invoked           | Audit delegation, enforce allowed-agent lists   |
| SubagentStop     | After a subagent returns               | Log subagent output, validate handoff results   |
| Stop             | The agent session terminates           | Final validation, generate session summary      |

Hooks can also be **agent-scoped** using the `agents` list in the hook config, restricting a hook to fire only for specific agents.

This lesson also includes MCP configuration for extending tool capabilities.

## Example Goal

This lesson should demonstrate guardrail implementation, not just analysis.

For this example, the intended outcome is:

- inspect the hook, MCP, and policy files to discover existing guardrail patterns
- create a new import-validation guardrail (hook config + validation script) that follows those patterns
- the new guardrail must enforce barrel-file import conventions for TypeScript files
- the change is assessable via actual vs expected file and pattern comparison

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

Create a new guardrail:

```bash
copilot -p "Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
```

Expected outcome:

- the CLI creates `.github/hooks/import-validation.json` and `.github/scripts/validate_imports.py`
- the hook config uses `PreToolUse` event type following existing patterns
- the validation script enforces barrel-file imports
- `.output/change/demo.patch` contains the new files
- `.output/change/comparison.md` shows actual vs expected file and pattern match results

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
