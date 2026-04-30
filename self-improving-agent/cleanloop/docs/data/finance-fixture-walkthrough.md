# Finance Fixture Walkthrough

This example teaches the process with the real shipped finance sample.

## Input Files

- `finance_invoices.csv`
- `finance_invoices_flags.csv`
- `finance_invoices_regional.csv`
- `finance_invoices_collections.csv`
- `finance_invoices_adjustments.csv`

## How To Read The Sample

Start with one deterministic row, one mutation row, and one failure row.

### Deterministic Row

`INV-101` already has a usable amount.

```csv
INV-101,Acme Manufacturing,15000.00,USD,2024-01-15,...,paid
```

That row becomes:

```text
2024-01-15,Acme Manufacturing,USD,15000.0,paid
```

### Mutation Row

`INV-404` keeps required business fields, but the amount is noisy.

```csv
INV-404,Contoso Retail,offset zero  🧾,GBP,2024-07-18,...,disputed
```

The playbook canonicalizes `offset zero  🧾` to `OFFSET`, then reads the
approved `resolution_amount` so the exported row keeps a real signed amount
instead of a placeholder zero.

### Failure Row

`INV-112` carries a real customer and status, but the shipped playbook does not resolve `SEE PDF 📎`.

That row is copied into `finance_mutation_failures.csv` for later mutation work.

## Why This Fixture Works For Teaching

The example is realistic because mutation success is caused by noisy signals,
not by blank core fields, and every shipped mutation-success row is recoverable
from local business metadata such as `resolution_amount` or `adjusted_amount`.
