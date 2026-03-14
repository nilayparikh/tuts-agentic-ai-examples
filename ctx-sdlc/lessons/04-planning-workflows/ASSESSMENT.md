# Lesson 04 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the output produced by the lesson's GitHub Copilot CLI prompt respected the required planning constraints, repository context, and lesson objective for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Read docs/architecture.md, docs/adr/ADR-003-frontend-state.md, specs/product-spec-notification-preferences.md, specs/non-functional-requirements.md, and specs/feature-request.md. Produce a read-only implementation plan for notification preferences. Separate confirmed product requirements from inferred implementation choices. Return: summary, open questions with source references, constraints and special conditions, numbered tasks with acceptance criteria and source refs, validation steps, and risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative. Do not modify files and do not run shell commands. Inspect and read only.
```

This is the historical prompt captured for the assessed run.

Follow-up lesson design change: future runs should discover relevant docs, specs, and source surfaces automatically instead of relying on a hardcoded file list.

The assessment run used the user-requested complex-example model:

- `gpt-5.4`

## Assessment Scope

The only question being evaluated is:

> Did the produced planning output follow the prompt in a way that respects the repository's documented constraints and the lesson's read-only planning objective?

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`

The run completed successfully.

The captured repository change artifacts are clean:

- `changed-files.json` shows no added, modified, or deleted tracked files
- `demo.patch` is empty

That is the correct high-level outcome for this lesson, because lesson 04 is a planning-only, read-only demo.

## What The Plan Did Well

The generated output is materially aligned with the lesson objective.

- It read and synthesized the architecture, ADR, product spec, NFRs, and feature request together instead of anchoring on a single document.
- It explicitly separated confirmed product requirements from inferred implementation choices.
- It preserved the planning boundary and returned a structured plan instead of proposing direct code edits.
- It surfaced meaningful open questions instead of silently filling gaps in the source material.
- It called out all of the lesson-specific planning traps the prompt required: delegated sessions, `LEGAL-218`, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, false positives, and hard negatives.
- Its numbered tasks are implementation-oriented without crossing into implementation, which is the correct shape for this lesson.
- Its validation section is concrete and tied to the hard-negative and false-positive scenarios in the specs.
- Its risks section is grounded in the actual documented ambiguities, especially contextual restrictions and ADR-003 state ownership.

## Constraint Review

Most required constraints were satisfied.

- Read-only lesson outcome: satisfied.
- No tracked file edits: satisfied.
- No shell commands: satisfied.
- Source-grounded planning output: satisfied.
- Separation of confirmed requirements from inferred choices: satisfied.
- Explicit handling of delegated sessions: satisfied.
- Explicit handling of `LEGAL-218`: satisfied.
- Explicit handling of mandatory-event delivery: satisfied.
- Explicit handling of fail-closed audit behavior: satisfied.
- Explicit handling of degraded-mode fallback: satisfied.
- Explicit false positive and hard negative coverage: satisfied.

## Remaining Weakness

There is one process caveat.

During the session, the model used a SQL tool to insert planning todos before continuing with document reads and plan generation.

That did not modify lesson files, and it did not affect the repository output. However, the prompt said:

> Do not modify files and do not run shell commands. Inspect and read only.

On a strict reading, creating planning todos is slightly outside the intended "inspect and read only" boundary, even though the final repo state remained read-only.

This is a tooling-discipline caveat, not a lesson-output failure.

## Verdict

Assessment result for this prompt:

- Planning objective followed: Yes
- Repository files kept read-only: Yes
- Required context applied: Yes
- Prompt followed perfectly: No, due to one minor tooling-boundary caveat

Overall judgment:

- The planning result itself is strong and well-grounded in the provided sources.
- The lesson's intended behavior was demonstrated: the session produced a useful implementation plan without editing the codebase.
- The only notable issue is that the session was not perfectly pure in its tooling behavior because it created planning todos through a non-file write tool.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered successful for the lesson objective. It produced a source-grounded, structured, read-only implementation plan and kept the repository unchanged. The only non-blocking caveat is that the session used a planning-todo write tool, which is slightly outside the strictest interpretation of "inspect and read only."