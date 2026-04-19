# Lesson 04 — Planning Workflow Example

This document defines the concrete example used in Lesson 04.

## Objective

Show that a planning workflow can turn a visible feature request into a grounded, written implementation plan. The CLI writes the plan to `docs/notification-preferences-plan.md` so the output is assessable as a code change.

## Expected Output Shape

The demo must produce a new file `docs/notification-preferences-plan.md` containing:

1. Summary
2. Source-backed confirmed requirements with FR/SC/ADR/NFR references
3. Open questions with file references
4. Inferred implementation choices separated from confirmed requirements
5. Constraints and special conditions
6. Numbered tasks with acceptance criteria and source references
7. Validation steps
8. Risks and dependencies

## Expected Change Artifacts

Assessment compares the actual `demo.patch` and `changed-files.json` against:

- `.output/change/expected-files.json` — expected added/modified/deleted files
- `.output/change/expected-patterns.json` — regex patterns that must appear in the patch

## Required Constraints

1. The plan must be written to `docs/notification-preferences-plan.md` as a real file change.
2. The plan must cite product spec, NFR, ADR, or special-condition references where relevant.
3. The plan must separate confirmed requirements from inferred implementation choices.
4. The plan must explicitly call out delegated-session behavior, LEGAL-218, mandatory-event delivery, fail-closed audit semantics, and degraded-mode fallback.
5. The plan must identify both backend and frontend impact surfaces.
6. The plan must surface at least one false positive and one hard negative pattern from the provided specs.
7. Do not run shell commands during the assessment run.
8. If lesson artifacts overlap or conflict, the plan must identify the canonical source and explain why.
9. Do not use SQL during the assessment run.

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
- produce a written plan file that the comparison tooling can verify against expected patterns
