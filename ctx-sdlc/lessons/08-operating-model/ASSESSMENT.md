# Lesson 08 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the read-only analysis produced by the lesson's GitHub Copilot CLI prompt respected the required operating-model constraints, repository context, and lesson objective for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Read .github/copilot-instructions.md, .github/scripts/audit_context.py, .github/scripts/detect_stale_refs.py, .github/examples/clean/copilot-instructions.md, .github/examples/drifted/copilot-instructions.md, and docs/maintenance-schedule.md. Produce a read-only operating-model analysis for context maintenance. Return: summary, what kinds of drift the lesson is trying to catch, the most dangerous differences between the clean and drifted examples, one false positive, one hard negative, a maintenance cadence recommendation, and prioritized fixes. Explicitly call out copy-paste drift, stale references, contradictory rules, over-specification, and under-specification. Do not modify files, do not run shell commands, and do not use SQL or any other write-capable tools. Inspect and read only.
```

This is the historical prompt captured for the assessed run.

Follow-up lesson design change: future runs should discover the relevant maintenance artifacts automatically instead of relying on a hardcoded file list, and should map major drift findings back to the exact artifacts that demonstrate them.

The assessment run used the user-requested complex-example model:

- `gpt-5.4`

## Assessment Scope

The only question being evaluated is:

> Did the produced read-only analysis accurately explain the lesson's context-maintenance operating model and the kinds of drift the lesson is designed to catch?

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

The generated answer is strong and closely aligned with the lesson objective.

- It summarizes the lesson correctly as an operating model for keeping `.github/` and `docs/` synchronized with the real codebase.
- It explicitly names the requested drift categories: copy-paste drift, stale references, contradictory rules, over-specification, and under-specification.
- It adds useful adjacent categories derived from the scripts, such as oversized global instructions, missing scoped metadata, over-privileged agents, broken links, and stale-but-unchanged files.
- It identifies the most dangerous clean-versus-drifted differences in the right places: stack facts, platform facts, file paths, and contradictory logging guidance.
- It gives a realistic false positive and a realistic hard negative based on what the scripts actually can and cannot detect.
- It recommends a maintenance cadence that matches the lesson's intended operating-model framing instead of presenting context maintenance as a one-time cleanup.
- It stayed read-only and respected the no-shell, no-SQL constraint.

## Constraint Review

Most required constraints were satisfied.

- Read-only behavior: satisfied.
- No shell commands: satisfied.
- No SQL or other write-capable tools: satisfied.
- Summary present: satisfied.
- Drift categories explicitly called out: satisfied.
- Dangerous clean versus drifted differences: satisfied.
- False positive and hard negative: satisfied.
- Maintenance cadence recommendation: satisfied.
- Prioritized fixes: satisfied.

## Remaining Weaknesses

The main limitations are about analytical depth, not correctness.

1. The answer is concise enough that some categories are grouped rather than traced back to exact artifacts.

For example, it correctly names contradictory rules and stale technology references, but it does not explicitly map each problem to the exact clean and drifted files that demonstrate it.

2. The hard-negative explanation is correct but broad.

The answer says the scripts will miss semantically wrong-but-existing guidance, which is true. A stronger version would have named a concrete example from the drifted materials where the file exists but the instruction is still wrong.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes
- Required context applied: Yes

Overall judgment:

- The run produced the intended read-only operating-model analysis for lesson 08.
- The answer demonstrates that the lesson is about continuous context hygiene, not only artifact creation.
- The remaining gaps are minor elaboration opportunities rather than lesson failures.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered successful for the lesson objective. It stayed fully read-only, captured the lesson's drift taxonomy, and explained the operating-model cadence and limits of automated audits well. The main non-blocking caveat is that the analysis could have tied a few of its conclusions more explicitly to specific clean-versus-drifted examples.