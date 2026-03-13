# Lesson 07 — VS Code Copilot Chat Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Agent mode — full context

Switch to Agent mode and ask:

```
Review the notification preferences endpoint for security issues and API convention compliance.
```

**Observe:** In Agent mode, the reviewer agent activates with full access to codebase, problems, and usages tools. It references both `copilot-instructions.md` and `api.instructions.md`.

### 3. Inline completions — scoped context

Open `src/backend/src/routes/notifications.ts` and start typing a new route handler. Inline completions use `api.instructions.md` (matched by applyTo pattern) plus the global instructions.

### 4. Compare surfaces

Ask the same question in Ask mode (no tools):

```
Review the notification preferences endpoint for security issues.
```

**Observe:** Without tool access, Ask mode relies only on the files you explicitly attach. The quality of the review depends on what context you provide.

### 5. Check the portability matrix

Open `docs/portability-matrix.md` to see which context files work on which surfaces. Design your instructions to degrade gracefully — the universal baseline in `copilot-instructions.md` should be useful even in the most limited surface.

### 6. Cleanup

```bash
python util.py --clean
```
