# Lesson 09 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the capstone lesson's project instructions, backend and frontend scoped instructions, architecture doc, and the relevant backend/frontend notification-preference surfaces you discover before answering. Do not assume a fixed file list beyond those starting points. Then implement a notification preference event-channel validator as a cross-stack hardening slice: 1. Create a pure validation rule module at backend/src/rules/preference-event-channel-validator.ts that validates event-channel combinations are allowed, enforcing that mandatory events cannot have all channels disabled, and respecting LEGAL-218 California SMS restrictions from existing rules. 2. Create unit tests at backend/tests/unit/preference-event-channel-validator.test.ts covering valid combinations, mandatory-event violations, and LEGAL-218 false positive and hard negative cases. 3. Wire the validator import into the existing notification preference write route in backend/src/routes/notifications.ts. Follow the repository conventions you discover. Apply the changes directly in code. Do not run npm install, npm test, or any shell commands. Do not use SQL.
```

The assessment run uses the model from `lessons/_common/assessment-config.json`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's cross-stack conventions and discovered context?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `backend/src/rules/preference-event-channel-validator.ts` (added), `backend/tests/unit/preference-event-channel-validator.test.ts` (added), `backend/src/routes/notifications.ts` (modified)
- `.output/change/expected-patterns.json` — required patterns in patch: event-channel, mandatory, LEGAL-218, import validator, tests, false positive/hard negative

The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report.

## Assessment Criteria

| Criterion | Source |
| --- | --- |
| Validator module created | `expected-files.json` |
| Unit tests created | `expected-files.json` |
| Route wired with validator import | `expected-files.json` |
| Event-channel validation present | `expected-patterns.json` |
| Mandatory-event enforcement present | `expected-patterns.json` |
| LEGAL-218 restriction referenced | `expected-patterns.json` |
| Validator import in route | `expected-patterns.json` |
| Test coverage with false positive/hard negative | `expected-patterns.json` |
| No shell commands executed | Prompt constraint |
| No SQL tools used | Prompt constraint |

## Captured Result

Pending re-run with the updated implementation-oriented prompt. Previous assessment was for a read-only capstone analysis demo that has been replaced.

## Verdict

Pending re-run.