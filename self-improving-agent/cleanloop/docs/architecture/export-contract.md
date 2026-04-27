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
