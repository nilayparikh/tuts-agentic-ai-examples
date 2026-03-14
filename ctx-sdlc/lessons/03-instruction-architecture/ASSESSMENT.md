# Lesson 03 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Create a pure business-rule module at src/backend/src/rules/notification-channel-rules.ts and matching tests at src/backend/tests/unit/notification-channel-rules.test.ts. The rule should validate when disabling a notification channel is allowed for mandatory events, including the California decline LEGAL-218 restriction. Follow the repository conventions you discover. Reuse existing mandatory-event knowledge from src/backend/src/rules/mandatory-events.ts or explicit function inputs; do not create a second hardcoded mandatory-events list or helper. Return structured results with human-readable reasons, include top-of-module false-positive and hard-negative comments, and add tests for happy path, boundary, false positive, and hard negative scenarios. Apply the change directly in code instead of only describing it. Do not run npm install, npm test, or any shell commands. Inspect and edit files only.
```

The assessment run used the shared default model from `lessons/_common/assessment-config.json`:

- `claude-haiku-4.5`

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and discovered instruction context?

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`

The run completed successfully and produced two added files:

- `backend/src/rules/notification-channel-rules.ts`
- `backend/tests/unit/notification-channel-rules.test.ts`

## What The Code Did Well

The generated change shows strong instruction-layer awareness.

- It created the new rule in `src/backend/src/rules/`, which is the surface covered by the global, backend, and business-rules instruction layers.
- It created matching tests in `src/backend/tests/unit/`, which is the surface covered by the testing instruction layer.
- The rule module stayed pure: no Express, database, queue, or audit imports were introduced.
- The rule returns a structured result object instead of a bare boolean.
- The module header comments explicitly document a false positive and a hard negative scenario.
- The California decline restriction includes `LEGAL-218` in the human-readable reason and in the rule identifier.
- The tests are explicit, behavior-oriented, and visibly grouped around happy path, boundary, false positive, and hard negative scenarios.
- The change stayed local to the rule and its test file and did not modify shared domain types.

## Constraint Review

Most required constraints were satisfied.

- Pure rule module: satisfied.
- Structured result shape: satisfied.
- `LEGAL-218` referenced in restriction metadata and reason: satisfied.
- False positive and hard negative module comments: satisfied.
- Matching unit tests with explicit scenario coverage: satisfied.
- No snapshots or shell commands in the generated change: satisfied.
- No change to `src/backend/src/models/types.ts`: satisfied.

## Remaining Weakness

The rerun eliminated the earlier duplicate mandatory-events helper and now imports `getMandatoryEvents()` from the existing rule module.

The remaining design tradeoff is smaller:

- the generated implementation still parses the transition string locally and re-encodes the known application states before calling `getMandatoryEvents()`

That is not a duplicate mandatory-event definition, and it does not materially weaken the lesson objective. It is a minor implementation detail rather than a prompt-compliance problem.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes, with one design caveat
- Required context applied: Yes

Overall judgment:

- The CLI edited the intended rule and test surfaces, which demonstrates that the lesson's scoped instruction architecture is being used.
- The generated code reflects both the business-rule and testing conventions in a meaningful way.
- The earlier duplicate mandatory-event caveat is resolved in this rerun.

## Final Assessment

For this prompt, the correct assessment is:

> Code changes were applied in the intended scoped locations and they follow the repository's layered instruction context well. This run should be considered fully successful for the lesson prompt, with only a minor non-blocking implementation tradeoff around local transition parsing.