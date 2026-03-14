# Lesson 04 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the relevant docs/, specs/, and existing source surfaces for notification preferences in this lesson before answering. Discover the architecture, ADR, product, and NFR context you need rather than assuming a fixed file list. Produce a structured implementation plan and save it to docs/notification-preferences-plan.md. The plan must include: summary, source-backed confirmed requirements with references to FR/SC/ADR/NFR identifiers, open questions with file references, inferred implementation choices separated from confirmed requirements, constraints and special conditions, numbered tasks with acceptance criteria and source references, validation steps, and risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative. If the sources overlap or conflict, identify the canonical source for the plan and explain why. Do not run shell commands and do not use SQL.
```

The assessment run uses the model from `lessons/_common/assessment-config.json`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and discovered context?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected file: `docs/notification-preferences-plan.md` (added)
- `.output/change/expected-patterns.json` — required patterns in patch: delegated-session, LEGAL-218, mandatory-event, fail-closed audit, false positive, hard negative, acceptance criteria

The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report.

## Assessment Criteria

| Criterion | Source |
| --- | --- |
| Plan file created at correct path | `expected-files.json` |
| Delegated-session callout present | `expected-patterns.json` |
| LEGAL-218 restriction referenced | `expected-patterns.json` |
| Mandatory-event delivery covered | `expected-patterns.json` |
| Fail-closed audit behavior called out | `expected-patterns.json` |
| False positive identified | `expected-patterns.json` |
| Hard negative identified | `expected-patterns.json` |
| Acceptance criteria present | `expected-patterns.json` |
| No shell commands executed | Prompt constraint |
| No SQL tools used | Prompt constraint |

## Captured Result

Pending re-run with the updated implementation-oriented prompt. Previous assessment was for a read-only planning demo that has been replaced.

## Verdict

Pending re-run.