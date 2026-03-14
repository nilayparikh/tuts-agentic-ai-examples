# Lesson 08 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the lesson's context-maintenance artifacts before answering. Discover the relevant project instructions, audit scripts, clean and drifted examples, and maintenance docs that exist here rather than assuming a fixed file list. Then fix the drifted example at .github/examples/drifted/copilot-instructions.md by resolving all drift issues you find. Specifically: update stale technology references (Node.js version, logging library), remove contradictory rules (console.log vs structured logging), fix dead file path references (deleted helpers directory), remove over-specified inline code blocks that belong in scoped instructions, and align the drifted file with the clean example's conventions for accuracy and conciseness. Apply the fixes directly in the file. Do not run shell commands and do not use SQL.
```

The rerun used `gpt-5.4`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that correctly resolves the drift issues and follows the clean example's conventions?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected file: `.github/examples/drifted/copilot-instructions.md` (modified)
- `.output/change/expected-patterns.json` — required patterns in patch: Node.js 20, pino, remove console.log, remove helpers

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`
- `.output/change/comparison.md`

The rerun completed and the comparison report shows:

- `Files match: True`
- `Patterns match: False`

The file-manifest match confirms that the run targeted the correct file surface:

- modified `.github/examples/drifted/copilot-instructions.md`

But the pattern comparison only confirmed one of the required drift fixes:

- matched: console.log contradiction resolution
- missing: explicit Node.js 20 update
- missing: explicit `pino` logging update
- missing: dead helpers-directory reference removal

## Verdict

Assessment result for this prompt:

- Standards followed: Partially
- Constraints followed: Partially
- Required context applied: Partially

Overall judgment:

- The rerun did operate on the correct drifted instruction file.
- It did not show evidence that the most important stale-fact fixes were actually applied.
- That makes the run incomplete for the lesson objective even though the file target itself was correct.

## Final Assessment

For this prompt, the correct assessment is:

> The run should not be considered fully successful. It modified the correct file, but the captured comparison does not show the required stale technology and dead-reference fixes that define the lesson's drift-repair objective.
