# Lesson 05 — VS Code Copilot Chat Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Implement with the implementer agent

Switch to `@implementer` and ask:

```
Implement the notification preferences feature from specs/non-functional-requirements.md. Create the route, business rules, and service layer.
```

**Observe:** The implementer agent can edit files, run terminal commands, and search the codebase. It follows the implementation playbook from docs/.

### 3. Test with the tester agent

Switch to `@tester` and ask:

```
Write tests for the notification preferences feature. Follow TDD — write failing tests first, then verify they pass after implementation.
```

**Observe:** The tester agent uses `runTests` and `testFailure` tools. It can see test output and iterate.

### 4. Review with the reviewer agent

Switch to `@reviewer` and ask:

```
Review the notification preferences implementation. Check for security issues, missing audit entries, and NFR compliance.
```

**Observe:** The reviewer agent is read-only — it searches the codebase and checks problems but cannot edit files. It produces a structured review.

### 5. Run the implement-feature prompt

Run the **implement-feature** prompt file (Ctrl+Shift+P → "Run Prompt File"). This orchestrates the full workflow using the implementer agent.

### 6. Cleanup

```bash
python util.py --clean
```
