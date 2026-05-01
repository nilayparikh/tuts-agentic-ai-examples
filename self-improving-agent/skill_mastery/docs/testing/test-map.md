# Skill Mastery Test Map

Focused tests live in `tests/test_skill_mastery.py`. They cover the behavior
that makes the example reliable as a teaching artifact.

## Test Coverage

| Area      | What the tests check                                                    |
| --------- | ----------------------------------------------------------------------- |
| Parser    | `--usecase` is accepted for Skill Mastery loop runs                     |
| Catalog   | Contexts, habit seeds, demonstrations, and use cases load from `.data/` |
| Profiles  | `resolve_usecase_profile` applies the use case context and problem      |
| Learner   | Habits promote only when successful across enough contexts              |
| Selector  | Relevant habit cards are selected for a new support issue               |
| Loop      | LLM metadata, logs, diffs, session output, and traces are saved         |
| Dashboard | JSON and diff helper functions return usable rows                       |

## Commands

```bash
python -m unittest tests.test_skill_mastery
```

Use focused lint and type checks when changing this example:

```bash
.venv\Scripts\pylint --disable=R skill_mastery tests/test_skill_mastery.py util.py
.venv\Scripts\mypy skill_mastery tests/test_skill_mastery.py util.py \
  --ignore-missing-imports --no-warn-unused-ignores
```

The full example suite may include unrelated CleanLoop assertions. Keep Skill
Mastery validation focused unless the task asks for a full repository run.
