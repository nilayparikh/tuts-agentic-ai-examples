# Lesson 03 — GitHub CLI Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Ask about backend patterns

```bash
gh copilot suggest "Add a DELETE /notifications/preferences/:event endpoint that resets to defaults"
```

The CLI picks up `.github/copilot-instructions.md` but cannot auto-scope by file path — all rules are merged.

### 3. Compare with scoped context

In VS Code, the same prompt with `src/routes/notifications.ts` open activates `backend.instructions.md` automatically, producing route-layer code (audit-first, middleware-based auth).

The CLI lacks this file-scoping, which is why layered instructions shine in the editor.

### 4. Cleanup

```bash
python util.py --clean
```
