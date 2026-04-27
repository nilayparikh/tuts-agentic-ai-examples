# Lesson 02 — Defining the Pipeline Genome

Lesson 02 is the heart of the example.

## What Learners Follow

- read the finance rows
- normalize direct numeric amounts
- apply the bounded mutation playbook to noisy amount tokens
- write master, success, and failure exports
- evaluate the result with the fixed referee

## Actual Records To Trace

- `INV-101`
- `INV-404`
- `INV-502`
- `INV-203`
- `INV-112`

## Code Anchors

- [Runtime entrypoint](../../clean_data_runtime.py#L28)
- [Numeric normalization decision](../../mutation_playbook.py#L106)
- [Mutation playbook repair](../../mutation_playbook.py#L144)
- [Stable export writer](../../export_writer.py#L12)

## Inline Coding

```python
value, anomaly_reason = normalize_numeric_amount(record)
```

That line decides whether a row stays deterministic, requires mutation, or must be routed to the failure dump.

## Read This In Order

1. Read [clean_data_runtime.py#L28](../../clean_data_runtime.py#L28) for the full row-routing flow.
2. Step into [mutation_playbook.py#L106](../../mutation_playbook.py#L106) when the amount token is the main question.
3. Step into [mutation_playbook.py#L144](../../mutation_playbook.py#L144) to see how repaired rows are built.
4. Finish with [export_writer.py#L12](../../export_writer.py#L12) to understand why the CSV output order stays stable.

## Hands-On Exercises

### Exercise 1 - Support accounting parentheses

- Difficulty: Medium
- Files: `mutation_playbook.py`
- Task: Extend numeric normalization so a value like `(125.50)` is treated as `-125.5` instead of falling into the mutation path.
- Hints: Keep the change near `normalize_numeric_amount()` so deterministic numeric cleanup still happens before rule lookup.
- Done when: A copied input row with parentheses lands in `finance_master.csv` with a numeric negative value.
- Stretch: Also accept spaced variants such as `( 125.50 )`.

### Exercise 2 - Add one new mutation rule

- Difficulty: Medium
- Files: `mutation_playbook.py`, `.input/*.csv`
- Task: Create one synthetic anomaly row and teach the playbook how to repair it from local business context such as `adjusted_amount` or `resolution_amount`.
- Hints: Add the rule through the existing mutation-rule lookup instead of adding a one-off branch in the runtime.
- Done when: Your new row moves from `finance_mutation_failures.csv` into `finance_mutation_success.csv`.
- Stretch: Make the rule conditional on `status` so it cannot fire on unrelated rows.

### Exercise 3 - Improve failure hints

- Difficulty: Medium
- Files: `mutation_playbook.py`, `clean_data_runtime.py`
- Task: Replace one generic failure hint with a more specific operator hint that points to the exact missing field or bad token.
- Hints: Compare the current paths for `missing_adjusted_amount`, `missing_resolution_amount`, and `unparseable_date`.
- Done when: The failure export tells the learner what to inspect next instead of only saying that the row failed.
- Stretch: Tailor the hint to the row status as well as the anomaly type.

### Exercise 4 - Trace the repair strategy

- Difficulty: Hard
- Files: `mutation_playbook.py`, `clean_data_runtime.py`, `tracing.py`
- Task: Add a `repair_strategy` or `rule_name` field to mutation trace records so later tooling can group rows by the rule that fixed them.
- Hints: Return the extra field from `apply_mutation_playbook()` and write it with `trace.record_row_decision()`.
- Done when: `.output/traces/row-decisions.jsonl` shows which rule repaired each mutation success.
- Stretch: Record the same field for mutation failures so you can see which rules almost matched.
