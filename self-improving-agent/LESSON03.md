# Lesson 03 Hands-On Guide

## Objective

Inspect the bounded CleanLoop arena so you can separate the fixed judge from the
mutable genome before the orchestrator automates the cycle.

## Source References

- [README.md](./README.md)
- [RUN.md](./RUN.md)
- [cleanloop/README.md](./cleanloop/README.md)
- [cleanloop/prepare.py](./cleanloop/prepare.py)
- [cleanloop/clean_data_starter.py](./cleanloop/clean_data_starter.py)
- [cleanloop/clean_data.py](./cleanloop/clean_data.py)

## Where To Look

- `./cleanloop/.input/` for the five finance input files.
- `./cleanloop/.gold/finance_expected.csv` for the fixed target.
- `./cleanloop/prepare.py` for the referee logic.
- `./cleanloop/clean_data_starter.py` for the weak reset source.
- `./cleanloop/clean_data.py` for the live mutable genome.
- `./cleanloop/.output/` for `finance_master.csv`,
  `finance_eval_history.json`, and `finance_strategy.json`.

## Commands

Run these from the root folder:

```powershell
python .\util.py status
python .\util.py -e cleanloop reset
python .\util.py -e cleanloop evaluate
Get-Content .\cleanloop\.output\finance_eval_history.json -TotalCount 40
```

## Expected Evidence

- You can explain why `./cleanloop/prepare.py` is fixed.
- You can explain why `./cleanloop/clean_data.py` is the only mutable surface.
- You can show the baseline output and the failing history artifact.
- You can explain how the output artifacts narrow the next repair instead of
  just reporting a score.
