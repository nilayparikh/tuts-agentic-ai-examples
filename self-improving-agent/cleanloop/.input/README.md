# CleanLoop Input Data

CleanLoop now uses one finance arena. The genome always reads these five CSVs
and writes one master file with this schema:

```text
date, entity, currency, value, category
```

## Files

| File                               | Purpose                                                |
| ---------------------------------- | ------------------------------------------------------ |
| `finance_invoices.csv`             | Base ledger with blanks, refunds, and text amounts     |
| `finance_invoices_flags.csv`       | Flags, review codes, placeholders, and outliers        |
| `finance_invoices_regional.csv`    | Regional fields, mixed currencies, and mixed dates     |
| `finance_invoices_collections.csv` | Collections metadata, escalations, and disputed values |
| `finance_invoices_adjustments.csv` | Reversals, adjustments, approval markers, and outliers |

The point of the arena is progression, not routing. Each file adds another kind
of mess while keeping the same target output.
