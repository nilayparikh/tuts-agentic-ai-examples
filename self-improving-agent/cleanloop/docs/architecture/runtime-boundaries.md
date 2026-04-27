# Runtime Boundaries

CleanLoop is easier to teach when each runtime boundary is explicit.

## Fixed Boundaries

- `prepare.py` is the fixed judge.
- `.gold/finance_expected.csv` is the canonical reference output.
- `.input/*.csv` is the current finance arena.

## Mutable Boundaries

- `clean_data.py` is the mutable genome.
- `clean_data_starter.py` is the deterministic-only reset baseline.
- `loop.py` is the bounded mutation orchestrator.

## Helper Modules

The teaching surface is now root-first.

- `status_snapshot.py` supports the CLI status view
- `input_loader.py`, `date_normalizer.py`, `mutation_playbook.py`, and `export_writer.py` support the cleaning runtime
- `history_store.py` and `tracing.py` support observability
- `reset_workflow.py` keeps recovery logic small and explicit

## Why This Split Matters

Learners should be able to start at the root runtime files and step into a helper only when a single job needs more focus.
