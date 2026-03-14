# Lesson 08 — Operating Model Example

This document defines the concrete example used in Lesson 08.

## Objective

Show that the CLI can discover context drift in a drifted instruction file and fix it — producing an assessable code change that resolves real maintenance issues.

## Expected Output Shape

The demo must modify one file:

1. `.github/examples/drifted/copilot-instructions.md` — fixed to resolve all discovered drift issues

The fixed file should resolve:

1. Stale technology references (Node.js version, logging library)
2. Contradictory rules (console.log vs structured logging)
3. Dead file path references (deleted helpers directory)
4. Over-specified inline code blocks that belong in scoped instructions
5. Alignment with the clean example's conventions

## Expected Change Artifacts

Assessment compares the actual `demo.patch` and `changed-files.json` against:

- `.output/change/expected-files.json` — expected added/modified/deleted files
- `.output/change/expected-patterns.json` — regex patterns that must appear in the patch

## Required Constraints

1. The fix must be applied directly to `.github/examples/drifted/copilot-instructions.md`.
2. The fix must update stale Node.js version references (18 → 20).
3. The fix must replace the stale logging library reference (winston → pino).
4. The fix must remove contradictory console.log rules.
5. The fix must remove or update dead file path references to non-existent helpers.
6. The fix must remove over-specified inline code blocks.
7. Do not run shell commands during the assessment run.
8. Do not use SQL during the assessment run.

## Concrete Scenario

Use the lesson's clean and drifted example instruction files plus the maintenance scripts and schedule to discover and fix all drift in the drifted file.

## What Good Output Looks Like

Good output will usually:

- update Node.js 18 references to Node.js 20
- replace winston references with pino
- remove or resolve the console.log contradiction
- remove references to deleted helpers directory
- make the drifted file concise and accurate like the clean example
