# Lesson 03 — The Orchestrator

Lesson 03 shows how one failed evaluation becomes the next mutation attempt.

## Core Loop Steps

1. run genome
2. evaluate output
3. ask for one mutation proposal
4. re-run candidate
5. commit or revert

## Code Anchors

- [Loop entrypoint](../../loop.py#L617)
- [Metacognition snapshot](../../loop.py#L260)
- [Attempt summary](../../loop.py#L139)

The orchestration stays bounded on purpose. One genome changes. One judge scores it. One loop decides whether the candidate survives.

## Inline Coding

```python
loop.run_loop(
	max_iterations=args.max_iterations,
	use_reranker=args.rerank,
	n_candidates=args.candidates,
)
```

That call is the whole bounded recipe. The important teaching move is not more abstraction. It is understanding the order of decisions around one candidate.

## Hands-On Exercises

### Exercise 1 - Export score delta into the structured logs

- Difficulty: Easy
- Files: `loop.py`
- Task: Add `score_delta` to the exported JSONL log payload so scripts and dashboards can chart improvement without recomputing it.
- Hints: Patch `_write_exported_logs()` instead of rebuilding the field in multiple consumers.
- Done when: Accepted and reverted rounds both emit log lines with an explicit delta.
- Stretch: Also export `before_score` so the change is obvious in one record.

### Exercise 2 - Track stalled rounds

- Difficulty: Medium
- Files: `loop.py`
- Task: Extend the metacognition snapshot with a `stalled_rounds` field when the same focus area repeats without a score increase.
- Hints: Look at the last few history entries plus the current `results` snapshot before you decide whether the loop is stalled.
- Done when: `.output/finance_strategy.json` reports both the focus area and how long the loop has been stuck there.
- Stretch: Change the coaching guidance after the second stalled round.

### Exercise 3 - Add an early-stop rule for no progress

- Difficulty: Hard
- Files: `loop.py`, `util.py`
- Task: Stop the loop after a small streak of zero-delta rounds and log why the run ended early.
- Hints: The cheapest signal is already in the round history. Keep the threshold local first, then expose it as a CLI option only if the behavior feels right.
- Done when: A non-improving run exits early with a clear teaching message instead of consuming every remaining round.
- Stretch: Add a `--patience` flag to the loop command.

### Exercise 4 - Trace the winning LLM path

- Difficulty: Hard
- Files: `loop.py`, `tracing.py`
- Task: Record the selected attempt label and total token usage as a proposal event when the loop commits a candidate.
- Hints: The LLM diagnostics already carry `selected_attempt`, `prompt_tokens`, and `total_tokens`.
- Done when: `.output/traces/proposal-events.jsonl` shows which attempt won and what it cost.
- Stretch: Include the requested candidate count when reranking is enabled.
