# Lesson 09 — GitHub CLI Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

### 2. Plan a full-stack feature

```bash
gh copilot suggest "Plan the implementation of a user dashboard that shows notification delivery history. The backend needs a new route and the frontend needs a new page."
```

The CLI uses `copilot-instructions.md` — the universal baseline. For full SDLC context (agents, layered instructions), use VS Code.

### 3. Generate backend code

```bash
gh copilot suggest "Create a GET /dashboard/history endpoint that returns notification delivery logs for the current user, paginated with cursor-based pagination."
```

### 4. Generate frontend code

```bash
gh copilot suggest "Create a dashboard page component that fetches and displays notification history with pagination controls."
```

### 5. Cleanup

```bash
python util.py --clean
```
