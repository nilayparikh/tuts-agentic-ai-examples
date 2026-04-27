# Failure Cases

Not every noisy row should be repaired automatically.

## Shipped Unresolved Rows

The current fixture leaves five rows unresolved.

- `INV-112` → `SEE PDF 📎`
- `INV-214` → `MANUAL ONLY 🧾`
- `INV-312` → `CHARGEBACK ⚠`
- `INV-412` → `ESCALATE TO TREASURY 🚫`
- `INV-510` → `CHECK ATTACHMENT 📎`

## Why They Stay In The Failure Dump

These tokens do not have a safe numeric resolution in the shipped playbook.
The correct teaching move is to surface them with diagnostics, not to guess.

## Failure Export Schema

`finance_mutation_failures.csv` keeps the raw fields a learner needs to inspect the miss.

```text
source_file, invoice_id, customer, raw_date, raw_amount, currency, status, anomaly_reason, mutation_hint
```

## Lesson Tie-In

Lesson 05 uses these misses to explain why the fixed judge and the challenger matter.
