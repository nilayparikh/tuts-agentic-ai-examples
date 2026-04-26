# Lesson 03 — The Orchestrator

This lesson follows one real loop round from start to finish. The orchestrator is where the course stops talking about ideas and starts acting like a controlled system: reset, evaluate, propose, re-evaluate, then either commit or revert.

## Command Path

Run this command from `_examples/self-improving-agent/cleanloop/`:

```bash
python util.py loop --max-iterations 1
```

This is the smallest useful loop run. It is long enough to show the full control flow, but short enough that you can still inspect each event.

## Captured Output

```text
CleanLoop — Karpathy Loop (Finance Invoice Ledger, Standard)

[FRESH_START] Starting from the immutable starter genome for dataset finance
[RESTORE_STARTER_GENOME] Restored clean_data.py from clean_data_starter.py

--- Round 1/1 ---
Score: 5/8
[REQUESTING_LLM_PROPOSAL] Requesting mutation proposal from model microsoft/Phi-4
[LLM_ATTEMPT] Attempt 1/1: AutoGen proposer
[HYPOTHESIS_SELECTED] Normalize currency symbols and accounting markers...
[WRITE_MUTATED_GENOME] Writing candidate mutation to clean_data.py
[MUTATION_EXECUTION_FAILED] can_run_genome: invalid syntax (clean_data.py, line 1)
[REVERT_MUTATION] Reverted mutation with score 0/1
```

This run is useful because it shows the orchestrator rejecting a bad mutation. The system stays honest even when the model returns unusable code.

## Code References

1. [run_loop in loop.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/loop.py#L532-L744)

   Important lines:

   ```python
   results = _run_and_evaluate(clean_data, prepare, INPUT_DIR, output_path)
   if use_reranker:
       new_code, hypothesis, llm_diagnostics = reranker.propose(...)
   else:
       new_code, hypothesis, llm_diagnostics = _propose_fix(...)
   GENOME_PATH.write_text(new_code, encoding="utf-8")
   new_results = _run_and_evaluate(clean_data, prepare, INPUT_DIR, output_path)
   ```

   Impact: this is the real orchestrator contract. The loop owns evaluation before and after the LLM proposal, which is why the course can separate mutation from judgment.

2. [\_prepare_fresh_run in loop.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/loop.py#L285-L327)

   Important lines:

   ```python
   _append_log(logs, "FRESH_START", ...)
   starter_code = starter_genome_path.read_text(encoding="utf-8")
   genome_path.write_text(starter_code, encoding="utf-8")
   ```

   Impact: every round starts from a known baseline. That keeps the loop reproducible and makes the mutation decision interpretable.

3. [propose_single_mutation in autogen_runtime.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/autogen_runtime.py#L86-L121)

   Important lines:

   ```python
   proposal, events, usage = _run_structured_agent(...)
   code = proposal.clean_data_py.strip() or None
   hypothesis = proposal.hypothesis.strip() or "no hypothesis"
   attempt = {
       "label": label,
       "usage": usage,
       "mutation_summary": proposal.mutation_summary,
   }
   ```

   Impact: this is the handoff from deterministic control into AutoGen. The proposer returns structured artifacts the orchestrator can inspect and log.

4. [evaluate in prepare.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/prepare.py#L188-L220)

   Important lines:

   ```python
   checks = _build_checks(df, metrics)
   for name, fn, data in checks:
       passed, detail = fn(data)
   results["score"] = len(results["passed"])
   ```

   Impact: this is where deterministic judging resumes. The orchestrator may hand the genome to AutoGen, but it always comes back here for scoring.

## How The Pieces Connect

The loop starts with a fresh baseline, collects the current failure state, asks AutoGen for one structured proposal, writes that candidate into the live genome, and then sends the result back through the same judge. If the candidate breaks execution or scoring, the orchestrator kills it.

## Hands-On Lab

Challenge:

Trace the standard loop path in `loop.py`. Mark the exact line where the LLM proposal begins and the exact line where deterministic judging resumes.

Success looks like this:

- You can point to the proposal call.
- You can point to the re-evaluation call.
- You can explain why the orchestrator, not the model, owns the final decision.
