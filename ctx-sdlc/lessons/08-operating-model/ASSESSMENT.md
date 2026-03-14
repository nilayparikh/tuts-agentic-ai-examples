# Lesson 08 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the lesson's context-maintenance artifacts before answering. Discover the relevant project instructions, audit scripts, clean and drifted examples, and maintenance docs that exist here rather than assuming a fixed file list. Then fix the drifted example at .github/examples/drifted/copilot-instructions.md by resolving all drift issues you find. Specifically: update stale technology references (Node.js version, logging library), remove contradictory rules (console.log vs structured logging), fix dead file path references (deleted helpers directory), remove over-specified inline code blocks that belong in scoped instructions, and align the drifted file with the clean example's conventions for accuracy and conciseness. Apply the fixes directly in the file. Do not run shell commands and do not use SQL.
```

The assessment run uses the model from `lessons/_common/assessment-config.json`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that correctly resolves the drift issues and follows the clean example's conventions?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected file: `.github/examples/drifted/copilot-instructions.md` (modified)
- `.output/change/expected-patterns.json` — required patterns in patch: Node.js 20, pino, remove console.log, remove helpers

The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report.

## Assessment Criteria

| Criterion | Source |
| --- | --- |
| Drifted file modified | `expected-files.json` |
| Node.js version updated (18 → 20) | `expected-patterns.json` |
| Logging library updated (winston → pino) | `expected-patterns.json` |
| console.log contradiction resolved | `expected-patterns.json` |
| Dead helpers reference removed | `expected-patterns.json` |
| No shell commands executed | Prompt constraint |
| No SQL tools used | Prompt constraint |

## Captured Result

Pending re-run with the updated implementation-oriented prompt. Previous assessment was for a read-only operating-model analysis demo that has been replaced.

## Verdict

Pending re-run.