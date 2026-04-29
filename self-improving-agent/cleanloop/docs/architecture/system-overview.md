# CleanLoop System Overview

This document explains the full CleanLoop flow for the course `Building the Self-Evolving Data Engineer`.

## Core Flow

CleanLoop runs one bounded pipeline against the finance fixture.

1. Read the five CSV inputs in `.input/`.
2. Normalize already-numeric rows into the canonical export schema.
3. Apply a bounded mutation playbook to noisy but populated amount fields.
4. Write three exports:
   - `finance_master.csv`
   - `finance_mutation_success.csv`
   - `finance_mutation_failures.csv`
5. Evaluate the outputs with the fixed referee in `prepare.py`.
6. Let the orchestrator in `loop.py` decide whether a mutation survives.

## Actual Fixture Shape

The shipped sample contains 60 input rows across five files.

- 30 rows succeed in the deterministic pass.
- 25 rows succeed through the shipped mutation playbook.
- 5 rows stay unresolved and remain in the failure dump.

That means the expected outputs are:

- `finance_master.csv`: 55 rows
- `finance_mutation_success.csv`: 25 rows
- `finance_mutation_failures.csv`: 5 rows

## Representative Records

- `INV-101`: a direct deterministic success
- `INV-404`: a noisy token that canonicalizes to `OFFSET`
- `INV-502`: a mutation success that reads `adjusted_amount`
- `INV-203`: a mutation success that reads `resolution_amount`
- `INV-112`: a true unresolved failure

## Teaching Boundary

The model never owns correctness. The model proposes code. The fixed referee owns score and pass or fail.

## Detailed Traced Flow

For the full function-by-function execution path derived from current `.output/`
artifacts, see [execution-flow.md](execution-flow.md).

## Run

### Commands

```powershell
python util.py status
python util.py verify
python util.py evaluate
python util.py loop --max-iterations 1
```

### Output

```text
$ python util.py status
Input Files:
   finance_invoices.csv               12 rows
   ...
   finance_invoices_adjustments.csv   12 rows
Environment:
   Python:   3.11.9
   .env:     exists
   Model:    microsoft/Phi-4
   Dataset:  finance

$ python util.py verify
Result: 4/4 checks passed.
Ready for: python util.py loop

$ python util.py evaluate
Ran genome. Output: Y:\.sources\localm-tuts\courses\_examples\self-improving-agent\cleanloop\.output\finance_master.csv
   CleanLoop Evaluation: 13/14
   [FAIL] matches_reference_output: matched=30, missing=25, unexpected=0, output_rows=30, reference_rows=55

$ python util.py loop --max-iterations 1
[CURRENT_SCORE] Score 13/14
[METACOGNITION] Focus row_reconciliation: Compare missing and unexpected rows to see which transformations are still dropping or inventing records.
[REVERT_MUTATION] Reverted mutation with score 0/1
History saved to Y:\.sources\localm-tuts\courses\_examples\self-improving-agent\cleanloop\.output\finance_eval_history.json
```

### Explanation

1. The first two commands are the same readiness gate used in [Lesson 01](../lessons/01-mutation-engine.md). Validate the fixture shape and provider health before you reason about architecture.
2. `python util.py evaluate` recreates the baseline described in [Lesson 02](../lessons/02-pipeline-genome.md): the starter genome writes a real export but still misses 25 reference rows.
3. `python util.py loop --max-iterations 1` exercises the round-level control path from [Lesson 03](../lessons/03-orchestrator.md). The key architecture check is that the loop records history and reverts a non-improving candidate.
4. If you need the function-by-function path behind those lines, continue into [execution-flow.md](execution-flow.md).
