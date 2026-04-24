# Lesson 04 Hands-On Guide

## Objective

Trace the orchestrator loop end to end so reset, read, propose, evaluate, and
select become concrete engineering stages instead of abstract animation.

## Source References

- [README.md](./README.md)
- [RUN.md](./RUN.md)
- [cleanloop/loop.py](./cleanloop/loop.py)
- [prompt_evolution/loop.py](./prompt_evolution/loop.py)
- [skill_mastery/loop.py](./skill_mastery/loop.py)

## Where To Look

- `./cleanloop/loop.py` for the full control path.
- `./cleanloop/clean_data.py` for the mutable genome the loop rewrites.
- `./cleanloop/prepare.py` for the fixed judge the loop reruns.
- `./cleanloop/.output/finance_eval_history.json` for round-by-round evidence.
- `./cleanloop/.output/finance_strategy.json` for the current repair focus.
- `./prompt_evolution/loop.py` and `./skill_mastery/loop.py` for the same outer
  control cycle on different mutable artifacts.

## Commands

Run these from the root folder:

```powershell
python .\util.py -e cleanloop reset
python .\util.py -e cleanloop loop --max-iterations 2
git log --oneline -n 3
Get-Content .\cleanloop\.output\finance_eval_history.json -TotalCount 40
Get-Content .\cleanloop\.output\finance_strategy.json -TotalCount 40
```

## Expected Evidence

- You can point to the reset, read, propose, evaluate, and selection stages in
  `./cleanloop/loop.py`.
- You can explain why a Git commit means survival and why a revert means the
  candidate died.
- You can show the history and strategy artifacts that make the loop
  inspectable after the terminal run ends.
- You can compare `./cleanloop/loop.py`, `./prompt_evolution/loop.py`, and
  `./skill_mastery/loop.py` without claiming they are different control
  patterns.
