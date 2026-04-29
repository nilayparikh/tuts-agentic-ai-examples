# Export Contract

The finance export contract is the non-negotiable output shape for CleanLoop.

## Canonical Columns

All success exports use this schema:

```text
date, entity, currency, value, category
```

## Files

- `finance_master.csv`: deterministic rows plus mutation-fixed rows
- `finance_mutation_success.csv`: only rows repaired by the shipped playbook
- `finance_mutation_failures.csv`: unresolved rows with raw diagnostic fields

## Contract Examples

Deterministic success:

```text
2024-01-15,Acme Manufacturing,USD,15000.0,paid
```

Mutation success:

```text
2024-08-14,Blue Yonder,USD,11890.0,paid
```

Unresolved failure:

```text
finance_invoices_regional.csv,INV-312,Blue Yonder,2024-06-24,CHARGEBACK ⚠,USD,disputed,unmapped_amount_token,No shipped mutation rule matches this token.
```

## Governing Tests

- `tests/test_cleanloop_exports.py`
- `tests/test_python_compat.py`

These tests are the fastest way to confirm the docs still match the real behavior.

## Run

### Commands

```powershell
python util.py reset
python util.py evaluate
Get-Content ".output\finance_master.csv" -TotalCount 3
Get-Content ".output\finance_mutation_success.csv" -TotalCount 2
Get-Content ".output\finance_mutation_failures.csv" -TotalCount 2
```

### Output

```text
$ python util.py reset
Preserved cleanloop/.output sample artifacts
Restored clean_data.py from clean_data_starter.py
Ready to re-run: python util.py loop

$ python util.py evaluate
Ran genome. Output: Y:\.sources\localm-tuts\courses\_examples\self-improving-agent\cleanloop\.output\finance_master.csv
	CleanLoop Evaluation: 13/14
	[FAIL] matches_reference_output: matched=30, missing=25, unexpected=0, output_rows=30, reference_rows=55

$ Get-Content ".output\finance_master.csv" -TotalCount 3
date,entity,currency,value,category
2024-01-15,Acme Manufacturing,USD,15000.0,paid
2024-01-18,Globex Retail,USD,8500.5,paid

$ Get-Content ".output\finance_mutation_success.csv" -TotalCount 2
date,entity,currency,value,category

$ Get-Content ".output\finance_mutation_failures.csv" -TotalCount 2
source_file,invoice_id,customer,raw_date,raw_amount,currency,status,anomaly_reason,mutation_hint
finance_invoices.csv,INV-105,Soylent Foods,2024-03-15,FREE   TRIAL 🎁,USD,active,requires_mutation_playbook,Starter genome stops at the deterministic pass.
```

### Explanation

1. Reset first so you know the exported files came from the deterministic starter genome, not from a previous mutation attempt.
2. `python util.py evaluate` writes the contract outputs and immediately scores them. That makes the contract visible in two places at once: the generated CSVs and the fixed-referee summary.
3. The `Get-Content` commands let you inspect the concrete contract surfaces directly: canonical success columns in `finance_master.csv` and diagnostic columns in `finance_mutation_failures.csv`.
4. Cross-check this doc with [Lesson 02](../lessons/02-pipeline-genome.md) for row routing and [Lesson 05](../lessons/05-judge-self-challenging.md) for the fixed judge boundary.
