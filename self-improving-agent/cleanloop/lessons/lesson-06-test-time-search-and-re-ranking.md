# Lesson 06 — Test-Time Search and Re-Ranking

This lesson widens one proposal into a small, bounded search. Instead of trusting the first candidate, the loop generates multiple candidates, evaluates them separately, and only then commits the strongest survivor.

## Command Path

Run this command from `_examples/self-improving-agent/cleanloop/`:

```bash
python util.py loop --max-iterations 1 --rerank --candidates 2
```

Two candidates are enough to show the pattern clearly without burying the learner in log noise.

## Captured Output

```text
CleanLoop — Karpathy Loop (Finance Invoice Ledger, Best-of-N Reranking)

Score: 5/8
Reranker: generating 2 candidates...
[LLM_ATTEMPT] Attempt 1/2: AutoGen candidate 1: conservative
[LLM_ATTEMPT] Attempt 2/2: AutoGen candidate 2: value-first
[HYPOTHESIS_SELECTED] Ensure numeric conversion of 'value' and handle missing values...
[RE_EVALUATE_MUTATION] Re-running the mutated genome against the referee
[MUTATION_SCORE] Candidate scored 7/8
[COMMIT_MUTATION] Committed improved mutation at 7/8
```

This is the strongest captured example in the course. The standard one-shot run failed. The reranked run improved the score to `7/8` in one round.

## Code References

1. [propose in reranker.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/reranker.py#L49-L81)

   Important lines:

   ```python
   def propose(..., n_candidates: int = 3) -> tuple[str | None, str, dict[str, object]]:
       print(f"  Reranker: generating {n_candidates} candidates...")
       return autogen_runtime.propose_reranked_mutation(
           client,
           model,
           system,
           user,
           n_candidates=n_candidates,
           evaluate_candidate=_evaluate_candidate,
       )
   ```

   Impact: this is the fan-out seam. One failure state becomes multiple candidate genomes.

2. [\_evaluate_candidate in reranker.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/reranker.py#L93-L125)

   Important lines:

   ```python
   with tempfile.TemporaryDirectory() as tmpdir:
       genome_file = tmp / "clean_data.py"
       genome_file.write_text(candidate_code, encoding="utf-8")
       mod.clean(INPUT_DIR, output_file)
       results = prepare.evaluate(output_file)
   ```

   Impact: every candidate is scored in isolation. Weak candidates never get to corrupt the live genome just because they were sampled.

3. [propose_reranked_mutation in autogen_runtime.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/autogen_runtime.py#L136-L221)

   Important lines:

   ```python
   for index, (style_name, style_instruction) in enumerate(...):
       code, hypothesis, attempt = propose_single_mutation(...)
       score, total = evaluate_candidate(code)
       candidates.append({
           "index": index,
           "style": style_name,
           "score": score,
       })
   ```

   Impact: this is the real bounded search loop. Candidate generation and candidate evaluation stay tightly coupled.

4. [summarize_attempts in autogen_runtime.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/autogen_runtime.py#L42-L75)

   Important lines:

   ```python
   summary: dict[str, object] = {
       "selected_attempt": selected_attempt,
       "attempts": attempts,
       "prompt_tokens": prompt_tokens if saw_usage else None,
       "completion_tokens": completion_tokens if saw_usage else None,
   }
   ```

   Impact: reranking is only teachable because the system records the losing attempts as well as the winner.

## How The Pieces Connect

`reranker.py` creates the search space. `_evaluate_candidate` scores each candidate safely. `propose_reranked_mutation` keeps the candidate metadata together. Then the outer loop still sends the winner through the same fixed judge path.

## Hands-On Lab

Challenge:

Compare one standard one-shot run and one reranked run. Write down exactly what extra logs and metrics appear once search depth is enabled.

Success looks like this:

- You can name the fan-out function.
- You can name the isolated evaluation function.
- You can explain why reranking improves choice quality without changing the judge.
