# Lesson 02 — VS Code Copilot Chat Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Behavior only — no docs attached

Open Agent mode and ask:

```
Add a route for preference management. Users save notification channel preferences (email, SMS) per event type.
```

Observe: Style is correct (ESM, const, async) but business logic is in the route handler instead of src/rules/.

### 3. Knowledge only — attach docs explicitly

```
#file:docs/architecture.md

Add a route for preference management. Users save notification channel preferences (email, SMS) per event type.
```

Observe: Architecture is correct (rules in rules/, audit-first) but style rules may be ignored.

### 4. Both halves together

With .github/ and docs/ in the workspace, send the same prompt. The generated code should be both architecturally correct AND style-consistent.

### 5. Cleanup

```bash
python util.py --clean
```
