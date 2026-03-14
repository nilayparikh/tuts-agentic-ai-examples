# Lesson 06 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL.
```

The assessment run uses the model from `lessons/_common/assessment-config.json`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and discovered guardrail patterns?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `.github/hooks/import-validation.json` (added), `.github/scripts/validate_imports.py` (added)
- `.output/change/expected-patterns.json` — required patterns in patch: PreToolUse, validate_imports.py, import, barrel/index.ts

The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report.

## Assessment Criteria

| Criterion | Source |
| --- | --- |
| Hook config created at `.github/hooks/import-validation.json` | `expected-files.json` |
| Validation script created at `.github/scripts/validate_imports.py` | `expected-files.json` |
| Hook uses `PreToolUse` event type | `expected-patterns.json` |
| Hook references `validate_imports.py` | `expected-patterns.json` |
| Script checks import paths | `expected-patterns.json` |
| Script enforces barrel-file (index.ts) convention | `expected-patterns.json` |
| No shell commands executed | Prompt constraint |
| No SQL tools used | Prompt constraint |

## Captured Result

Pending re-run with the updated implementation-oriented prompt. Previous assessment was for a read-only guardrail audit demo that has been replaced.

## Verdict

Pending re-run.
