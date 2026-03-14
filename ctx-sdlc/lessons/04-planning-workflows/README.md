# Lesson 04 — Planning Workflows

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Read-only planning, investigation, and triage workflows using custom agents and prompt files.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Planning workflows use read-only agents and prompt files that combine docs,
specs, and codebase context to produce structured plans without editing code.

| File                                        | Type   | Purpose                    |
| ------------------------------------------- | ------ | -------------------------- |
| `.github/agents/planner.agent.md`           | Agent  | Read-only investigator     |
| `.github/prompts/investigate-bug.prompt.md` | Prompt | Bug investigation workflow |
| `.github/prompts/plan-feature.prompt.md`    | Prompt | Feature planning workflow  |
| `.github/prompts/triage-incident.prompt.md` | Prompt | Incident triage workflow   |

## Context Files

| Path                                             | Purpose                                                 |
| ------------------------------------------------ | ------------------------------------------------------- |
| `docs/architecture.md`                           | System architecture reference                           |
| `docs/adr/ADR-003-frontend-state.md`             | Architecture decision record                            |
| `specs/product-spec-notification-preferences.md` | Product specification                                   |
| `specs/non-functional-requirements.md`           | NFR constraints                                         |
| `specs/bug-report.md`                            | Sample bug report                                       |
| `specs/feature-request.md`                       | Sample feature request                                  |
| `docs/planning-workflow-example.md`              | Concrete lesson-04 demo target and planning constraints |

## Example Goal

This lesson should demonstrate planning quality, not implementation speed.

For this example, the intended outcome is:

- investigate the notification preferences feature request in a read-only workflow
- inspect the relevant lesson docs, specs, and code surfaces first instead of relying on a hardcoded file checklist
- synthesize architecture, ADR, product spec, and NFR constraints into a structured implementation plan
- explicitly separate product requirements from inferred implementation choices
- produce open questions, task breakdown, validation steps, risks, and hidden complexity without editing code or using any write-capable tools

## Copilot CLI Workflow

Investigate a bug:

```bash
copilot -p "Investigate specs/bug-report.md. Trace the data flow for stale notification preference data and identify likely root causes." --allow-all-tools
```

Plan a feature:

```bash
copilot -p "Inspect the relevant docs/, specs/, and existing source surfaces for notification preferences in this lesson before answering. Discover the architecture, ADR, product, and NFR context you need rather than assuming a fixed file list. Produce a read-only implementation plan with source-backed confirmed requirements, open questions with file references, inferred implementation choices, constraints, numbered tasks with acceptance criteria and source refs, validation steps, and risks. If the sources overlap or conflict, identify the canonical source for the plan and explain why. Do not use SQL, task/todo write tools, or any other write-capable tools." --allow-all-tools --deny-tool=sql
```

Expected outcome:

- the CLI produces a structured plan without modifying files
- the CLI stays inside read-only tools and does not create planning todos or other side effects
- the plan cites FR, SC, ADR, and NFR sources instead of giving a shallow task list
- the plan explains which source should be treated as canonical if multiple lesson artifacts overlap or conflict
- the plan surfaces hidden complexity such as delegated sessions, LEGAL-218, fail-closed audit behavior, and degraded-mode fallback

## VS Code Chat Workflow

Use the `@planner` agent for read-only investigation.

Suggested prompts:

```text
Investigate the bug described in specs/bug-report.md. Trace the data flow from the frontend save action through the API to the database and identify where stale data could be served.
```

```text
Plan the implementation of notification preferences per specs/product-spec-notification-preferences.md and specs/non-functional-requirements.md.
```

```text
Users report 500 errors on the notification preferences page during peak hours. Triage the incident and produce a root-cause hypothesis.
```

Expected result: the planner agent searches the codebase and specs, then returns a structured plan without editing files.

## Cleanup

```bash
python util.py --clean
```
