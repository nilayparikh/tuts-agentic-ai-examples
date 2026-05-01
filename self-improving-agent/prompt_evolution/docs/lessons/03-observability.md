# Lesson 03 - Observability

## Learning Objectives

- Open the dashboard from the local project folder.
- Locate the latest session, trace files, and score history.
- Use status output as a non-UI readiness check.

## Command

```powershell
cd prompt_evolution
python util.py status
python util.py dashboard
```

## Inputs

- `.output/latest_session.json`
- `.output/traces/*.jsonl`
- `.output/best_response.md`

## Outputs

```text
Prompt Evolution Status
  output: present
  latest session: present
  traces: present
```

The dashboard renders score history, prompt changes, response previews, and trace records for the latest loop run.

## Validation

If `dashboard` reports that no latest session exists, run `python util.py loop --max-iterations 1` first. That creates the session file the dashboard reads.

## Summary

Observability is split into a quick CLI status path and the richer Streamlit dashboard. Both work from the local `prompt_evolution` folder.
