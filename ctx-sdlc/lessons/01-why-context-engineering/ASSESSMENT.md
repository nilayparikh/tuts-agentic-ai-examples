# Lesson 01 Comparative Prompt Assessment

This assessment is intentionally comparative.

It evaluates the same prompt under two workspace conditions:

- `with-context/`
- `without-context/`

It does not claim a fresh rerun in this change. It records the current lesson-01
assessment framing based on the existing comparison material.

## Prompt Under Review

```text
Implement the manual review escalation workflow for this repository.
Follow existing repo conventions and architecture.
Return the exact files you would change and the code for each change.
```

This is the historical prompt used for the existing with-context versus without-context comparison.

## Assessment Scope

The only question being evaluated is:

> Does the same prompt become materially more repository-aware when the lesson exposes the right contextual workspace files?

## Current Assessment Basis

Lesson 01 does not yet use the standardized `.output/` prompt-assessment bundle
used by lessons 02 through 08.

The current comparative assessment is based on:

- `README.md`
- `COMPARE.md`
- `with-context/docs/experiment.md`
- `with-context/docs/manual-review-escalation.md`

## Current Verdict

Based on the existing comparison, the lesson succeeds.

- The with-context run is clearly more repository-aware.
- The without-context run is plausible but wrong in repo-specific ways.
- The comparison demonstrates that context changes architecture choices, route shape, permission behavior, audit behavior, queue reuse, and regulatory nuance.

## What The Lesson Already Demonstrates Well

- It keeps the prompt short and realistic.
- It shows that hidden repository rules do not need to be restated in the prompt when the workspace carries the right context.
- It creates a strong contrast between a context-aware workflow and a plausible but repo-wrong workflow.
- It focuses on repository intent, not only syntactic correctness.

## Current Gaps

1. Lesson 01 does not yet have the same standardized prompt-assessment artifact bundle as lessons 02 through 08.

That makes the lesson slightly harder to compare mechanically with the rest of the series.

2. The with-context run still appears to miss one response detail called out in `COMPARE.md`.

The expected payload shape should include `notificationEventId`, so the contextual result is substantially better than baseline but still not perfect.

## Follow-Up Design Change

Future standardization for lesson 01 should:

- capture both runs under a consistent artifact layout similar to lessons 02 through 08
- preserve the same short prompt in both workspace conditions
- score the pair explicitly against the existing lesson rubric instead of relying only on prose comparison

## Final Assessment

For lesson 01, the correct assessment is:

> The lesson is successful as a comparative context-engineering demonstration. The same prompt performs materially better when the workspace exposes the hidden repository context. The remaining gap is structural: lesson 01 should eventually adopt the same standardized artifact capture used by the later lessons.
