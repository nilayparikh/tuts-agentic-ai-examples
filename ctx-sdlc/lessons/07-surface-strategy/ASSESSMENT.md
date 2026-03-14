# Lesson 07 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the read-only analysis produced by the lesson's GitHub Copilot CLI prompt respected the required portability constraints, repository context, and lesson objective for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Read .github/copilot-instructions.md, .github/instructions/api.instructions.md, .github/agents/reviewer.agent.md, docs/cli-guide.md, and docs/portability-matrix.md. Produce a read-only surface-strategy analysis for this lesson. Return: summary, what is portable across all surfaces, what is VS Code-only, one concrete portability risk, one false positive, one hard negative, and prioritized recommendations for where each kind of guidance should live. Explicitly compare CLI, VS Code Chat, inline completions, coding agent, and code review surfaces, and call out path-scoped instructions, agents, prompts, MCP, hooks, and docs separately. Do not modify files, do not run shell commands, and do not use SQL or any other write-capable tools. Inspect and read only.
```

This is the historical prompt captured for the assessed run.

Follow-up lesson design change: future runs should discover the relevant portability artifacts automatically instead of relying on a hardcoded file list, and should explicitly resolve which artifact is canonical when lesson materials disagree.

The assessment run used the user-requested complex-example model:

- `gpt-5.4`

## Assessment Scope

The only question being evaluated is:

> Did the produced read-only analysis answer the prompt accurately and in a way that matches the lesson's intended surface-portability teaching point?

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`

The successful run completed with no tracked file changes:

- added: none
- modified: none
- deleted: none

That is the correct high-level shape for this lesson.

## What The Analysis Did Well

The generated answer is focused and materially aligned with the lesson objective.

- It clearly identifies `.github/copilot-instructions.md` as the only guaranteed cross-surface foundation.
- It compares the requested surfaces explicitly: CLI, VS Code Chat, inline completions, coding agent, and code review.
- It separates portable guidance from VS Code-only guidance instead of flattening everything into one bucket.
- It calls out path-scoped instructions, agents, prompts, MCP, hooks, and docs as separate mechanism categories.
- It provides the requested risk taxonomy: one concrete portability risk, one false positive, and one hard negative.
- It gives prioritized recommendations for where different kinds of guidance should live.
- It stayed read-only and respected the no-shell, no-SQL constraint.

## Constraint Review

Most required constraints were satisfied.

- Read-only behavior: satisfied.
- No shell commands: satisfied.
- No SQL or other write-capable tools: satisfied.
- Requested surface comparison: satisfied.
- Portable versus VS Code-only split: satisfied.
- Risk, false-positive, and hard-negative callouts: satisfied.
- Prioritized recommendations: satisfied.

## Remaining Weaknesses

There is one substantive caveat and one smaller limitation.

1. The answer surfaced a real contradiction but did not fully resolve it.

It notes that `.github/agents/reviewer.agent.md` says agents are VS Code Chat-only while `docs/portability-matrix.md` says agents also work in Coding Agent. That is exactly the right inconsistency to detect, but the response stops at identifying the conflict rather than stating which source should be treated as canonical.

2. The recommendations are correct but slightly compressed.

The prompt asked to call out prompts, MCP, hooks, and docs separately, and the response does that, but it could have been a little more explicit about which of those are portability enhancers versus which are enforcement-only or surface-local.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes
- Required context applied: Yes

Overall judgment:

- The run produced the intended read-only portability analysis for lesson 07.
- The answer captured the core teaching point that portable context must live in the base layer and that richer artifacts should be treated as surface-specific enhancements.
- The remaining issue is analytical completeness, not behavioral correctness.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered successful for the lesson objective. It stayed fully read-only, compared the requested surfaces, and correctly explained the core portability hierarchy. The main non-blocking caveat is that it identified but did not definitively resolve the agent-surface inconsistency between the lesson's own artifacts.