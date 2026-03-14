# Lesson 06 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the output produced by the lesson's GitHub Copilot CLI prompt respected the required read-only guardrail-audit constraints, repository context, and lesson objective for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Read .github/copilot-instructions.md, .github/mcp.json, docs/tool-trust-boundaries.md, docs/security-policy.md, .github/hooks/file-protection.json, .github/hooks/pre-commit-validate.json, .github/hooks/post-save-format.json, .github/scripts/check_protected_files.py, and .github/scripts/validate_commit.py. Produce a read-only guardrail audit for this lesson. Return: summary, confirmed controls, inconsistencies with file references, false positives, hard negatives, prioritized fixes, and residual risks. Explicitly call out whether protected-file policy matches hook enforcement, whether filesystem scope matches the documented trust boundaries, whether fail-closed audit and 404-not-403 rules are represented consistently, and what the CLI cannot demonstrate because VS Code hooks do not run here. Do not modify files, do not run shell commands, and do not use SQL or any other write-capable tools. Inspect and read only.
```

This is the historical prompt captured for the assessed run.

Follow-up lesson design change: future runs should discover the relevant guardrail, policy, and enforcement artifacts automatically instead of relying on a hardcoded file list.

The assessment run used the user-requested complex-example model:

- `gpt-5.4`

## Assessment Scope

The only question being evaluated is:

> Did the produced audit follow the prompt in a way that respects the repository's documented constraints and the lesson's read-only guardrail-analysis objective?

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

That is the correct high-level outcome for this lesson, because lesson 06's CLI demo is an audit, not a code-change exercise.

## What The Audit Did Well

The generated output is strong and well-aligned with the lesson objective.

- It stayed fully read-only.
- It inspected the hook files, hook scripts, MCP config, policy docs, and Copilot instructions together instead of reading them in isolation.
- It correctly identified the largest real inconsistency in the lesson: the mismatch between `docs/security-policy.md` and `.github/scripts/check_protected_files.py`.
- It correctly identified that `src/frontend/src/` is present in `.github/mcp.json` and `docs/tool-trust-boundaries.md` but omitted from `.github/copilot-instructions.md`.
- It correctly noted that the fail-closed audit rule is documented but not enforced by the inspected hooks/scripts.
- It correctly noted that the 404-not-403 rule is documented in instructions but not represented consistently across the inspected lesson artifacts.
- It explicitly distinguished static auditability from runtime hook behavior that the CLI cannot prove.
- Its false-positive, hard-negative, prioritized-fix, and residual-risk sections are all grounded in concrete file references.

## Constraint Review

The required constraints were satisfied.

- Read-only lesson outcome: satisfied.
- No tracked file edits: satisfied.
- No shell commands: satisfied.
- No SQL or other write-capable tool usage: satisfied.
- Hook, script, MCP, and policy comparison: satisfied.
- Protected-file policy vs enforcement comparison: satisfied.
- Trust-boundary vs MCP scope comparison: satisfied.
- Fail-closed audit coverage discussion: satisfied.
- 404-not-403 consistency discussion: satisfied.
- Explicit note about CLI limits vs VS Code runtime hooks: satisfied.

## Remaining Weakness

There is no meaningful prompt-compliance problem in this run.

The main limitation is inherent to the lesson format rather than the output:

- this was a static config audit, so it cannot prove that the hooks execute correctly at runtime in VS Code

The session itself explicitly called that out, which is the correct behavior.

## Verdict

Assessment result for this prompt:

- Guardrail-audit objective followed: Yes
- Repository files kept read-only: Yes
- Required context applied: Yes

Overall judgment:

- The run is a good demonstration of lesson 06.
- The audit is specific, source-grounded, and surfaces real inconsistencies instead of repeating the intended policy.
- The output cleanly separates what is statically demonstrable from what still requires live VS Code hook testing.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered fully successful for the lesson objective. It produced a useful, source-grounded, read-only guardrail audit, kept the repository unchanged, and identified real mismatches between documented policy and enforced behavior without overstating what the CLI could prove.
