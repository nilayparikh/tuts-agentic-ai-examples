# Surface Portability Notes

This lesson currently contains these relevant surface-strategy artifacts:

- `.github/copilot-instructions.md` — universal baseline instructions
- `.github/instructions/api.instructions.md` — path-scoped route rules
- `.github/agents/reviewer.agent.md` — reviewer role and checklist
- `docs/cli-guide.md` — CLI behavior and usage notes
- `docs/portability-matrix.md` — surface compatibility reference
- `docs/surface-strategy-example.md` — lesson-specific target and constraints

No prompt files, MCP configuration, or hook artifacts are present in this
lesson directory today, so portability analysis here is based on the baseline
instruction, the scoped instruction, the agent, and the docs.

## Portable vs Surface-Specific

| Artifact or feature | Present here | Portability | Notes |
| --- | --- | --- | --- |
| `.github/copilot-instructions.md` | Yes | Portable | This is the universal baseline and the only lesson artifact explicitly positioned to work across CLI, Chat, inline completions, coding agent, and code review. |
| `.github/instructions/*.instructions.md` with `applyTo` | Yes | Surface-specific | Useful for scoped activation in supported editors and coding agent flows, but not a reliable cross-surface baseline. |
| `.github/agents/*.agent.md` | Yes | Surface-specific | Agent files define a role and checklist, but they are not a portable foundation. |
| `docs/*.md` reference docs | Yes | Partially portable | Helpful as discoverable knowledge, but not guaranteed to auto-load on every surface. |
| Prompt files | No | Surface-specific | Not present here; if added later, they should be treated as workflow helpers rather than universal guidance. |
| MCP configuration | No | Surface-specific | Not present here; if added later, it should be treated as a tool availability layer, not baseline policy. |
| Hooks | No | Surface-specific | Not present here; if added later, they would enforce editor-side behavior rather than provide portable context. |

## Canonical Baseline

Treat `.github/copilot-instructions.md` as the canonical cross-surface
instruction source for this lesson.

That conclusion is supported by multiple lesson artifacts:

- `README.md` labels it the "Universal baseline".
- `docs/cli-guide.md` says it is the only context file guaranteed to load in
  the CLI.
- `docs/portability-matrix.md` places it at the base of the portability
  pyramid.

There is one lesson-level disagreement about agent portability. The portability
matrix says `.agent.md` is available in VS Code Chat and coding agent, while
`README.md` and the note inside `reviewer.agent.md` speak more narrowly about
VS Code Chat usage. For portability decisions, `docs/portability-matrix.md`
should be treated as canonical because it is the dedicated compatibility
reference, while the README and agent note are explanatory summaries.

## Why the New Portable Baseline Is Smaller

The route template in `.github/instructions/api.instructions.md` is stronger
than the portable baseline, but it is intentionally scoped to
`app/backend/src/routes/**`.

The reviewer checklist in `.github/agents/reviewer.agent.md` is also stronger,
but it depends on agent-style role framing and tool assumptions.

For that reason, the extracted portable baseline should keep only guidance that
still makes sense everywhere:

- project and stack identity
- architecture boundaries
- fail-closed audit ordering
- universal coding conventions
- error-shape and logging rules

It should not copy route-only templates or agent-only review workflow details
into the universal layer.

## Portability Risk Taxonomy

### Concrete portability risk

A team could place the route error-handling requirements only in
`.github/instructions/api.instructions.md` and assume CLI or code review will
enforce them. That creates inconsistent behavior because surfaces that do not
load scoped instructions may still generate code, comments, or review output
without the same guarantees.

### False positive

A developer may notice that the CLI did not apply the reviewer checklist and
conclude that the repository baseline is broken. In this lesson, that is a
false positive: the missing checklist can be caused by the CLI not loading the
agent layer, not by missing or incorrect universal instructions.

### Hard negative

Putting a must-follow universal rule such as "no stack traces in error
responses" only in an agent file or only in a path-scoped instruction is a hard
negative. That guidance becomes unavailable on surfaces that do not support the
chosen layer, so the most critical rule is absent exactly where portability was
required.

## Recommendations

Put universal project identity, architecture boundaries, security rules, error
shape requirements, and logging conventions in
`.github/copilot-instructions.md`.

Put file-pattern-specific implementation guidance in
`.github/instructions/*.instructions.md`. In this lesson, the route handler
template belongs there, not in the portable baseline.

Put role-based review behavior, checklists, and tool-constrained workflows in
`.github/agents/*.agent.md`.

Put explanatory reference material, rationale, examples, and compatibility
tables in `docs/*.md`.

If prompt files, MCP, or hooks are added later, treat them as surface-specific
enhancement layers. They can improve supported surfaces, but they should not be
the only home for guidance that the whole team depends on.
