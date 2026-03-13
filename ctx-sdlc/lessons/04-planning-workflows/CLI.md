# Lesson 04 — GitHub CLI Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Investigate a bug

```bash
gh copilot explain "The notification preferences page shows stale data after saving. How does the frontend state management work and where might caching cause this?"
```

Without the planner agent, the CLI uses general context. Attach the bug report for better results:

```bash
cat specs/bug-report.md | gh copilot explain "Investigate this bug report. Where in the codebase would this issue originate?"
```

### 3. Plan a feature

```bash
cat specs/product-spec-notification-preferences.md | gh copilot explain "Plan the implementation of this feature. What files need to change?"
```

### 4. Cleanup

```bash
python util.py --clean
```
