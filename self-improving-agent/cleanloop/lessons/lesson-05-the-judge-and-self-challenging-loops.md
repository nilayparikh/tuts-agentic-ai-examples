# Lesson 05 — The Judge and Self-Challenging Loops

This lesson raises pressure without moving the target. The loop gets harder data, but the same fixed judge still decides what counts as correct.

## Command Path

Run these commands from `_examples/self-improving-agent/cleanloop/`:

```bash
python util.py verify
python util.py challenge --levels 1
python util.py evaluate
```

This sequence matters. First prove the runtime is healthy. Then generate harder data. Then keep using the same judge.

## Captured Output

From `python util.py challenge --levels 1`:

```text
CleanLoop — Adversarial Data Generator (Levels: [1])

Step 1/1 — Generating adversarial CSV files
Generating 1 adversarial CSVs across levels: [1]
  Created: adversarial_d1_01.csv

Done. Run `python util.py loop` to test the genome against new data.
```

This output is the whole point of the lesson. The loop can generate harder fixtures, but the command does not touch the judge or the genome contract.

## Code References

1. [local verify command in cleanloop/util.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/util.py)

   Important lines:

   ```python
   def _cmd_verify(_args: argparse.Namespace) -> int:
       return _run_module_main("cleanloop.verify", [])
   ```

   Impact: you do not increase challenge pressure on a broken runtime. The local command
   surface still routes learners through the same verification gate first.

2. [assert_has_required_columns and friends in prepare.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/prepare.py#L37-L167)

   Important lines:

   ```python
   def assert_numeric_column(df: pd.DataFrame, column: str) -> tuple[bool, str]:
       coerced = pd.to_numeric(df[column], errors="coerce")
       if coerced.notna().all():
           return True, f"{column} is numeric"
   ```

   Impact: this is the fixed correctness surface. The challenger can make the task harder, but it cannot loosen this gate.

3. [DIFFICULTY_LEVELS in challenger.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/challenger.py#L53-L79)

   Important lines:

   ```python
   DIFFICULTY_LEVELS: dict[int, str] = {
       1: "Mild messiness: some currency symbols...",
       2: "Moderate messiness: mixed date formats...",
       5: "Nightmare: all of the above PLUS inconsistent row lengths...",
   }
   ```

   Impact: the curriculum pressure is explicit. Difficulty is not hidden in prompt text spread around the repo.

4. [generate_messy_csv in challenger.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/challenger.py#L88-L108) and [main in challenger.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/challenger.py#L118-L160)

   Important lines:

   ```python
   content = util.create_text_completion(
       client,
       system_prompt=SYSTEM_PROMPT,
       user_prompt=DIFFICULTY_LEVELS[difficulty],
       temperature=0.8,
       max_tokens=500,
   )
   path.write_text(csv_content, encoding="utf-8")
   ```

   Impact: the challenger changes the data surface only. It writes adversarial CSVs into the input area and leaves the judge untouched.

## How The Pieces Connect

`verify` proves the model path works. `challenger.py` creates harder data. `prepare.py` then evaluates the output against the same assertions as before. That is the correct way to increase pressure.

## Hands-On Lab

Challenge:

Generate one adversarial CSV, then explain why `challenger.py` is allowed to mutate the input landscape while `prepare.py` is not allowed to change at all.

Success looks like this:

- You can point to the difficulty ladder.
- You can point to the fixed judge code.
- You can explain why harder data is not the same thing as a softer judge.
