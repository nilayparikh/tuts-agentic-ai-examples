# Lesson 04 - Challenges And Sandbox

## Learning Objectives

- Generate harder use case variants.
- Run one isolated habit-composition round.
- Validate a saved response against the deterministic evaluator.

## Command

```powershell
cd skill_mastery
python util.py challenge --usecase makerspace_access_checkpoint --levels 1 2 3
python util.py sandbox --usecase makerspace_access_checkpoint --timeout 30
python util.py evaluate --usecase makerspace_access_checkpoint --candidate .output/best_response.md
```

## Inputs

- Base use case from `.data/usecases.json`
- Habit catalog from `.data/habit_definitions.json`
- Deterministic evaluator rules from `evaluator.py`

## Outputs

```text
Generated adversarial use case variants:
  - habit_refund_deescalation_tier_1: ...
  - habit_refund_deescalation_tier_2: ...

Sandbox round: score 8/10
  selected habits: mirror_issue, cite_policy_gate, offer_checkpoint
  elapsed:         4.10s
  timeout exceeded: False
  iteration clamp: 1
```

## Validation

Sandbox output includes selected habits, score, timing, and issues. It does not persist a new best response unless you run the full loop.

## Summary

Challenge, sandbox, and evaluate form the safety workflow. They expose input pressure, output quality, and failure reasons before you trust the loop.
