# Lesson 08 — GitHub CLI Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Run the context audit

```bash
python .github/scripts/audit_context.py
```

The script checks `.github/` for completeness: are instructions present, do file references resolve, are applyTo patterns valid?

### 3. Detect stale references

```bash
python .github/scripts/detect_stale_refs.py
```

This finds instructions that reference files or paths that no longer exist in the codebase.

### 4. Compare clean vs drifted

```bash
diff .github/examples/clean/copilot-instructions.md .github/examples/drifted/copilot-instructions.md
```

Identify what drifted: outdated file paths, removed feature references, stale tool configurations.

### 5. Cleanup

```bash
python util.py --clean
```
