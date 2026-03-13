# Lesson 06 — GitHub CLI Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Understand hook limitations in CLI

Hooks (PreToolUse, PostToolUse) are a VS Code Copilot feature — they do not run in the GitHub CLI. The CLI equivalent is pre-commit hooks and CI checks.

### 3. View the hook configuration

```bash
cat .github/hooks/file-protection.json
```

This hook intercepts `editFiles` and `createFile` tool calls and blocks changes to protected files like `.env`, `feature-flags.ts`, and `connection.ts`.

### 4. View the MCP configuration

```bash
cat .github/mcp.json
```

MCP servers extend Copilot with custom tools. In the CLI context, equivalent functionality would come from CLI extensions or scripts.

### 5. Cleanup

```bash
python util.py --clean
```
