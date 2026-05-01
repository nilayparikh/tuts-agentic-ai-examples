# Skill Mastery Code Map

This map shows where each piece of the Skill Mastery example lives.

| File                    | Role                                                         |
| ----------------------- | ------------------------------------------------------------ |
| `config.py`             | Loads contexts, habits, demonstrations, and named use cases  |
| `learner.py`            | Promotes reusable habits from successful demonstrations      |
| `selector.py`           | Chooses habit cards for the active profile                   |
| `evaluator.py`          | Scores policy grounding, habit signals, and forbidden claims |
| `loop.py`               | Orchestrates Hermes drafting, revision, outputs, and traces  |
| `tracing.py`            | Writes JSONL and OTEL-shaped observability artifacts         |
| `dashboard.py`          | Shows use case, habit, trace, diff, and LLM request views    |
| `.data/usecases/*.json` | Repeatable support cases for demos and regression tests      |

## Output Ownership

`loop.py` owns `.output/` artifacts. It writes the user-facing reply, selected
habit notes, session JSON, and mutation diff. `tracing.py` owns only trace files
under `.output/traces/`.

## Shared Entry Point

`util.py` is the only CLI entry point. Skill Mastery-specific commands are:

```bash
python util.py -e skill_mastery catalog
python util.py -e skill_mastery usecases
python util.py -e skill_mastery loop --usecase makerspace_access_checkpoint
python util.py -e skill_mastery dashboard
python util.py -e skill_mastery reset
```
