# Lesson 05 - Autonomy Ladder

## Learning Objectives

- Run several sandbox rounds through the trust ladder.
- Classify the habit-composed response as supervised, human-gated, or autonomous.
- Use score level and stability as the autonomy signal.

## Command

```powershell
cd skill_mastery
python util.py autonomy --usecase makerspace_access_checkpoint --rounds 3 --timeout 30
```

## Inputs

- Use case profile from the catalog
- Habit selection output from the sandbox round
- Evaluator scores from repeated rounds

## Outputs

```text
Autonomy: HUMAN_GATED
  rounds observed:   3
  mean score ratio:  0.84
  stability spread:  0.06
  notes:
    - acceptable mean score with visible variance
```

## Validation

The autonomy command only reports trust posture. It does not deploy, approve, or persist production changes.

## Summary

The autonomy ladder turns repeated evidence into a simple operating mode. It helps learners see when a habit catalog needs more review before less supervised use.
