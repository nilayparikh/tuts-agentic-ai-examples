# Lesson 02 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Refactor notification preference write handlers so the generic route and the existing email/SMS routes follow the same owner-only, delegated-session, audit, and FORBIDDEN-error conventions. Follow the repository conventions you discover. Apply the change directly in code instead of only describing it. Do not run npm install, npm test, or any shell commands. Inspect and edit files only.
```

The assessment run used the shared default model from `lessons/_common/assessment-config.json`:

- `claude-haiku-4.5`

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and discovered context?

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`

The run completed successfully and produced one modified file:

- `backend/src/routes/notifications.ts`

## What The Code Did Well

The generated change shows clear repository-awareness in several ways.

- It worked in the existing `notifications.ts` route file instead of inventing a new unrelated location.
- It kept the generic route and the existing email and SMS routes, then refactored them locally.
- It extracted a small shared helper, `validatePreferenceWriteAuth`, instead of duplicating the same authorization logic in three places.
- It enforces owner-only writes for the generic route and both channel-specific routes.
- It blocks delegated sessions consistently across all write paths.
- It keeps the existing `hasPermission` check and preserves compliance-reviewer read-only behavior.
- It switched the write-path authorization failures to `throw new Error("FORBIDDEN: ...")`, which matches the repository's central error-handler contract.
- It preserved `auditAction(...)` behavior and did not introduce new queue contracts, types, services, or shell-command dependencies.

## Constraint Review

The final result satisfies the lesson prompt's required constraints.

- Owner-only writes: satisfied.
- Delegated-session blocking: satisfied.
- Compliance-reviewer read-only behavior: satisfied through role + permission enforcement.
- Central `FORBIDDEN:` error-prefix handling: satisfied.
- Audit behavior preserved: satisfied.
- No new queue contracts or domain types: satisfied.
- Change stays local to the preference-routing surface: satisfied.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes
- Required context applied: Yes

Overall judgment:

- The CLI applied a focused refactor that matches the lesson's curated context.
- The resulting change follows the repository standards and the prompt's constraints without expanding the scope of the edit.
- This run should be treated as a complete success for the lesson prompt.

## Final Assessment

For this prompt, the correct assessment is:

> Code changes were applied and they follow the repository's standards, constraints, and discovered context as required for this lesson prompt. This run should be considered fully successful.
