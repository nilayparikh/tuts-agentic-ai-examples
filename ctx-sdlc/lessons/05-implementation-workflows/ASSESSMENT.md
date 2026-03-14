# Lesson 05 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required implementation constraints, repository context, and lesson objective for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Read docs/implementation-playbook.md, specs/product-spec-notification-preferences.md, specs/non-functional-requirements.md, src/backend/src/routes/notifications.ts, src/backend/src/rules/mandatory-events.ts, src/backend/src/models/preference-repository.ts, and src/backend/src/services/audit-service.ts. Implement a focused notification-preference write hardening slice. Write tests first at src/backend/tests/unit/notification-preference-write-rules.test.ts, then add a pure rule module at src/backend/src/rules/notification-preference-write-rules.ts, and wire the minimal production changes into src/backend/src/routes/notifications.ts. The rule must use explicit inputs plus existing types, not direct DB access. Enforce these cases: manual-review-escalation must keep at least one channel enabled; decline SMS cannot be enabled when loanState is CA or California under LEGAL-218; the false positive where escalation SMS is disabled but escalation email stays enabled must remain allowed. Preserve delegated-session and role guards, keep changes minimal, include top-of-module false-positive and hard-negative comments in the new rule file, and do not edit protected config or database files. Do not run npm install, npm test, npx vitest, or any shell commands. Inspect and edit files only. Return a short handoff summary naming changed files and which tests should pass.
```

This is the historical prompt captured for the assessed run.

Follow-up lesson design change: future runs should discover the relevant route, rule, service, and spec context automatically instead of relying on a hardcoded file list, which also avoids stale or missing file references.

The assessment run used the user-requested complex-example model:

- `gpt-5.4`

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and intended lesson scope?

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`

The successful rerun completed and produced three tracked file changes:

- added `backend/src/rules/notification-preference-write-rules.ts`
- added `backend/tests/unit/notification-preference-write-rules.test.ts`
- modified `backend/src/routes/notifications.ts`

That is the correct high-level shape for this lesson.

## What The Code Did Well

The generated change is focused and mostly aligned with the lesson objective.

- It created a new pure rule module under `src/backend/src/rules/` instead of embedding the full policy in the route.
- It created a matching unit test file under `src/backend/tests/unit/`.
- It limited production edits to the existing notification route rather than sprawling into unrelated services or config.
- The new rule module includes top-of-file false-positive and hard-negative comments.
- The rule enforces the requested escalation-channel constraint.
- The rule enforces the requested California decline SMS restriction and references `LEGAL-218` in the rejection reason.
- The route preserves the pre-existing delegated-session and permission checks.
- The route now performs audit before persistence, which is closer to the documented fail-closed ordering than the baseline route.

## Constraint Review

Most required constraints were satisfied.

- Focused change shape: satisfied.
- New pure rule module: satisfied.
- Matching unit test file: satisfied.
- Delegated-session and role guards preserved: satisfied.
- Mandatory-event channel protection: satisfied.
- California `LEGAL-218` restriction: satisfied.
- False-positive and hard-negative rule comments: satisfied.
- Protected config and database files untouched: satisfied.
- No shell commands executed by the session: satisfied.

## Remaining Weaknesses

There are several real caveats.

1. The session used a SQL todo-write tool even though the prompt said to inspect and edit files only.

This did not modify lesson files, but it is outside the intended tool boundary for the demo.

2. The session tried to read `specs/product-spec-notification-preferences.md` inside lesson 05, and that path does not exist in this lesson.

The implementation still landed in a reasonable place because the prompt and lesson docs were strong enough, but part of the requested source context was missing during the run.

3. The TDD requirement was only partially demonstrated.

The run created the test file and the rule file, but because shell commands were forbidden, there is no red-step proof that the tests were observed failing before implementation. The lesson prompt asked for tests first, but the strongest TDD evidence available here is file creation order and the presence of the test file.

4. The rule is narrower than the full playbook and NFR language.

It hardens the generic preference write route, but it does not extend the same rule coverage to the bulk email and SMS routes that remain in the file. That keeps the change focused, which is good for lesson scope, but it means the hardening slice is not comprehensive across all preference mutation surfaces.

## Verdict

Assessment result for this prompt:

- Standards followed: Mostly yes
- Constraints followed: Yes, with notable caveats
- Required context applied: Partially yes

Overall judgment:

- The run produced the right kind of focused implementation change for lesson 05.
- The change is small, local, and materially improves the notification preference write path.
- The session was not perfectly clean from a workflow standpoint because it used SQL todo writes and partially missed the requested source context.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered successful for the lesson objective. It produced a focused rule-plus-tests implementation slice in the intended surfaces and preserved the key delegated-session and notification-policy constraints. The main non-blocking caveats are the use of a SQL todo tool, the missing lesson-local product-spec file, and incomplete evidence for a strict red-step TDD sequence.

## Expected Change Comparison

Assessment now also compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `backend/src/rules/notification-preference-write-rules.ts` (added), `backend/tests/unit/notification-preference-write-rules.test.ts` (added), `backend/src/routes/notifications.ts` (modified)
- `.output/change/expected-patterns.json` — required patterns in patch: import, validate, LEGAL-218, test, delegated/owner

The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report. Future re-runs will automatically produce this comparison alongside the existing assessment artifacts.
