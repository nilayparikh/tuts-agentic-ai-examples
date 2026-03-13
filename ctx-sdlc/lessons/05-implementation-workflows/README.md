# Lesson 05 — Implementation Workflows

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Specialized agents for implementation, review, and testing with different tool access and responsibilities.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Three agents with different capabilities form an implementation workflow.

| Agent | Tools | Role |
| --- | --- | --- |
| `implementer` | edit, terminal, code search, problems | Writes and runs code |
| `reviewer` | code search, problems, usages | Reviews without editing |
| `tester` | edit, terminal, tests, failure analysis | Writes and runs tests |

This lesson also includes a TDD skill and prompt files for structured implementation and review.

## Context Files

| Path | Purpose |
| --- | --- |
| `.github/agents/implementer.agent.md` | Implementation agent definition |
| `.github/agents/reviewer.agent.md` | Review agent definition |
| `.github/agents/tester.agent.md` | Testing agent definition |
| `.github/prompts/implement-feature.prompt.md` | Feature implementation workflow |
| `.github/prompts/review-changes.prompt.md` | Review workflow |
| `.github/skills/tdd-workflow/SKILL.md` | TDD skill |
| `docs/implementation-playbook.md` | Implementation standards |
| `specs/non-functional-requirements.md` | NFR constraints |

## Copilot CLI Workflow

The CLI cannot switch into custom agents, but it can still provide a baseline implementation prompt.

```bash
copilot -p "Implement a notification preferences API endpoint. Users can set per-event channel preferences (email, SMS). Follow TDD and repository conventions." --allow-all-tools
```

For review-oriented prompting:

```bash
copilot -p "Review the notification preferences implementation for security issues, missing audit entries, and NFR compliance." --allow-all-tools
```

Expected outcome: useful baseline guidance, but no real multi-agent separation.

## VS Code Chat Workflow

Implement with `@implementer`:

```text
Implement the notification preferences feature from specs/non-functional-requirements.md. Create the route, business rules, and service layer.
```

Test with `@tester`:

```text
Write tests for the notification preferences feature. Follow TDD and verify they pass.
```

Review with `@reviewer`:

```text
Review the notification preferences implementation. Check for security issues, missing audit entries, and NFR compliance.
```

You can also run the prompt file workflow for feature implementation and review.

## Cleanup

```bash
python util.py --clean
```
