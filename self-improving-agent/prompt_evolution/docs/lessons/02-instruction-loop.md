# Lesson 02 - Instruction Loop

## Learning Objectives

- Run the prompt mutation loop against a named scenario.
- See the input profile, response score, and persisted outputs.
- Compare single-shot and reranked candidate selection.

## Command

```powershell
cd prompt_evolution
python util.py loop --scenario makerspace_missing_booking --max-iterations 2
python util.py loop --scenario makerspace_missing_booking --rerank --candidates 3
```

## Inputs

- Scenario catalog from `.data/scenario_cases.json`
- Mutable instructions from the project runtime files
- LLM settings from `.env` or `../.env`

## Outputs

```text
NOTE: REQUESTING_LLM_PROPOSAL ...
NOTE: ROUND_SCORE Score 8/10.
Best score: 8/10
Best response: .output/best_response.md
Best instructions: .output/best_instructions.md
```

Artifacts:

- `.output/latest_session.json`
- `.output/best_response.md`
- `.output/best_instructions.md`
- `.output/traces/*.jsonl`

## Validation

Run `python util.py evaluate --scenario makerspace_missing_booking --candidate .output/best_response.md` to score the saved response with the deterministic referee.

## Summary

The loop mutates instruction text, generates a response, scores the response, and keeps the best instruction state. Rerank mode adds a test-time search surface before committing a winner.
