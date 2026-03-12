---
mode: "ask"
description: "Diagnose and fix a bug using the systematic debug workflow."
---

# Fix Bug — Debugging Prompt

You are a senior developer debugging an issue in TaskFlow.

## Context

#file:docs/architecture.md
#file:.github/copilot-instructions.md

## Bug Report

**Bug**: {{ bug_description }}
**Expected behavior**: {{ expected }}
**Actual behavior**: {{ actual }}
**Steps to reproduce**: {{ steps }}

## Diagnostic Steps

Work through these in order:

### 1. Locate

- Which package is the bug in? (`web`, `api`, `shared`)
- Which layer? (component, hook, store, route, controller, service, model)
- Which specific file(s)?

### 2. Root Cause

- What is the actual cause (not just the symptom)?
- Is this a logic error, data error, state error, or race condition?
- Could this be caused by stale context or wrong assumptions?

### 3. Impact Assessment

- What other features could this affect?
- Could fixing it break anything else?
- Is there a data integrity concern?

### 4. Fix

- Show the exact code change needed
- Explain WHY the fix works
- Ensure the fix follows project conventions

### 5. Test

- Write a regression test for the fix
- Verify edge cases are covered
