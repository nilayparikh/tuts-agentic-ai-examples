# Lesson 07 — Production Safety

Lesson 07 closes the course with containment, trust policy, and recovery.

## Controls

- [Sandbox runner](../../sandbox.py#L56) isolates the genome in a subprocess.
- [Autonomy simulator](../../autonomy.py#L148) models the trust ladder.
- [Reset workflow](../../reset_workflow.py#L9) restores the starter genome without deleting the shipped sample outputs.

## Why Recovery Matters

A self-improving loop without reset is hard to trust. A learner needs a reliable path back to the deterministic baseline.

## Inline Coding

```python
return reset_to_starter(
	output_dir=OUTPUT_DIR,
	genome_path=GENOME_PATH,
	starter_genome_path=STARTER_GENOME_PATH,
)
```

That call keeps recovery explicit. The learner can see the exact handoff from the CLI to the reset logic.

## Hands-On Exercises

### Exercise 1 - Persist sandbox outcomes

- Difficulty: Medium
- Files: `sandbox.py`
- Task: Write each sandbox result dict to a small JSON or JSONL artifact so the learner can inspect past isolation runs.
- Hints: `run_sandboxed()` already returns everything you need. Keep the artifact append-only and easy to diff.
- Done when: Repeated sandbox runs leave a short audit trail under `.output/`.
- Stretch: Include elapsed runtime in the saved payload.

### Exercise 2 - Make timeout failures obvious

- Difficulty: Easy
- Files: `sandbox.py`, `util.py`
- Task: Try a tiny timeout and then improve the operator-facing message so it is obvious whether the genome crashed or simply hung.
- Hints: The result dict already separates `timed_out`, `stderr`, and `return_code`.
- Done when: The learner can tell timeout from Python exception at a glance.
- Stretch: Surface the same distinction in one dashboard note or trace event.

### Exercise 3 - Enrich the trust ladder

- Difficulty: Medium
- Files: `autonomy.py`
- Task: Add one more trust-state field such as `consecutive_success_rounds` or `last_transition_reason` and print it in the simulation output.
- Hints: Derive the field where promotion and demotion already happen so it stays truthful.
- Done when: The simulation explains why a level changed, not only which level won.
- Stretch: Save the simulation rounds to CSV for later plotting.

### Exercise 4 - Add reset safety notes

- Difficulty: Medium
- Files: `reset_workflow.py`
- Task: Improve the reset output so it names exactly which artifacts are preserved and which file is restored.
- Hints: Keep behavior unchanged for the first pass. This exercise is about operator trust, not new mutation logic.
- Done when: `python util.py reset` reads like a safe recovery step instead of a risky destructive command.
- Stretch: Add a dry-run mode that reports actions without writing files.
