# Lesson 07 — Surface Strategy Example

This document defines the concrete example used in Lesson 07.

## Objective

Show that the CLI can analyze surface-portability concerns and produce actionable artifacts: a portable baseline instruction file and a surface-portability analysis document.

## Expected Output Shape

The demo must produce two new files:

1. `.github/instructions/portable-baseline.instructions.md` — extracted cross-surface-portable instruction subset with `applyTo: '**'` scope
2. `docs/surface-portability-notes.md` — analysis documenting portable vs surface-specific features, risks, and recommendations

## Expected Change Artifacts

Assessment compares the actual `demo.patch` and `changed-files.json` against:

- `.output/change/expected-files.json` — expected added/modified/deleted files
- `.output/change/expected-patterns.json` — regex patterns that must appear in the patch

## Required Constraints

1. The portable baseline instruction must work across CLI, Chat, inline completions, coding agent, and code review surfaces.
2. The analysis must compare CLI, VS Code Chat, inline completions, coding agent, and code review explicitly.
3. The analysis must treat `.github/copilot-instructions.md` as the universal baseline and explain why.
4. The analysis must note that `.instructions.md`, agents, prompts, MCP, and hooks are not equally portable.
5. If lesson artifacts disagree, the analysis must identify which one should be treated as canonical and why.
6. The portability notes must include one portability risk, one false positive, and one hard negative.
7. Do not run shell commands during the assessment run.
8. Do not use SQL during the assessment run.

## Concrete Scenario

Use the lesson's current files to extract what guidance would still help on the widest range of Copilot surfaces and capture that in a dedicated portable-baseline instruction file.

## What Good Output Looks Like

Good output will usually:

- create a portable-baseline instruction file scoped to all files
- extract only guidance that works across all five surfaces
- create a portability notes document with risk taxonomy
- explain why `api.instructions.md` is stronger but less portable than the baseline
- call out one false positive where a CLI limitation is mistaken for missing context
- call out one hard negative where teams put critical guidance only in a non-portable layer
