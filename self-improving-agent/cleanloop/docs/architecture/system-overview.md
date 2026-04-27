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
