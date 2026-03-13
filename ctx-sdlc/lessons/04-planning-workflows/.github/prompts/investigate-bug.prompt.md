---
name: investigate-bug
description: "Diagnose a Loan Workbench bug by cross-referencing code against specs, NFRs, and ADRs"
agent: planner
tools:
  - search/codebase
  - read/problems
  - search/usages
  - read/readFile
argument-hint: "Paste the bug description or failing scenario"
---

# Investigate Bug

Bug description: ${input:bug:Paste the bug report or failing behavior}

Current file: ${file}
Selected code: ${selection}

## Investigation Steps

1. Read [architecture](../../docs/architecture.md)
2. Read [ADR-003](../../docs/adr/ADR-003-frontend-state.md)
3. Read [product spec](../../specs/product-spec-notification-preferences.md)
4. Read [NFRs](../../specs/non-functional-requirements.md)
5. Search for the affected routes, services, rules, and tests in `app/`
6. Check whether the issue conflicts with ADR guidance, product rules, or NFRs

## Analysis Requirements

- Determine whether the reported behavior is a **real bug**, a **false positive**
  (correct behavior that looks wrong), or a **hard negative** (forbidden behavior
  that looks normal).
- Trace the issue through middleware → route → service → rules → store.
- Check whether the defect involves overlapping constraints (e.g. delegated session
  - state restriction + optimistic UI).

## Output Format

- **Classification**: Bug / False positive / Hard negative
- **Root cause**: What specifically is wrong and where in the code.
- **Evidence**: File paths, line-level references, spec section citations.
- **Fix options**: Ranked by scope and risk.
- **Spec or NFR conflicts**: Which requirements are violated or at risk.
- **Edge cases to retest**: Related scenarios that might have the same root cause.
- **Validation approach**: How to confirm the fix works without regressions.
