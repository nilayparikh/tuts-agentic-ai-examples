# Lesson 02 — Defining the Pipeline Genome

This lesson narrows the mutation surface until it is boringly explicit. In CleanLoop, the genome is one file. The judge is another file. The course only works because those two responsibilities are not allowed to blur.

## Command Path

Run these commands from `_examples/self-improving-agent/cleanloop/`:

```bash
python util.py evaluate
python util.py reset
```

Why these two commands matter:

- `evaluate` gives you the baseline score for the current genome output.
- `reset` proves the course can always return to the immutable starter genome.

## Captured Output

From `python util.py evaluate`:

```text
CleanLoop — Evaluate (Finance Invoice Ledger)

Step 1/2 — Running genome (no output yet)
  OK: Output generated: ...\cleanloop\.output\finance_master.csv

Step 2/2 — Running binary assertions
  OK: PASS  can_read_output
  OK: PASS  has_required_columns: all columns present
  ERROR: FAIL  value_is_numeric: 36 non-numeric or missing values in value
  ERROR: FAIL  no_nan_value: 8 NaN values in value
  ERROR: FAIL  matches_reference_output: matched=2, missing=58, unexpected=73

Score: 5/8 — 3 Failing
```

From `python util.py reset`:

```text
CleanLoop — Reset
  NOTE: No .output/ directory to delete
Step 2/2 — Restoring genome to last committed state
  OK: Restored cleanloop/clean_data.py from clean_data_starter.py
```

The point of this lesson is visible in those two outputs. The starter genome is weak on purpose, and the loop can always restore it.

## Code References

1. [clean in clean_data_starter.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/clean_data_starter.py#L75-L92)

   Important lines:

   ```python
   def clean(input_dir: Path, output_path: Path) -> None:
       frames: list[pd.DataFrame] = []
       for csv_file in cleanloop_datasets.get_input_paths(input_dir):
           frame = _read_finance_frame(csv_file)
           if not frame.empty:
               frames.append(frame)
       master = pd.concat(frames, ignore_index=True)
       master = _normalize_finance_frame(master)
   ```

   Impact: this is the immutable teaching baseline. It runs, but it does not solve the finance arena well enough. That makes the failure surface measurable.

2. [\_read_finance_frame in clean_data_starter.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/clean_data_starter.py#L43-L63) and [\_normalize_finance_frame in clean_data_starter.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/clean_data_starter.py#L66-L72)

   Important lines:

   ```python
   records.append(
       {
           "date": str(raw.get("issued", "")).strip(),
           "entity": str(raw.get("customer", "")).strip(),
           "value": str(raw.get("amount", "")).strip(),
           "category": str(raw.get("status", csv_file.stem)).strip(),
       }
   )
   ```

   Impact: these lines show the real genome surface. The loop is not mutating the whole repo. It is mutating how raw rows become the shared finance schema.

3. [evaluate in prepare.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/prepare.py#L188-L220)

   Important lines:

   ```python
   def evaluate(master_csv: Path) -> dict:
       df = pd.read_csv(master_csv)
       reference_df = _load_reference_df()
       metrics = _build_reference_metrics(df, reference_df, DEFAULT_DATASET.required_columns)
       checks = _build_checks(df, metrics)
   ```

   Impact: this is the fixed referee entrypoint. Every genome mutation still has to pass through this same deterministic gate.

4. [\_prepare_fresh_run in loop.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/loop.py#L285-L327)

   Important lines:

   ```python
   for artifact in [output_path, history_path]:
       if artifact.exists():
           artifact.unlink()
   starter_code = starter_genome_path.read_text(encoding="utf-8")
   genome_path.write_text(starter_code, encoding="utf-8")
   ```

   Impact: this is the operational reset boundary. It clears stale artifacts and rewrites the live genome from the starter snapshot.

## How The Pieces Connect

`clean_data_starter.py` gives you the baseline genome. `prepare.py` gives you the fixed judge. `_prepare_fresh_run` makes that boundary reproducible at the start of every new run.

## Hands-On Lab

Challenge:

Open `clean_data_starter.py`, `clean_data.py`, and `prepare.py` side by side. Write a short note that explains why only one of those files is allowed to mutate.

Success looks like this:

- You can name the exact mutable file.
- You can name the exact reset path.
- You can defend why the judge must remain immutable.
