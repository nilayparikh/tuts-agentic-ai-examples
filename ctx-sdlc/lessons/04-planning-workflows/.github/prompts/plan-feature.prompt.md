---
name: "plan-feature"
description: "Decompose a Loan Workbench feature request into implementation tasks using specs, NFRs, and architecture docs"
agent: "planner"
tools:
  - read_file
  - grep_search
  - semantic_search
argument-hint: "Describe the feature in one sentence"
---

# Plan Feature

Feature request: ${input:feature:Describe the requested feature}

Current file: ${file}
Current selection: ${selection}

## Before Planning — Read These Documents

1. Read [architecture](../docs/architecture.md)
2. Read [ADR-003](../docs/adr/ADR-003-frontend-state.md)
3. Read [product spec](../specs/product-spec-notification-preferences.md)
4. Read [NFRs](../specs/non-functional-requirements.md)
5. Search for related workflow, service, and rule files in `src/`

## Planning Requirements

- Separate **product requirements** (from specs/) from **inferred implementation choices**.
- Call out role-based rules, state-based exceptions, degraded-mode behavior, and audit impacts.
- If the feature appears simple but the spec introduces hidden constraints, **make that explicit**.
- Identify which acceptance criteria come from NFRs versus functional requirements.
- Flag any false-positive scenarios (things that look wrong but are correct behavior).
- Flag any hard-negative scenarios (things that look correct but violate a rule).

## Output Format

1. **Summary** — one paragraph describing the feature and its complexity.
2. **Open questions** — unresolved ambiguities with references to specific spec sections.
3. **Constraints and special conditions** — from specs/NFRs that affect the plan.
4. **Numbered tasks with acceptance criteria** — each task references its source (FR, NFR, ADR, SC).
5. **Validation steps** — how to verify correctness, including edge cases.
6. **Risks and dependencies** — what could go wrong, what blocks what.
