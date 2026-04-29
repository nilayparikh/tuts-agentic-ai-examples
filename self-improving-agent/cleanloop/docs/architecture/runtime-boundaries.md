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

## Run

### Commands

```powershell
python util.py status
python util.py reset
python util.py sandbox --timeout 10
```

### Output

```text
$ python util.py status
Environment:
	Python:   3.11.9
	.env:     exists
	Model:    microsoft/Phi-4
	Output:   exists
	Dataset:  finance

$ python util.py reset
Preserved cleanloop/.output sample artifacts
Restored clean_data.py from clean_data_starter.py
Ready to re-run: python util.py loop

$ python util.py sandbox --timeout 10
Running genome in sandbox for finance (timeout=10s)...
	[OK] Genome completed successfully
	CleanLoop Evaluation: 13/14
	[FAIL] matches_reference_output: matched=30, missing=25, unexpected=0, output_rows=30, reference_rows=55
```

### Explanation

1. `python util.py status` confirms the fixed arena and environment boundary before you inspect mutable code.
2. `python util.py reset` demonstrates the starter-baseline boundary directly: the mutable genome is restored, but `.output` evidence is preserved.
3. `python util.py sandbox --timeout 10` shows the containment boundary from [Lesson 07](../lessons/07-production-safety.md). The genome runs in isolation, but the fixed judge still owns the score.
