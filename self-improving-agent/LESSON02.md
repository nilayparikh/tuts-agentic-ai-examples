# Lesson 02 Hands-On Guide

## Objective

Map the three runnable mutation surfaces in this repo so later lessons start
from recognition instead of reorientation.

## Source References

- [README.md](./README.md)
- [RUN.md](./RUN.md)
- [cleanloop/README.md](./cleanloop/README.md)
- [prompt_evolution/README.md](./prompt_evolution/README.md)
- [skill_mastery/README.md](./skill_mastery/README.md)

## Where To Look

- `./util.py` for the shared entry path.
- `./cleanloop/` for executable-logic mutation.
- `./prompt_evolution/` for instruction mutation.
- `./skill_mastery/` for habit-set mutation.
- `./cleanloop/.output/`, `./prompt_evolution/.output/`, and
  `./skill_mastery/.output/` for the artifacts each branch leaves behind.

## Commands

Run these from the root folder:

```powershell
python .\util.py setup
python .\util.py verify
python .\util.py status
python .\util.py -e prompt_evolution catalog
python .\util.py -e skill_mastery catalog
```

## Expected Evidence

- You can point to one shared entry path in `./util.py`.
- You can name the mutable artifact in each branch.
- You can show where each branch writes its output artifacts.
- You can explain why CleanLoop is the teaching path and why the other two
  branches still matter.
