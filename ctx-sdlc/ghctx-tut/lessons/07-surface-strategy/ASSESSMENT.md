# Lesson 07 — Surface Strategy — Assessment

> **Assessment mode:** static artifact review

## Prompt Under Review

```text
Open the Lesson 07 context pack and explain how application context is
separated into data (context) and format (templates) to serve GitHub Copilot,
Claude Code, and Codex. Identify the context sources, the template shells, the
graph mapping, and the generated outputs. Do not try to run the app. Focus on
the architecture and why each layer exists.
```

## Scorecard

| #   | Dimension                  | Rating  | Summary                                                |
| --- | -------------------------- | ------- | ------------------------------------------------------ |
| 1   | Context Utilization (CU)   | ✅ PASS | Uses context files, templates, graph, and outputs      |
| 2   | Session Efficiency (SE)    | ✅ PASS | Requires reading, comparison, and explanation only     |
| 3   | Prompt Alignment (PA)      | ✅ PASS | Matches the data/format separation teaching goal       |
| 4   | Change Correctness (CC)    | ✅ PASS | Artifact set reflects clean context/template split     |
| 5   | Objective Completion (OC)  | ✅ PASS | Explains polyglot context through architecture         |
| 6   | Behavioral Compliance (BC) | ✅ PASS | Avoids pretending the lesson is a runnable demo        |

**Verdict:** ✅ PASS

## What Good Assessment Looks For

The explanation should identify these layers clearly:

1. `.code.agent/context/*.md` is the single source of reusable application context.
2. `.code.agent/templates/*.tpl` are pure format shells with zero app knowledge.
3. `.code.agent/graph.json` maps context through templates to outputs.
4. `transform.py` generates all tool-facing files from the graph.
5. `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` are generated
   bridges — not hand-maintained canonical sources.
6. Scoped rules (`.github/instructions/*.md` and `.claude/rules/*.md`) share the
   same context but use different structural templates.
7. `docs/` documents the `src/` application, not the context architecture.

## Failure Conditions

Mark the walkthrough as incorrect if it does any of these things:

- claims the lesson must be run to be useful
- claims one entry file is automatically consumed by every tool
- claims the generated output files are the canonical source
- confuses context (data) with templates (format)
- treats templates as containing application knowledge
- ignores the difference between context sources and generated outputs
- explains only GitHub Copilot and skips Claude or Codex
- references deleted files like `docs/requirements/` or `docs/portability-matrix.md`

## Final Judgment

This lesson succeeds when the reviewer can point to the context/template
separation, explain why templates contain zero application knowledge, and show
how the same context produces tool-native outputs for Copilot, Claude, and
Codex.
