# Hands-On Lab

Use this file as the index for the interactive lessons in this repo.
All relative paths in this guide assume you are already in `.` at
`_examples/self-improving-agent`.

## Start Here

Read these files in this order before you start any lesson lab:

1. [README.md](./README.md)
2. [RUN.md](./RUN.md)
3. [LESSON02.md](./LESSON02.md)
4. [LESSON03.md](./LESSON03.md)
5. [LESSON04.md](./LESSON04.md)

## Shared Setup

Run the shared setup once from the root folder:

```powershell
python .\util.py setup
python .\util.py verify
python .\util.py status
```

## Lesson Map

| Lesson | Focus | Main Files | Main Outcome |
| --- | --- | --- | --- |
| 02 | Map the mutation surfaces | `./util.py`, `./cleanloop/`, `./prompt_evolution/`, `./skill_mastery/` | You can explain what changes in each branch and what stays fixed |
| 03 | Inspect the bounded arena | `./cleanloop/prepare.py`, `./cleanloop/clean_data_starter.py`, `./cleanloop/clean_data.py` | You can identify the judge, the mutable genome, and the artifact trail |
| 04 | Trace the orchestrator loop | `./cleanloop/loop.py`, `./prompt_evolution/loop.py`, `./skill_mastery/loop.py` | You can explain reset, read, propose, evaluate, and select with real artifacts |

## Working Rule

Do not jump straight to code edits. Read the repo anchor files first.
Then run the smallest command that produces visible evidence.
After each run, inspect the output files before you move to the next lesson.
