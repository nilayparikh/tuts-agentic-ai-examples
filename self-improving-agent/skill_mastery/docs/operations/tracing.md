# Skill Mastery Tracing

Skill Mastery writes observability files beside the saved reply artifacts. The
trace tells you which habits were promoted, which habits were selected, what the
LLM was asked to do, and how the evaluator scored each round.

## Files

```text
skill_mastery/.output/traces/
  run_events.jsonl
  habit_events.jsonl
  llm_requests.jsonl
  evaluator_events.jsonl
  otel_spans.jsonl
  otel_events.jsonl
  otel_logs.jsonl
  runs/<run-instance>/
```

Top-level files collect all runs. The `runs/<run-instance>/` folder stores a
copy for one named run. Use `--named-instance` when you want stable paths for a
demo or test capture.

```bash
python util.py -e skill_mastery loop \
  --usecase makerspace_access_checkpoint \
  --named-instance habit-demo
```

## Event Types

| File                     | What it records                                          |
| ------------------------ | -------------------------------------------------------- |
| `run_events.jsonl`       | Loop start, round start, and loop completion             |
| `habit_events.jsonl`     | Learned and selected habit cards                         |
| `llm_requests.jsonl`     | Draft and revision prompt metadata                       |
| `evaluator_events.jsonl` | Scores, strengths, and issues                            |
| `otel_*.jsonl`           | OTEL-shaped spans, events, and logs for downstream tools |

The dashboard reads the same files. Use the Trace and Habits tabs to explain
why a response changed without opening raw JSON by hand.
