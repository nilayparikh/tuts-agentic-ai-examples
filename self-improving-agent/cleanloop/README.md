# CleanLoop

[![Watch: Stop Fixing Pipelines: Build a Self-Evolving AI Data Engineer | Lesson 01 of 07](https://img.youtube.com/vi/yx6aB5heI9o/maxresdefault.jpg)](https://www.youtube.com/watch?v=yx6aB5heI9o)

[![Watch: One File to Rule the Loop: Engineering the Pipeline Genome | Lesson 02 of 07](https://img.youtube.com/vi/8Y7MEbEw8wc/maxresdefault.jpg)](https://www.youtube.com/watch?v=8Y7MEbEw8wc)

[![Watch: Stop Fixing Data Pipelines: Build an AI Orchestrator with AutoGen | Lesson 03 of 07](https://img.youtube.com/vi/--mpnJ8f4Sg/maxresdefault.jpg)](https://www.youtube.com/watch?v=--mpnJ8f4Sg)

> <strong>Watch Lesson 01:</strong> <a href="https://www.youtube.com/watch?v=yx6aB5heI9o" target="_blank" rel="noopener noreferrer">Stop Fixing Pipelines: Build a Self-Evolving AI Data Engineer | Lesson 01 of 07</a>
> <strong>Watch Lesson 02:</strong> <a href="https://www.youtube.com/watch?v=8Y7MEbEw8wc" target="_blank" rel="noopener noreferrer">One File to Rule the Loop: Engineering the Pipeline Genome | Lesson 02 of 07</a>
> <strong>Watch Lesson 03:</strong> <a href="https://www.youtube.com/watch?v=--mpnJ8f4Sg" target="_blank" rel="noopener noreferrer">Stop Fixing Data Pipelines: Build an AI Orchestrator with AutoGen | Lesson 03 of 07</a>
> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>

CleanLoop is the runnable example for the course `Building the Self-Evolving Data Engineer`.

It teaches one bounded self-improving loop over a finance data-cleaning pipeline.
The shipped fixture contains 87 rows across five CSV files and currently produces:

- 78 rows in `finance_master.csv`
- 48 rows in `finance_mutation_success.csv`
- 9 rows in `finance_mutation_failures.csv`

## Start Here

Run from inside `cleanloop/`:

```bash
pip install -e .
python util.py status
python util.py verify
python util.py evaluate
```

The local runtime uses `cleanloop/.env` first. That keeps the example self-sufficient.

## Docs Map

All documentation now lives under `docs/`.

- architecture: `docs/architecture/`
- data walkthroughs: `docs/data/`
- lesson-by-lesson notes: `docs/lessons/`
- operations and tracing: `docs/operations/`
- test coverage map: `docs/testing/`
- naming and code maps: `docs/reference/`

Each lesson note under `docs/lessons/` now ends with a hands-on exercise block.
Those exercises point at real files, include hints, and give a clear done state
so the learner can move from reading to changing the example.

The core course notes run from Lesson 01 through Lesson 07. Lesson 08 and
Lesson 09 are companion deep dives for dashboard oversight and the autonomy
ladder.

Recommended reading order:

1. `docs/architecture/system-overview.md`
2. `docs/data/finance-fixture-walkthrough.md`
3. `docs/lessons/01-mutation-engine.md`
4. `docs/testing/test-map.md`

## Root-First Code Layout

The root files are the real learning surface.

- `util.py`: CLI, environment loading, and command dispatch
- `verify.py`: local environment and LLM verification gate
- `clean_data_runtime.py`: deterministic pass plus mutation playbook routing
- `loop.py`: bounded mutation orchestrator
- `prepare.py`: fixed referee and scoring
- `challenger.py`: adversarial CSV generation
- `reranker.py`: best-of-N candidate search
- `dashboard.py`: learner-facing observability surface

Small helper modules live beside those files with job-based names such as
`status_snapshot.py`, `mutation_playbook.py`, `history_store.py`,
`reset_workflow.py`, and `tracing.py`.

The lesson markdown files under `docs/lessons/` now point back into those root
files with exact line references and short code excerpts.

## Key Commands

```bash
python util.py loop --max-iterations 5
python util.py challenge --levels 1 2 3
python util.py sandbox --timeout 10
python util.py autonomy --rounds 10
python util.py autonomy --from-history
python util.py observe
python util.py dashboard
python util.py reset
```

## Lesson 05-09 Capability Map

| Lesson              | Command                                                | Visible Artifacts                                              | What It Validates                                                            |
| ------------------- | ------------------------------------------------------ | -------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 05 self-challenge   | `python util.py challenge --levels 1 2 3`              | `.input/adversarial_d*.csv`, `.output/challenge_manifest.json` | Generated files match the finance invoice schema before they enter the arena |
| 06 test-time search | `python util.py loop --rerank --candidates 3`          | `.output/rerank_scoreboard.json`, per-round scoreboards        | Candidate repairs are scored and the selected repair is visible              |
| 07 safety           | `python util.py sandbox --timeout 10`                  | `.output/sandbox_runs.jsonl`                                   | Genome execution is isolated and audited before evaluation                   |
| 08 observability    | `python util.py observe` or `python util.py dashboard` | `.output/traces/`, `.output/runs/`, artifact health rows       | Operators can see scores, missing rows, unexpected rows, and artifact health |
| 09 autonomy         | `python util.py autonomy --from-history`               | latest loop history plus trust decision text                   | Trust level is derived from judged history, not only synthetic simulation    |

Challenge files are active inputs. Once `adversarial_d*.csv` files exist in
`.input/`, `evaluate`, `loop`, and `sandbox` read them together with the shipped
finance fixtures. Use `python util.py status` to see shipped row counts,
challenge row counts, and whether the challenge manifest exists.

## Validation

```bash
python -m unittest tests.test_cleanloop_course_structure
python -m unittest tests.test_cleanloop_exports
python -m unittest tests.test_python_compat
```

Provider compatibility matters here. Some OpenAI-compatible providers accept
AutoGen's native structured-output path directly. Others reject `json_schema`
and only allow `json_object`. When that happens, this example now falls back to
an AutoGen model-client JSON call and validates the returned object with the
same Pydantic schema. The loop still stays on AutoGen clients, but the schema
enforcement moves into the example runtime for that provider.

## Native Capability Boundary

This example deliberately uses AutoGen where AutoGen already helps, and keeps
the lesson-specific behavior outside the framework.

Native AutoGen capabilities used here:

- agent execution with `AssistantAgent`
- streamed message traces with `run_stream()`
- provider clients from `autogen-ext`
- typed response models for mutation and judge decisions when the provider supports them

Custom lesson logic that remains outside AutoGen on purpose:

- the deterministic finance referee in `prepare.py`
- the commit-or-revert learning loop in `loop.py`
- best-of-N candidate scoring against the fixed judge
- dashboard-specific attempt summaries and artifact history

This means the example does not reimplement generic team chat, tool routing, or
workflow selection that AutoGen already ships. It keeps AutoGen at the model
interaction seam and keeps the tutorial-specific learning loop in application
code.

## Series Navigation

| Lesson | Video                                                                                                                                   | Example Folder  |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 01     | [Stop Fixing Pipelines: Build a Self-Evolving AI Data Engineer &#124; Lesson 01 of 07](https://www.youtube.com/watch?v=yx6aB5heI9o)     | [cleanloop](./) |
| 02     | [One File to Rule the Loop: Engineering the Pipeline Genome &#124; Lesson 02 of 07](https://www.youtube.com/watch?v=8Y7MEbEw8wc)        | [cleanloop](./) |
| 03     | [Stop Fixing Data Pipelines: Build an AI Orchestrator with AutoGen &#124; Lesson 03 of 07](https://www.youtube.com/watch?v=--mpnJ8f4Sg) | [cleanloop](./) |
