# Lesson 06 — Guardrail Audit Example

This document defines the concrete example used in Lesson 06.

## Objective

Show that a read-only audit workflow can inspect the lesson's hook, MCP, and policy files and identify real enforcement gaps without modifying the repository.

## Expected Output Shape

The preferred output for this lesson is a structured audit with:

1. Summary
2. Confirmed controls
3. Inconsistencies with file references
4. False positives
5. Hard negatives
6. Prioritized fixes
7. Residual risks

## Required Constraints

1. The workflow must remain read-only.
2. The audit must inspect the hook JSON, hook scripts, MCP config, Copilot instructions, and the policy docs together.
3. The audit must explicitly compare documented protected files with actual hook enforcement.
4. The audit must explicitly compare documented trust boundaries with actual MCP scope.
5. The audit must mention fail-closed audit semantics and the 404-not-403 feature-flag rule.
6. The audit must call out what the CLI cannot validate because VS Code hooks do not execute in the CLI run.
7. The audit must include at least one hard negative and one false positive.
8. The audit must identify the canonical artifact when policy documentation and enforcement logic disagree.
9. The assessment run must not use SQL, task/todo write tools, or other write-capable tools.

## Concrete Scenario

Use the lesson's current hook, MCP, and policy files to determine whether the documented guardrails match the actual enforcement code.

Good output should identify mismatches rather than just repeating the intended policy.

## What Good Output Looks Like

Good output will usually:

- compare `docs/security-policy.md` against `.github/scripts/check_protected_files.py`
- compare `docs/tool-trust-boundaries.md` and `.github/copilot-instructions.md` against `.github/mcp.json`
- explain which controls are purely static documentation and which ones are actually enforced by scripts or runtime hooks
- note that CLI analysis cannot substitute for a live VS Code hook demonstration
