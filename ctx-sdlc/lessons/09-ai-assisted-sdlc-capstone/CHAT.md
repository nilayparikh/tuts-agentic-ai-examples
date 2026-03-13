# Lesson 09 — VS Code Copilot Chat Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Plan — investigate the architecture

Open Agent mode:

```
I need to add a user dashboard that shows notification delivery history. Review docs/architecture.md and plan the implementation across both backend and frontend.
```

**Observe:** With the full context layer active, Copilot produces an architecture-aware plan that respects both API and frontend conventions.

### 3. Implement — backend route

Open `src/backend/src/routes/` and ask:

```
Create a GET /dashboard/history endpoint that returns paginated delivery logs for the current user.
```

**Observe:** `api.instructions.md` activates — the route follows audit-first patterns, uses middleware for auth, and delegates to a service layer.

### 4. Implement — frontend page

Open `src/frontend/src/pages/` and ask:

```
Create a dashboard page that calls the /dashboard/history API and renders a paginated table.
```

**Observe:** `frontend.instructions.md` activates — the component follows frontend conventions (accessibility, loading states, error handling).

### 5. Review the full implementation

```
Review the dashboard feature implementation across backend and frontend. Check for consistency with project conventions, missing error handling, and security issues.
```

### 6. Reflect

This capstone combines all prior lessons:
- Layered instructions scoped the right guidance to each file
- Docs provided architectural knowledge
- Hooks could guard against editing protected files
- The same workflow degrades gracefully to CLI (universal baseline)

### 7. Cleanup

```bash
python util.py --clean
```
