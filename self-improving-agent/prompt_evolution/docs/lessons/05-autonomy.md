# Lesson 05 - Autonomy Ladder

## Learning Objectives

- Run several sandbox rounds through a trust ladder.
- See whether the instruction prompt should stay supervised.
- Use score stability as an autonomy signal.

## Command

```powershell
cd prompt_evolution
python util.py autonomy --scenario makerspace_missing_booking --rounds 3 --timeout 30
```

## Inputs

- The same scenario profile used by `loop` and `sandbox`
- Round scores from the deterministic evaluator

## Outputs

```text
Autonomy: HUMAN_GATED
  rounds observed:   3
  mean score ratio:  0.82
  stability spread:  0.08
  notes:
    - acceptable mean score with visible variance
```

## Validation

Autonomy is advisory. It never deploys or approves real changes. It classifies the prompt state from observed score level and score variance.

## Summary

The autonomy command turns repeated sandbox evidence into a plain trust decision. Learners can see why a prompt remains supervised, moves to human-gated mode, or earns autonomous status.
