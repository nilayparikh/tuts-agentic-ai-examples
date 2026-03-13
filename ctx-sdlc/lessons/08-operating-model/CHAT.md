# Lesson 08 — VS Code Copilot Chat Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Audit context quality

In Agent mode, ask:

```
Run the context audit script at .github/scripts/audit_context.py and summarize the findings. What context files are missing or incomplete?
```

**Observe:** Copilot runs the audit script and interprets the output, identifying gaps in the context layer.

### 3. Find stale references

```
Run .github/scripts/detect_stale_refs.py and list all broken file references in .github/ files.
```

**Observe:** The script finds instructions that point to files that have been moved or deleted.

### 4. Compare clean vs drifted examples

```
Compare .github/examples/clean/copilot-instructions.md with .github/examples/drifted/copilot-instructions.md. What has drifted and how should it be fixed?
```

**Observe:** Copilot identifies the differences and suggests specific fixes to bring the drifted version back in sync.

### 5. Create a maintenance PR

```
Based on the audit findings, create a plan to update the stale context files. List each file that needs changes and what should be updated.
```

### 6. Cleanup

```bash
python util.py --clean
```
