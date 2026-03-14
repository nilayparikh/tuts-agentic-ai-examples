# Lesson 04 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the relevant docs/, specs/, and existing source surfaces for notification preferences in this lesson before answering. Discover the architecture, ADR, product, and NFR context you need rather than assuming a fixed file list. Produce a structured implementation plan and save it to docs/notification-preferences-plan.md. The plan must include: summary, source-backed confirmed requirements with references to FR/SC/ADR/NFR identifiers, open questions with file references, inferred implementation choices separated from confirmed requirements, constraints and special conditions, numbered tasks with acceptance criteria and source references, validation steps, and risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative. If the sources overlap or conflict, identify the canonical source for the plan and explain why. Do not run shell commands and do not use SQL.
```

The rerun used `gpt-5.4`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and discovered context?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected file: `docs/notification-preferences-plan.md` (added)
- `.output/change/expected-patterns.json` — required patterns in patch: delegated-session, LEGAL-218, mandatory-event, fail-closed audit, false positive, hard negative, acceptance criteria

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`
- `.output/change/comparison.md`

The rerun completed successfully and produced exactly one tracked file change:

- added `docs/notification-preferences-plan.md`

The comparison report shows:

- `Files match: True`
- `Patterns match: True`

All required plan-content checks matched, including delegated-session handling, `LEGAL-218`, mandatory-event delivery, fail-closed audit behavior, false positive, hard negative, and tasks with acceptance criteria.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes
- Required context applied: Yes

Overall judgment:

- The rerun produced the expected plan artifact in the correct location.
- The plan content matched all required expectation patterns.
- This run is a complete success for the updated lesson objective.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered fully successful. It wrote the expected plan file, matched the expected file manifest exactly, and covered all required planning constraints in the generated content.