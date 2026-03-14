# Lesson 07 CLI Prompt Assessment

This assessment is intentionally narrow.

It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.

It does not assess the lesson overall.

## Prompt Under Test

```text
Inspect the lesson's surface-strategy artifacts before answering. Discover the relevant baseline instructions, scoped instructions, agents, prompts, MCP, hooks, and docs that exist here rather than assuming a fixed file list. Then create two new files based on your analysis: 1. Create .github/instructions/portable-baseline.instructions.md containing the extracted cross-surface-portable subset of the existing instructions that works on CLI, Chat, inline completions, coding agent, and code review surfaces. Use applyTo: '**' scope. 2. Create docs/surface-portability-notes.md documenting which features are portable vs surface-specific, one concrete portability risk, one false positive, one hard negative, and recommendations for where each kind of guidance should live. Follow the discovered instruction architecture conventions. Apply the changes directly in files. Do not run shell commands and do not use SQL.
```

The rerun used `gpt-5.4`.

## Assessment Scope

The only question being evaluated is:

> Did the produced code changes implement the prompt in a way that follows the repository's surface-strategy conventions and instruction architecture?

## Expected Change Artifacts

Assessment compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `.github/instructions/portable-baseline.instructions.md` (added), `docs/surface-portability-notes.md` (added)
- `.output/change/expected-patterns.json` — required patterns in patch: scope, portable, CLI/surfaces, VS Code, risk taxonomy

## Captured Result

Artifacts used for this assessment:

- `.output/logs/prompt.txt`
- `.output/logs/command.txt`
- `.output/logs/session.md`
- `.output/logs/copilot.log`
- `.output/change/demo.patch`
- `.output/change/changed-files.json`
- `.output/change/comparison.md`

The rerun completed successfully and produced the exact expected file set:

- added `.github/instructions/portable-baseline.instructions.md`
- added `docs/surface-portability-notes.md`

The comparison report shows:

- `Files match: True`
- `Patterns match: True`

All required pattern checks matched, including the `applyTo: '**'` scope, portability emphasis, multi-surface comparison, VS Code-specific distinctions, and explicit risk taxonomy.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes
- Required context applied: Yes

Overall judgment:

- The rerun created both required portability artifacts in the correct locations.
- The generated content matched the expected architecture and portability-shape requirements.
- This run is a complete success for the updated lesson objective.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered fully successful. It created both required artifacts, matched the expected file manifest exactly, and demonstrated the intended cross-surface portability guidance in the generated content.
