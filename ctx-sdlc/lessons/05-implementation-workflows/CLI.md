# Lesson 05 — GitHub CLI Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

### 2. Ask for implementation guidance

```bash
gh copilot suggest "Implement a notification preferences API endpoint. Users can set per-event channel preferences (email, SMS). Follow TDD."
```

The CLI does not support custom agents, so it uses the default context. Compare this with the agent-based workflow in VS Code.

### 3. Ask for a code review

```bash
gh copilot explain "Review this code for security issues, missing error handling, and adherence to audit-first write patterns."
```

### 4. Cleanup

```bash
python util.py --clean
```
