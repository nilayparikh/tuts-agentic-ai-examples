# Lesson 04 - Challenges And Sandbox

## Learning Objectives

- Generate adversarial scenario variants.
- Run one isolated prompt round before committing to a full loop.
- Validate response quality with the deterministic evaluator.

## Command

```powershell
cd prompt_evolution
python util.py challenge --scenario makerspace_missing_booking --levels 1 2 3
python util.py sandbox --scenario makerspace_missing_booking --timeout 30
python util.py evaluate --scenario makerspace_missing_booking --candidate .output/best_response.md
```

## Inputs

- Base scenario from `.data/scenario_cases.json`
- Deterministic evaluator rules from `evaluator.py`
- Optional candidate response file

## Outputs

```text
Generated adversarial scenario variants:
  - makerspace_missing_booking_tier_1: ...
  - makerspace_missing_booking_tier_2: ...

Sandbox round: score 7/10
  elapsed:        4.22s
  timeout exceeded: False
  iteration clamp: 1
```

## Validation

The sandbox clamps Hermes iterations and reports evaluator issues instead of mutating saved instructions. The evaluate command scores a saved response against the same rubric.

## Summary

This lesson makes the safety workflow explicit. Challenge generation widens the input space, sandbox checks one round, and evaluate scores a saved output.
