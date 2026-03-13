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

| File | Type | Purpose |
| --- | --- | --- |
| `.github/agents/planner.agent.md` | Agent | Read-only investigator |
| `.github/prompts/investigate-bug.prompt.md` | Prompt | Bug investigation workflow |
| `.github/prompts/plan-feature.prompt.md` | Prompt | Feature planning workflow |
| `.github/prompts/triage-incident.prompt.md` | Prompt | Incident triage workflow |

## Context Files

| Path | Purpose |
| --- | --- |
| `docs/architecture.md` | System architecture reference |
| `docs/adr/ADR-003-frontend-state.md` | Architecture decision record |
| `specs/product-spec-notification-preferences.md` | Product specification |
| `specs/non-functional-requirements.md` | NFR constraints |
| `specs/bug-report.md` | Sample bug report |
| `specs/feature-request.md` | Sample feature request |

## Copilot CLI Workflow

Investigate a bug:

```bash
copilot -p "Investigate specs/bug-report.md. Trace the data flow for stale notification preference data and identify likely root causes." --allow-all-tools
```

Plan a feature:

```bash
copilot -p "Read specs/product-spec-notification-preferences.md and specs/non-functional-requirements.md. Plan the implementation and list the files that would need to change." --allow-all-tools
```

Expected outcome: the CLI can produce a useful plan, but it does not expose the same custom planner-agent workflow as VS Code.

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
