# Lesson 07 — Surface Strategy Example

This document defines the concrete example used in Lesson 07.

## Objective

Show that a read-only analysis workflow can explain which context belongs in the universal baseline versus surface-specific layers without editing the repository.

## Expected Output Shape

The preferred output for this lesson is a structured analysis with:

1. Summary
2. What is portable across all surfaces
3. What is VS Code-only or limited-surface context
4. One portability risk
5. One false positive
6. One hard negative
7. Prioritized recommendations

## Required Constraints

1. The workflow must remain read-only.
2. The analysis must inspect the relevant baseline instructions, scoped instructions, agent definitions, and lesson docs together.
3. The analysis must compare CLI, VS Code Chat, inline completions, coding agent, and code review explicitly.
4. The analysis must treat `.github/copilot-instructions.md` as the universal baseline and explain why.
5. The analysis must note that `.instructions.md`, agents, prompts, MCP, and hooks are not equally portable.
6. If lesson artifacts disagree, the analysis must identify which one should be treated as canonical and why.
7. The assessment run must not use SQL, task/todo write tools, or other write-capable tools.

## Concrete Scenario

Use the lesson's current files to explain which guidance would still help a user on the widest range of Copilot surfaces and which guidance only works in richer VS Code environments.

## What Good Output Looks Like

Good output will usually:

- identify `.github/copilot-instructions.md` as the most portable layer
- explain why `api.instructions.md` is stronger but less portable than the baseline
- explain why `reviewer.agent.md` is useful in chat/coding-agent contexts but unavailable in CLI and review, or resolve any lesson-local contradiction if the artifacts disagree
- call out one false positive where a CLI limitation is mistaken for missing context
- call out one hard negative where teams put critical guidance only in a non-portable layer
