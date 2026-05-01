# Lesson 01 - Local Runner

## Learning Objectives

- Run Skill Mastery Studio from its own folder.
- Confirm the habit catalog and use cases load.
- Understand how the project resolves `.env` and `.venv`.

## Command

```powershell
cd skill_mastery
python util.py catalog
python util.py usecases
python util.py status
```

## Inputs

- `.data/context_packs.json`
- `.data/habit_definitions.json`
- `.data/demonstrations.json`
- `.data/usecases.json`
- `.env` or the shared parent `../.env`

## Outputs

```text
Contexts:
- makerspace_frontdesk: Makerspace Front Desk

Habit seeds:
- mirror_issue: Mirror the customer issue

Use cases:
- makerspace_access_checkpoint: Makerspace Access Checkpoint
```

## Validation

This lesson validates local project self-containment. Commands run from `skill_mastery`, not from the parent example folder.

## Summary

The local `util.py` is the command surface for Skill Mastery. It exposes catalog, use case, loop, dashboard, sandbox, challenge, evaluate, and autonomy workflows from the project directory.
