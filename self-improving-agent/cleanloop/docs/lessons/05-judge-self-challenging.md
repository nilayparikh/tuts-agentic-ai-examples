# Lesson 05 — The Judge and Self-Challenging Loops

Lesson 05 explains why the fixed judge and the challenger belong together.

## Judge Rule

The model does not grade itself. `prepare.py` and the reference export stay fixed.

## Challenger Rule

The challenger generates harder anomaly inputs when the loop becomes too comfortable.

## Code Anchors

- [Fixed referee](../../prepare.py#L324)
- [Challenger generator](../../challenger.py#L106)

## Inline Coding

```python
results = prepare.evaluate(output)
```

That line matters because the loop never grades itself. The scorer stays fixed, even when the genome changes.

## Hands-On Exercises

### Exercise 1 - Add a judge rule for failure quality

- Difficulty: Medium
- Files: `prepare.py`
- Task: Add one assertion that fails when a mutation-failure row is missing `anomaly_reason` or `mutation_hint`.
- Hints: Keep the check beside the other binary judge rules so the contract stays readable.
- Done when: Blank failure diagnostics make the fixed judge fail.
- Stretch: Also reject placeholder hints such as `unknown` or `todo`.

### Exercise 2 - Add a mutation coverage metric

- Difficulty: Medium
- Files: `prepare.py`
- Task: Compute how many rows ended in deterministic success, mutation success, and mutation failure, then expose that split in `results["metrics"]`.
- Hints: The judge already loads the optional success and failure exports. Reuse those counts instead of rescanning the inputs.
- Done when: The evaluation result includes a stable mutation-coverage view that later tools can print.
- Stretch: Surface the same numbers in the dashboard.

### Exercise 3 - Harden one challenger difficulty

- Difficulty: Hard
- Files: `challenger.py`
- Task: Strengthen one difficulty prompt so it produces finance-specific anomalies that the current playbook does not solve yet.
- Hints: Parentheses, blank cancellations, and mixed currency tokens are better targets than random CSV corruption.
- Done when: The challenger produces a new failure mode that is still understandable and debuggable.
- Stretch: Add a short note on which assertion you expect to fail first.

### Exercise 4 - Improve the genome without moving the goalposts

- Difficulty: Hard
- Files: `prepare.py`, `clean_data.py`, `.input/*.csv`
- Task: Run one challenge set, capture the baseline failure list, then improve only the genome-side handling against the same judge.
- Hints: Treat `prepare.py` as frozen once you record the baseline. The whole point is to keep selection pressure fixed.
- Done when: The score improves against the exact same judge contract.
- Stretch: Save a before-and-after note with the failing assertions that disappeared.
