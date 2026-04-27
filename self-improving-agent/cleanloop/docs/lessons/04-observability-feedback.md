# Lesson 04 — Observability and the Feedback Signal

Lesson 04 explains how CleanLoop turns hidden state into visible artifacts.

## What To Inspect

- `.output/finance_eval_history.json`
- `.output/finance_strategy.json`
- `.output/traces/run-events.jsonl`
- `.output/traces/row-decisions.jsonl`

## Code Anchors

- [Dashboard history loader](../../dashboard.py#L58)
- [Shared history store](../../history_store.py#L10)
- [Trace recorder](../../tracing.py#L19)

## Feedback Signal

The learner should read both the referee score and the trace records. The score says whether the run improved. The trace says why one row took one path.

## Inline Coding

```python
trace.record_row_decision(
	stage="mutation-playbook",
	decision="mutation_fixed",
	invoice_id=record["invoice_id"],
	source_file=record["source_file"],
)
```

That trace call is what turns one hidden row decision into a durable teaching artifact.

## Hands-On Exercises

### Exercise 1 - Surface focus area in the dashboard

- Difficulty: Easy
- Files: `dashboard.py`, `loop.py`
- Task: Add `focus_area` and `repeated_failure_count` to the main dashboard history rows so each round explains what it was trying to fix.
- Hints: Normalize `history_entry["metacognition"]` the same way the dashboard already normalizes LLM diagnostics.
- Done when: The history table shows strategy context, not only score movement.
- Stretch: Add a simple severity label when the repeated count is high.

### Exercise 2 - Build a decision breakdown table

- Difficulty: Medium
- Files: `dashboard.py`, `.output/traces/row-decisions.jsonl`
- Task: Parse the row-decision trace file and count rows by `stage` and `decision`.
- Hints: A small `pandas` group-by is enough. Keep the first version read-only and avoid changing the trace format.
- Done when: The dashboard can show how many rows were deterministic, repaired, and unresolved.
- Stretch: Add a filter for `source_file`.

### Exercise 3 - Add invoice drill-down

- Difficulty: Medium
- Files: `dashboard.py`
- Task: Let the operator enter one `invoice_id` and inspect every trace row for that record.
- Hints: Start from `INV-404` or `INV-112` because those are already called out in the docs.
- Done when: One invoice can be followed from input scan to final decision inside the dashboard.
- Stretch: Show the last trace event as a short summary card.

### Exercise 4 - Warn on missing artifacts

- Difficulty: Medium
- Files: `dashboard.py`, `history_store.py`
- Task: Show a visible warning when history, strategy, or trace artifacts are missing on a fresh repo.
- Hints: Reuse existing path helpers and keep the warning actionable by naming the next command to run.
- Done when: The dashboard still feels usable even before the learner has generated outputs.
- Stretch: Add one compact checklist of the commands that produce each missing artifact.
