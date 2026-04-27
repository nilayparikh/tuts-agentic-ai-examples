# Lesson 01 — The Mutation Engine

Lesson 01 explains the local command surface, provider resolution, and the verify gate.

## Code Anchors

- [Status snapshot builder](../../status_snapshot.py#L16)
- [Status CLI command](../../util.py#L357)
- [Verify entrypoint](../../verify.py#L168)

## Actual Example Detail

Before any mutation round, the learner should confirm that the five finance files are present and that `cleanloop/.env` resolves a working endpoint.

## Inline Coding

```python
snapshot = build_status_snapshot()
```

That one line gives the learner a stable view of row counts, Python version, model, and output presence.

## Read This In Order

1. Start at [status_snapshot.py#L16](../../status_snapshot.py#L16) to see which facts the CLI gathers.
2. Then read [util.py#L357](../../util.py#L357) to see how those facts are rendered for the learner.
3. Finish at [verify.py#L168](../../verify.py#L168) to see the hard gate before the loop starts.

## Hands-On Exercises

### Exercise 1 - Add model provenance to the status view

- Difficulty: Easy
- Files: `status_snapshot.py`, `util.py`
- Task: Add a `model_source` field beside `model` so the status view shows whether the active model came from `MODEL_NAME`, `AZURE_OPENAI_DEPLOY_NAME`, or the default constant.
- Hints: The fallback chain already exists in `build_status_snapshot()`. Keep the logic in one place and only change the renderer after the snapshot shape is stable.
- Done when: `python util.py status` shows both the resolved model and where that value came from.
- Stretch: Also show which expected environment variables are still unset.

### Exercise 2 - Fail fast on empty fixture inputs

- Difficulty: Easy
- Files: `status_snapshot.py`, `verify.py`
- Task: Add a verification rule that fails when one of the shipped finance CSV files is missing or has zero data rows.
- Hints: Reuse `_count_rows()` and the dataset path helpers instead of scanning the directory twice.
- Done when: A broken or empty input file makes `python util.py verify` fail with the exact filename.
- Stretch: Add a status warning when the total fixture row count is not the expected 60 rows.

### Exercise 3 - Verify that the output directory is writable

- Difficulty: Medium
- Files: `verify.py`
- Task: Add one preflight check that proves `.output/` can be created and written before the learner starts the loop.
- Hints: Use a tiny probe file and clean it up even when the write fails.
- Done when: `python util.py verify` reports a dedicated pass or fail line for output write access.
- Stretch: Print a short fix hint when the path is blocked by permissions.

### Exercise 4 - Add a baseline fixture summary

- Difficulty: Medium
- Files: `status_snapshot.py`, `util.py`
- Task: Extend the status snapshot with `total_input_rows` and `fixture_matches_expected` so the learner can tell whether the starter fixture is intact.
- Hints: Build the aggregate from the existing `input_rows` dict. Do not hardcode the per-file counts in the renderer.
- Done when: `python util.py status` clearly shows whether the shipped baseline still matches the documented fixture.
- Stretch: Add one compact line that lists only the files whose row counts drifted.
