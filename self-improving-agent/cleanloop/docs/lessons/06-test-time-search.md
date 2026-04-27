# Lesson 06 — Test-Time Search and Re-Ranking

Lesson 06 explains how best-of-N mutation search works.

## Core Idea

Instead of trusting the first candidate, the loop can generate several proposals and compare them before commit.

## Code Anchors

- [Best-of-N proposal](../../reranker.py#L67)
- [Candidate evaluation](../../reranker.py#L118)
- [Loop caller](../../loop.py#L617)

## Inline Coding

```python
code, hyp, diagnostics = propose(
	client,
	model,
	genome_code,
	results["failed"],
	args.candidates,
)
```

That call matters because test-time search is still bounded. The loop asks for several candidates, but the fixed judge still decides which one survives.

## Hands-On Exercises

### Exercise 1 - Save candidate scoreboards

- Difficulty: Medium
- Files: `reranker.py`, `loop.py`
- Task: Persist every candidate score, total assertion count, and hypothesis to one JSON artifact for each reranked round.
- Hints: The cleanest first version writes the scoreboard right after the reranker returns, before commit or revert logic starts.
- Done when: One reranked run leaves a readable candidate scoreboard beside the other output artifacts.
- Stretch: Include token usage for each candidate when it is available.

### Exercise 2 - Add a tie-break rule

- Difficulty: Hard
- Files: `reranker.py`, `autogen_runtime.py`
- Task: Break equal scores with a deterministic secondary rule such as lower token cost or smaller response size.
- Hints: Do not hide the tie-break inside print-only output. Make it part of selection logic and explain it in logs.
- Done when: Equal-score candidates no longer produce ambiguous winners.
- Stretch: Log the exact tie-break reason in the proposal trace.

### Exercise 3 - Make search width visible end to end

- Difficulty: Medium
- Files: `loop.py`, `reranker.py`, `dashboard.py`
- Task: Thread `n_candidates` through console logs, history entries, and any scoreboard artifact so operators can see how wide the search really was.
- Hints: The loop already knows the requested width at startup. Reuse that fact instead of recomputing it downstream.
- Done when: A saved round explains both its winning score and how many candidates were considered.
- Stretch: Warn when reranking is enabled with only one candidate.

### Exercise 4 - Add a safe ceiling for candidate count

- Difficulty: Hard
- Files: `reranker.py`, `util.py`
- Task: Cap `n_candidates` at a practical maximum and explain the clamp in CLI output.
- Hints: The cap protects both token budget and runtime. Keep the first version simple and explicit.
- Done when: Oversized reranker requests are clamped instead of flooding the model with work.
- Stretch: Make the ceiling configurable through one environment variable.
