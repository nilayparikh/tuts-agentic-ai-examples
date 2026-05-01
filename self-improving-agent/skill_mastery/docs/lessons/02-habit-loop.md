# Lesson 02 - Habit Loop

## Learning Objectives

- Learn reusable habits from demonstrations.
- Select habits for a named use case.
- Generate and score a composed response.

## Command

```powershell
cd skill_mastery
python util.py loop --usecase makerspace_access_checkpoint --max-iterations 2
python util.py loop --usecase makerspace_access_checkpoint --rerank --candidates 3
```

## Inputs

- Demonstrations and habit definitions from `.data/`
- Use case profile from `.data/usecases.json`
- LLM settings from `.env` or `../.env`

## Outputs

```text
NOTE: SELECTED_HABITS selected=mirror_issue, cite_policy_gate, offer_checkpoint
NOTE: ROUND_SCORE Score 9/10.
Best score: 9/10
Best response: .output/best_response.md
Selected habits: .output/selected_habits.json
```

Artifacts:

- `.output/latest_session.json`
- `.output/learned_habits.json`
- `.output/selected_habits.json`
- `.output/best_response.md`

## Validation

Run `python util.py evaluate --usecase makerspace_access_checkpoint --candidate .output/best_response.md` to score the saved response.

## Summary

The habit loop separates learning, selection, generation, and scoring. Rerank mode adds test-time search without changing the habit catalog itself.
