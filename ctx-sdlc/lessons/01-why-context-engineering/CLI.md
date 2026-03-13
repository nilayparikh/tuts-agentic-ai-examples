# Lesson 01 — GitHub CLI Guide

## Prerequisites

- GitHub CLI installed (`gh`)
- GitHub Copilot CLI extension (`gh copilot`)

## Steps

### 1. Set up the workspace

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

### 2. Without context — baseline prompt

Run from outside the lesson directory (no `.github/` visible):

```bash
gh copilot suggest "Add a route handler for deleting loan applications with proper error handling"
```

The suggestion will miss domain rules (audit-first, state machine, role checks).

### 3. With context — same prompt in the project root

```bash
cd <lesson-root>
gh copilot suggest "Add a route handler for deleting loan applications with proper error handling"
```

The CLI reads `.github/copilot-instructions.md` automatically. The suggestion should now include audit patterns, ESM imports, and role checks.

### 4. Explain existing code

```bash
gh copilot explain "src/backend/src/middleware/auth.ts"
```

### 5. Cleanup

```bash
python util.py --clean
```
