# Lesson 04 — VS Code Copilot Chat Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Use the planner agent to investigate a bug

Switch to the **planner** agent (`@planner`) and ask:

```
Investigate the bug described in specs/bug-report.md. Trace the data flow from the frontend save action through the API to the database and identify where stale data could be served.
```

**Observe:** The planner agent searches the codebase (read-only), checks for problems, and finds usages — it never edits files. It produces a structured investigation report.

### 3. Use the plan-feature prompt

Run the prompt file: **plan-feature** (Ctrl+Shift+P → "Run Prompt File"):

```
Plan the implementation of notification preferences per the product spec.
```

**Observe:** The prompt file automatically attaches `docs/architecture.md`, `specs/product-spec-notification-preferences.md`, and `specs/non-functional-requirements.md` as context.

### 4. Triage an incident

Run the **triage-incident** prompt:

```
Users report 500 errors on the notification preferences page during peak hours.
```

**Observe:** The planner agent examines architecture docs, traces the request path, and generates an incident triage report with root cause hypothesis.

### 5. Cleanup

```bash
python util.py --clean
```
