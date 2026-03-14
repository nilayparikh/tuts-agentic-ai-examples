# Lesson 06 — Guardrail Implementation Example

This document defines the concrete example used in Lesson 06.

## Objective

Show that the CLI can discover existing guardrail patterns and create a new import-validation guardrail that follows the same conventions — producing assessable file changes.

## Expected Output Shape

The demo must produce two new files:

1. `.github/hooks/import-validation.json` — PreToolUse hook config matching existing hook patterns
2. `.github/scripts/validate_imports.py` — validation script enforcing barrel-file import convention

## Expected Change Artifacts

Assessment compares the actual `demo.patch` and `changed-files.json` against:

- `.output/change/expected-files.json` — expected added/modified/deleted files
- `.output/change/expected-patterns.json` — regex patterns that must appear in the patch

## Required Constraints

1. The hook config must use `PreToolUse` event type following existing hook file patterns.
2. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths.
3. The implementation must follow the discovered conventions from existing hook configs and scripts.
4. The change must stay scoped to `.github/hooks/` and `.github/scripts/`.
5. Do not run shell commands during the assessment run.
6. Do not use SQL during the assessment run.

## Concrete Scenario

Use the lesson's existing hook configs (file-protection, pre-commit-validate, post-save-format) and their scripts as pattern references to create a new import-validation guardrail.

Good output should produce a hook + script pair that is consistent with the existing guardrail style.

## What Good Output Looks Like

Good output will usually:

- create a hook JSON config with `PreToolUse` event type and a reference to `validate_imports.py`
- create a Python validation script that checks import paths
- follow the same structure and conventions as the existing hook + script pairs
- keep the change scoped to the `.github/` guardrail surface
