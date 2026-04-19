#!/usr/bin/env python3
"""Lesson 07 walkthrough helper.

This lesson is a static context specimen. The helper prints a short summary of
the files you should open during the walkthrough.
"""

from __future__ import annotations

import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parent

WALKTHROUGH_FILES = [
    (".code.agent/context/app-identity.md", "Application identity, stack, source map, shared rules."),
    (".code.agent/context/backend.md", "Backend contract: layering, middleware, error handling."),
    (".code.agent/context/frontend.md", "Frontend contract: stack, routing, rendering, API boundary."),
    (".code.agent/context/testing.md", "Testing contract: stack, intent, change rules."),
    (".code.agent/context/api-routes.md", "API route contract: handler pattern, middleware, errors."),
    (".code.agent/context/delivery-workflow.md", "Delivery workflow context for the skill."),
    (".code.agent/context/change-planning.md", "Change planning context for the prompt."),
    (".code.agent/context/reviewer-checklist.md", "Reviewer checklist context for the agent."),
    (".code.agent/context/context-guard.md", "Hook configuration context."),
    (".code.agent/graph.json", "Maps context through templates to outputs."),
    ("transform.py", "Generation engine: context + template → output."),
    ("AGENTS.md", "Generated shared projection (Codex/humans)."),
    ("CLAUDE.md", "Generated Claude bridge (imports @AGENTS.md)."),
    (".github/copilot-instructions.md", "Generated Copilot bridge."),
    (".github/instructions/backend.instructions.md", "Generated Copilot backend rule."),
    (".github/instructions/frontend.instructions.md", "Generated Copilot frontend rule."),
    (".github/instructions/tests.instructions.md", "Generated Copilot testing rule."),
    (".github/instructions/api.instructions.md", "Generated Copilot API route rule."),
    (".claude/rules/backend.md", "Generated Claude backend rule."),
    (".claude/rules/frontend.md", "Generated Claude frontend rule."),
    (".claude/rules/tests.md", "Generated Claude testing rule."),
    (".claude/rules/api.md", "Generated Claude API route rule."),
    (".github/agents/reviewer.agent.md", "Generated reviewer agent."),
    (".github/skills/loan-workbench-delivery/SKILL.md", "Generated delivery skill."),
    (".github/prompts/implement-loan-workbench-change.prompt.md", "Generated planning prompt."),
    (".github/hooks/context-guard.json", "Generated context guard hook."),
    ("docs/architecture.md", "Application architecture documentation."),
    ("docs/api-reference.md", "Application API reference."),
    ("docs/feature-map.md", "Feature-to-source mapping."),
    ("docs/data-model.md", "Domain entities and storage."),
]


def print_summary() -> int:
    """Print the lesson walkthrough summary."""
    print("Lesson 07 is a walkthrough, not a runnable demo.")
    print()
    print("Open these files in order:")
    for relative_path, description in WALKTHROUGH_FILES:
        full_path = LESSON / relative_path
        exists_flag = "OK" if full_path.exists() else "MISSING"
        print(f"- {relative_path} [{exists_flag}] - {description}")
    return 0


def print_usage() -> int:
    """Print the accepted command line usage."""
    print("Usage: python util.py --summary")
    return 1


def main() -> int:
    """Parse arguments and run the requested helper action."""
    if len(sys.argv) != 2 or sys.argv[1] != "--summary":
        return print_usage()
    return print_summary()


if __name__ == "__main__":
    raise SystemExit(main())
