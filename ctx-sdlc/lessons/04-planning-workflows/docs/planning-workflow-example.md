# Lesson 04 — Planning Workflow Example

This document defines the concrete example used in Lesson 04.

## Objective

Show that a planning workflow can turn a visible feature request into a grounded implementation plan without modifying code.

## Expected Output Shape

The preferred output for this lesson is a structured plan with:

1. Summary
2. Open questions with source references
3. Constraints and special conditions
4. Numbered tasks with acceptance criteria and source references
5. Validation steps
6. Risks and dependencies

## Required Constraints

1. The workflow must remain read-only. No code edits should be proposed as already completed.
2. The plan must cite product spec, NFR, ADR, or special-condition references where relevant.
3. The plan must separate confirmed requirements from inferred implementation choices.
4. The plan must explicitly call out delegated-session behavior, LEGAL-218, mandatory-event delivery, fail-closed audit semantics, and degraded-mode fallback.
5. The plan must identify both backend and frontend impact surfaces.
6. The plan must surface at least one false positive and one hard negative pattern from the provided specs.
7. Do not run shell commands during the assessment run.
8. If lesson artifacts overlap or conflict, the plan must identify the canonical source and explain why.
9. Do not use SQL, task/todo write tools, or any other write-capable tools during the assessment run.

## Concrete Scenario

Use the notification preferences feature request and supporting docs to produce a plan that is deeper than "add a settings page and API route".

Good output should identify hidden complexity around:

- delegated sessions
- California decline SMS restrictions
- optimistic UI rollback behavior
- audit fail-closed semantics
- release-flag rollout and observability

## What Good Output Looks Like

Good output will usually:

- cite FR-2, FR-4, FR-5, FR-6, SC-2, ADR-003, and relevant NFRs
- identify affected route, rule, service, UI, state, and audit surfaces
- list validation steps that cover false-positive and hard-negative cases
- stay read-only and avoid pretending the implementation has already been done
- avoid any side-effecting tool usage such as SQL inserts or task/todo writes
