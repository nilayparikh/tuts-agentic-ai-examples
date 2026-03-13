# Lesson 01 — VS Code Copilot Chat Guide

## Prerequisites

- VS Code with GitHub Copilot extension
- Open this lesson folder as a workspace (or in a multi-root workspace)

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Without context — ask Copilot with no project files

Open Agent mode (Ctrl+Shift+I) and send:

```
Add a route handler for deleting loan applications. Include proper error handling and validation.
```

Observe: The generated code is generic — it uses `require()`, `var`, `console.log()`, and misses audit trail, role checks, and state machine guards.

### 3. With context — same prompt with project context active

Ensure `.github/copilot-instructions.md` and `docs/architecture.md` are in the workspace. Send the same prompt:

```
Add a route handler for deleting loan applications. Include proper error handling and validation.
```

Observe: The code now uses ESM imports, `const`, structured logging, audit-first patterns, and role middleware.

### 4. Verify context is loaded

Ask in chat:

```
What are the coding conventions for this project?
```

Copilot should reference the instructions file and architecture docs.

### 5. Cleanup

```bash
python util.py --clean
```
