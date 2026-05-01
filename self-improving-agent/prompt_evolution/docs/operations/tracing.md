# Tracing and Observability

Prompt Evolution writes runtime artifacts to `.output/`. The main learner files
are still `latest_session.json`, `best_response.md`, `best_instructions.md`,
and `latest_mutation.diff`. The advanced trace layer adds JSONL files under
`.output/traces/`.

| Artifact                        | Purpose                                                  |
| ------------------------------- | -------------------------------------------------------- |
| `traces/run_events.jsonl`       | Loop start, round start, mutation, and completion events |
| `traces/llm_requests.jsonl`     | Draft and mutation request summaries                     |
| `traces/evaluator_events.jsonl` | Deterministic score, issues, and strengths per round     |
| `traces/otel_spans.jsonl`       | OTEL-shaped span records                                 |
| `traces/otel_events.jsonl`      | OTEL-shaped event records                                |
| `traces/otel_logs.jsonl`        | OTEL-shaped log records                                  |
| `traces/runs/<run>/`            | Per-run copies for named or generated run instances      |

Use `--named-instance` when you want a stable trace folder:

```bash
python util.py -e prompt_evolution loop --scenario makerspace_missing_booking \
  --named-instance workshop-demo
```

The dashboard reads the session, trace, evaluator, LLM, and diff artifacts:

```bash
python util.py -e prompt_evolution dashboard
```

## What To Inspect

Start with the dashboard overview. It shows round scores and the final response.
Then open the Trace tab. The trace table shows whether the loop drafted,
scored, mutated, or stopped. The LLM Requests tab shows prompt and response
character counts. The Diff tab shows how the instruction artifact changed.

This gives the support-desk agent the same operational feel as CleanLoop. You
can explain not only what answer won, but why the loop changed direction.
