# Tracing and Logging

CleanLoop now writes structured traces beside the CSV exports.

## Trace Files

- `.output/traces/run-events.jsonl`
- `.output/traces/row-decisions.jsonl`
- `.output/traces/proposal-events.jsonl`

## Current Trace Coverage

The pipeline currently records:

- run start and finish for `clean_data_runtime.py`
- per-file scans
- deterministic row exports
- starter-stage mutation skips
- mutation fixes
- mutation failures

## Important Fields

- `trace_id`
- `run_id`
- `component`
- `stage`
- `decision`
- `invoice_id`
- `source_file`

## Inline Coding Anchor

```python
trace.record_row_decision(
    stage="mutation-playbook",
    decision="mutation_fixed",
    invoice_id=record["invoice_id"],
    source_file=record["source_file"],
    value=mutated_row["value"],
)
```

This is the teaching bridge between what the cleaner decided and what the learner sees in the exports.
