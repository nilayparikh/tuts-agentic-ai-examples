# Lesson 07 — GitHub CLI Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup   # copies app, creates .env interactively
python util.py --run     # installs deps + starts backend & frontend
```

### 2. Test CLI context access

```bash
gh copilot explain "What coding conventions does this project follow?"
```

The CLI picks up `.github/copilot-instructions.md` — the universal baseline. It does NOT see `.github/instructions/api.instructions.md` or agents.

### 3. Compare with scoped instructions

```bash
gh copilot suggest "Add input validation to the notification preferences endpoint"
```

The suggestion follows project-level conventions but lacks API-specific rules (like audit-first writes) that the scoped `api.instructions.md` would provide in VS Code.

### 4. Review the portability matrix

```bash
cat docs/portability-matrix.md
```

This documents which context files work on which surfaces — essential for teams using multiple IDEs.

### 5. Cleanup

```bash
python util.py --clean
```
