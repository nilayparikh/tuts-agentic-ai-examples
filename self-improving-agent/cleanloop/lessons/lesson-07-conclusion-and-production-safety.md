# Lesson 07 — Conclusion and Production Safety

This lesson closes the course by adding the three controls that make the loop survivable in production: containment, trust policy, and reset. Without those three controls, the loop is still just a clever experiment.

## Command Path

Run these commands from `_examples/self-improving-agent/cleanloop/`:

```bash
python util.py sandbox --timeout 10
python util.py autonomy --rounds 5
python util.py reset
```

Each command maps to one safety control:

- `sandbox` is containment.
- `autonomy` is trust policy.
- `reset` is recovery.

## Captured Output

From `python util.py sandbox --timeout 10`:

```text
CleanLoop — Sandbox (Finance Invoice Ledger, timeout=10s)
Step 1/2 — Running genome in isolated subprocess
  OK: Genome completed successfully
Step 2/2 — Evaluating sandboxed output
  NOTE: Score: 5/8
```

From `python util.py autonomy --rounds 5`:

```text
Graduated Autonomy Simulation
Round   Rate     Level          Action                           Mode
1       0.37     SUPERVISED     HOLD                             [REVIEW]
2       0.33     SUPERVISED     HOLD                             [REVIEW]
3       0.37     SUPERVISED     HOLD                             [REVIEW]
4       0.55     SUPERVISED     HOLD                             [REVIEW]
5       0.49     SUPERVISED     HOLD                             [REVIEW]

Final: SUPERVISED (score: 0.42)
```

From `python util.py reset`:

```text
CleanLoop — Reset
Step 2/2 — Restoring genome to last committed state
  OK: Restored cleanloop/clean_data.py from clean_data_starter.py
```

## Code References

1. [run_sandboxed in sandbox.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/sandbox.py#L48-L96)

   Important lines:

   ```python
   result = subprocess.run(
       [sys.executable, "-c", runner],
       capture_output=True,
       text=True,
       timeout=timeout,
       cwd=str(PROJECT_ROOT),
   )
   ```

   Impact: the genome runs in a separate process with a timeout. That is the actual containment boundary for self-rewriting code.

2. [TrustState in autonomy.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/autonomy.py#L74-L120)

   Important lines:

   ```python
   @dataclass
   class TrustState:
       level: int = 0
       history: list[float] = field(default_factory=list)
       rounds_at_level: int = 0

       def record_round(self, pass_rate: float) -> str:
           if pass_rate == 0.0 and self.level > 0:
               self.level = 0
   ```

   Impact: trust is stateful and conservative. Promotion takes time. Critical failure collapses trust immediately.

3. [simulate in autonomy.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/autonomy.py#L143-L178)

   Important lines:

   ```python
   for i in range(1, n_rounds + 1):
       base = min(0.95, 0.3 + i * 0.06)
       noise = random.uniform(-0.15, 0.10)
       rate = max(0.0, min(1.0, base + noise))
       action = trust.record_round(rate)
   ```

   Impact: this is the simplest way to explain the autonomy ladder before you bind it to a real deployment policy.

4. [local reset command in cleanloop/util.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/util.py)

   Important lines:

   ```python
     if OUTPUT_DIR.exists():
       shutil.rmtree(OUTPUT_DIR)
     GENOME_PATH.write_text(STARTER_GENOME_PATH.read_text(encoding="utf-8"), encoding="utf-8")
   ```

   Impact: this is the operator-facing recovery path. It clears the output directory and restores the starter genome from a known-good source.

## How The Pieces Connect

Sandboxing keeps bad code contained. The trust ladder keeps the loop from escalating too fast. Reset gives you a clean way back when the run state becomes unreliable.

## Hands-On Lab

Challenge:

Run all three commands and map each one to a specific production failure mode. Do not use vague language like "safety" or "stability." Name the actual failure each control protects against.

Success looks like this:

- You can name the isolation failure mode.
- You can name the trust failure mode.
- You can name the recovery failure mode.
