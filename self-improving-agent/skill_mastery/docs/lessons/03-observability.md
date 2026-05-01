# Lesson 03 - Observability

## Learning Objectives

- Inspect the latest Skill Mastery session.
- Open the dashboard from the local folder.
- Connect selected habits to scored outputs.

## Command

```powershell
cd skill_mastery
python util.py status
python util.py dashboard
```

## Inputs

- `.output/latest_session.json`
- `.output/learned_habits.json`
- `.output/selected_habits.json`
- `.output/traces/*.jsonl`

## Outputs

```text
Skill Mastery Status
  output: present
  latest session: present
  selected habits: present
```

The dashboard shows the selected habit set, score history, response diffs, trace records, and artifact health.

## Validation

If `dashboard` reports that no latest session exists, run `python util.py loop --max-iterations 1` first.

## Summary

Observability explains why the habit-composed answer received its score. The local status command gives a fast readiness check, and the dashboard gives the richer trace view.
