# Lesson 09 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the capstone lesson's project instructions, backend and frontend scoped instructions, architecture doc, and the relevant backend/frontend notification-preference surfaces you discover before answering. Do not assume a fixed file list beyond those starting points. Then implement a notification preference event-channel validator as a cross-stack hardening slice: 1. Create a pure validation rule module at backend/src/rules/preference-event-channel-validator.ts that validates event-channel combinations are allowed, enforcing that mandatory events cannot have all channels disabled, and respecting LEGAL-218 California SMS restrictions from existing rules. 2. Create unit tests at backend/tests/unit/preference-event-channel-validator.test.ts covering valid combinations, mandatory-event violations, and LEGAL-218 false positive and hard negative cases. 3. Wire the validator import into the existing notification preference write route in backend/src/routes/notifications.ts. Follow the repository conventions you discover. Apply the changes directly in code. Do not run npm install, npm test, or any shell commands. Do not use SQL.
```

The rerun used `gpt-5.4`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's cross-stack conventions and discovered context?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `backend/src/rules/preference-event-channel-validator.ts` (added), `backend/tests/unit/preference-event-channel-validator.test.ts` (added), `backend/src/routes/notifications.ts` (modified)
- `.output/change/expected-patterns.json` — required patterns in patch: event-channel, mandatory, LEGAL-218, import validator, tests, false positive/hard negative

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`
- `.output/change/comparison.md`

The rerun completed successfully and produced the exact expected file set:

- added `backend/src/rules/preference-event-channel-validator.ts`
- added `backend/tests/unit/preference-event-channel-validator.test.ts`
- modified `backend/src/routes/notifications.ts`

The comparison report shows:

- `Files match: True`
- `Patterns match: True`

All required expectation patterns matched, including event-channel validation, mandatory-event enforcement, `LEGAL-218`, route wiring through the validator, test coverage, and explicit false-positive / hard-negative handling.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes
- Required context applied: Yes

Overall judgment:

- The rerun produced the intended rule-plus-tests-plus-route shape for the capstone.
- The generated change matched both the expected file manifest and the expected behavioral patterns.
- This run is a complete success for the updated lesson objective.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered fully successful. It produced the expected cross-stack backend hardening slice, matched the expected file manifest exactly, and covered the required validator, rule, and test behaviors.
