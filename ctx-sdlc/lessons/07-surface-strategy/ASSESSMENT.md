# Lesson 07 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the lesson's surface-strategy artifacts before answering. Discover the relevant baseline instructions, scoped instructions, agents, prompts, MCP, hooks, and docs that exist here rather than assuming a fixed file list. Then create two new files based on your analysis: 1. Create .github/instructions/portable-baseline.instructions.md containing the extracted cross-surface-portable subset of the existing instructions that works on CLI, Chat, inline completions, coding agent, and code review surfaces. Use applyTo: '**' scope. 2. Create docs/surface-portability-notes.md documenting which features are portable vs surface-specific, one concrete portability risk, one false positive, one hard negative, and recommendations for where each kind of guidance should live. Follow the discovered instruction architecture conventions. Apply the changes directly in files. Do not run shell commands and do not use SQL.
```

The assessment run uses the model from `lessons/_common/assessment-config.json`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's surface-strategy conventions and instruction architecture?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `.github/instructions/portable-baseline.instructions.md` (added), `docs/surface-portability-notes.md` (added)
- `.output/change/expected-patterns.json` — required patterns in patch: scope, portable, CLI/surfaces, VS Code, risk taxonomy

The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report.

## Assessment Criteria

| Criterion | Source |
| --- | --- |
| Portable baseline instruction created | `expected-files.json` |
| Surface portability notes created | `expected-files.json` |
| Instruction uses cross-surface scope | `expected-patterns.json` |
| Content is portable across surfaces | `expected-patterns.json` |
| Multiple surfaces compared (CLI, VS Code) | `expected-patterns.json` |
| Risk taxonomy present | `expected-patterns.json` |
| No shell commands executed | Prompt constraint |
| No SQL tools used | Prompt constraint |

## Captured Result

Pending re-run with the updated implementation-oriented prompt. Previous assessment was for a read-only surface-analysis demo that has been replaced.

## Verdict

Pending re-run.