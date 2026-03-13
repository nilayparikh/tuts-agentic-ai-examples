# Lesson 02 — GitHub CLI Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Ask about the project (no docs context)

```bash
gh copilot explain "What is the architecture of this project?"
```

Without docs/, the CLI only has .github/ — it describes conventions but cannot explain the system shape.

### 3. Ask to generate code

```bash
gh copilot suggest "Add a route handler for preference management with email and SMS channels"
```

.github/copilot-instructions.md provides behavioral guidance. docs/ files would add architectural knowledge, but CLI cannot auto-index them.

### 4. Cleanup

```bash
python util.py --clean
```
