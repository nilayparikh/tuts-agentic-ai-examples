# Lesson 06 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL.
```

The rerun used `gpt-5.4`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and discovered guardrail patterns?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `.github/hooks/import-validation.json` (added), `.github/scripts/validate_imports.py` (added)
- `.output/change/expected-patterns.json` — required patterns in patch: PreToolUse, validate_imports.py, import, barrel/index.ts

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`
- `.output/change/comparison.md`

The rerun completed and produced one tracked file change:

- added `.github/hooks/import-validation.json`

The generated hook file used the correct `PreToolUse` event type and referenced `python .github/scripts/validate_imports.py`, but the run did **not** create the expected `.github/scripts/validate_imports.py` file.

The comparison report shows:

- `Files match: False`
- `Patterns match: False`

Detailed misses:

- expected added files: `.github/hooks/import-validation.json`, `.github/scripts/validate_imports.py`
- actual added files: `.github/hooks/import-validation.json`
- missing expected pattern: barrel-file or `index.ts` import convention

## Verdict

Assessment result for this prompt:

- Standards followed: Partially
- Constraints followed: Partially
- Required context applied: Partially

Overall judgment:

- The rerun discovered the right hook surface and created a correctly-shaped hook config.
- The implementation stopped short of the full lesson objective because it never created the validation script.
- The most important repository-specific rule, the barrel-file import convention, was not actually implemented.

## Final Assessment

For this prompt, the correct assessment is:

> The run should not be considered fully successful. It produced a plausible hook config, but it failed to create the companion validation script and did not demonstrate the required barrel-file import enforcement logic.
