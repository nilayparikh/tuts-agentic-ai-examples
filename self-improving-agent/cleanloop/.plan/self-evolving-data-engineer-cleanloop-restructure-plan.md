# CleanLoop Restructure Plan for Building the Self-Evolving Data Engineer

> Historical note: this plan describes the earlier package-by-lesson refactor
> shape. The current implementation is root-first. Use `README.md` and
> `docs/reference/code-map.md` for the live file layout.

## Purpose

This plan defines how to restructure the CleanLoop example so it teaches the
course `Building the Self-Evolving Data Engineer` more clearly.

The plan does not execute the refactor yet. It defines the target structure,
file moves, documentation scope, naming rules, tracing improvements, and the
validation sequence.

## Current State Summary

The current CleanLoop example already has the right core mechanics, but the
teaching surface is fragmented.

- Documentation is split across root files such as `ARCHITECTURE.md`,
  `EXAMPLE.md`, `README.md`, and `lessons/*.md`.
- Code is mostly flat in the `cleanloop/` root, which makes it harder to map
  each file to a lesson in the seven-part course.
- The finance fixture is now richer, but the teaching docs are not yet centered
  around the real sample data and export contract.
- Logging exists, but there is no single tracing model that follows one run,
  one round, one mutation, and one row-level decision from input to export.

## Design Goals

1. Keep only `README.md` at the CleanLoop root.
2. Move all explanatory material into `docs/`.
3. Align code layout to the seven-course lesson map.
4. Break large files into smaller teaching units with clear module docstrings.
5. Explain the process using the actual finance fixture and the actual tests.
6. Improve runtime logging into explicit trace-oriented observability.
7. Preserve current behavior while the layout changes.

## Naming Convention Rules

Use the course slug as the package anchor, but adapt it for valid Python module
names.

- Course title: `Building the Self-Evolving Data Engineer`
- Course slug: `self-evolving-data-engineer`
- Python package folder: `self_evolving_data_engineer`

Use this rule for code paths:

- top-level teaching package: `cleanloop/self_evolving_data_engineer/`
- lesson package folders: `lesson_01_mutation_engine/` through
  `lesson_07_production_safety/`
- filenames: snake_case and task-oriented, for example `cli_status.py`,
  `mutation_playbook.py`, `round_runner.py`

Use this rule for docs paths:

- retain the course slug style for docs and lesson folders because Markdown file
  names do not need to be import-safe
- example: `docs/lessons/01-mutation-engine.md`

This gives a clean course-to-code map without breaking Python imports.

## Target Folder Structure

```text
cleanloop/
  README.md
  docs/
    architecture/
      system-overview.md
      runtime-boundaries.md
      export-contract.md
    data/
      finance-fixture-walkthrough.md
      mutation-cases.md
      failure-cases.md
    lessons/
      01-mutation-engine.md
      02-pipeline-genome.md
      03-orchestrator.md
      04-observability-feedback.md
      05-judge-self-challenging.md
      06-test-time-search.md
      07-production-safety.md
    operations/
      setup-and-verify.md
      runbook.md
      tracing-and-logging.md
      reset-and-recovery.md
    testing/
      test-map.md
      export-contract-tests.md
      compatibility-tests.md
    reference/
      code-map.md
      naming-conventions.md
      module-dependency-map.md
  self_evolving_data_engineer/
    shared/
      paths.py
      tracing.py
      logging_utils.py
      csv_io.py
      text_normalization.py
    lesson_01_mutation_engine/
      cli_status.py
      cli_verify.py
      llm_env.py
      llm_client.py
      autogen_bridge.py
    lesson_02_pipeline_genome/
      dataset_contract.py
      input_loader.py
      date_normalizer.py
      amount_normalizer.py
      mutation_playbook.py
      export_writer.py
      starter_genome.py
      evolved_genome.py
      referee.py
    lesson_03_orchestrator/
      round_runner.py
      mutation_session.py
      snapshots.py
      artifact_restore.py
    lesson_04_observability_feedback/
      dashboard_app.py
      dashboard_metrics.py
      history_store.py
      event_stream.py
    lesson_05_judge_self_challenging/
      challenge_generator.py
      judge_contract.py
      evaluation_report.py
    lesson_06_test_time_search/
      reranker.py
      candidate_pool.py
      selection_report.py
    lesson_07_production_safety/
      sandbox_runner.py
      autonomy_policy.py
      reset_workflow.py
  clean_data.py
  clean_data_starter.py
  autogen_runtime.py
  loop.py
  prepare.py
  dashboard.py
  dashboard_metrics.py
  challenger.py
  reranker.py
  sandbox.py
  autonomy.py
  util.py
```

## Compatibility Strategy

The existing root Python files should not disappear in the first refactor pass.
They should become thin teaching wrappers that import from the new lesson-based
package.

Examples:

- `util.py` stays as the learner-facing command surface, but delegates to
  `self_evolving_data_engineer.lesson_01_mutation_engine.*`
- `clean_data.py` stays as the mutable genome entrypoint, but delegates to
  `lesson_02_pipeline_genome.evolved_genome`
- `clean_data_starter.py` stays as the reset baseline, but delegates to
  `lesson_02_pipeline_genome.starter_genome`
- `prepare.py`, `loop.py`, `dashboard.py`, `challenger.py`, `reranker.py`,
  `sandbox.py`, and `autonomy.py` stay import-compatible while the logic is
  moved behind them

This preserves the current CLI and test contract while the code becomes easier
to teach.

## Lesson-to-Code Map

### Lesson 01 — Mutation Engine

Primary teaching story:
local command surface, provider resolution, verification, AutoGen mutation seam

Move or extract:

- `util.py` into `cli_status.py`, `cli_verify.py`, `llm_env.py`, `llm_client.py`
- `autogen_runtime.py` into `autogen_bridge.py` plus structured proposal helpers

Documentation required:

- command path walkthrough
- provider resolution matrix
- verify flow with sample output

### Lesson 02 — Pipeline Genome

Primary teaching story:
dataset contract, deterministic cleanup, bounded mutation playbook, fixed judge

Move or extract:

- `datasets.py` into `dataset_contract.py`
- `clean_data_runtime.py` into `input_loader.py`, `date_normalizer.py`,
  `amount_normalizer.py`, `mutation_playbook.py`, `export_writer.py`
- `clean_data_starter.py` into `starter_genome.py`
- `clean_data.py` into `evolved_genome.py`
- `prepare.py` into `referee.py`, `judge_contract.py`, `evaluation_report.py`

Documentation required:

- row-by-row walkthrough from the real finance fixture
- export contract walkthrough using `55 / 25 / 5`
- inline coding notes for representative records such as `INV-101`, `INV-404`,
  `INV-502`, and `INV-112`

### Lesson 03 — Orchestrator

Primary teaching story:
proposal, run, score, commit-or-revert, artifact restore

Move or extract:

- `loop.py` into `round_runner.py`, `mutation_session.py`, `snapshots.py`,
  `artifact_restore.py`

Documentation required:

- one round lifecycle
- snapshot and restore rules
- failure and revert paths

### Lesson 04 — Observability & Feedback Signal

Primary teaching story:
history, score visibility, diagnostics, dashboard, traces

Move or extract:

- `dashboard.py` into `dashboard_app.py`
- `dashboard_metrics.py` into `dashboard_metrics.py` under lesson 04
- add `history_store.py` and `event_stream.py`

Documentation required:

- event types and history files
- dashboard panels and what they mean
- how to trace one mutation across proposal, run, judge, and output artifacts

### Lesson 05 — Judge & Self-Challenging

Primary teaching story:
fixed judge pressure and harder data generation

Move or extract:

- `challenger.py` into `challenge_generator.py`
- judge-related report formatting out of `prepare.py` into `evaluation_report.py`

Documentation required:

- referee invariants
- challenger-generated anomaly classes
- why the model never grades itself

### Lesson 06 — Test-Time Search & Re-Ranking

Primary teaching story:
candidate pool, comparison, judge-guided selection

Move or extract:

- `reranker.py` into `candidate_pool.py`, `reranker.py`, `selection_report.py`
- shared AutoGen rerank helpers into lesson 06 plus lesson 01 bridge seam

Documentation required:

- best-of-N flow
- candidate comparison format
- where the final selection is recorded

### Lesson 07 — Production Safety

Primary teaching story:
sandboxing, autonomy ladder, reset and recovery

Move or extract:

- `sandbox.py` into `sandbox_runner.py`
- `autonomy.py` into `autonomy_policy.py`
- reset logic out of `util.py` into `reset_workflow.py`

Documentation required:

- production failure modes and the control that contains each one
- reset semantics that preserve `.output`
- trust ladder explanation tied to the real simulation output

## Documentation Work Plan

### Root README Policy

Keep `README.md` as the only root documentation file.

Its job should be minimal:

- what CleanLoop is
- how the course maps to the example
- where docs live
- how to run the first commands
- where the learner goes next

Everything else should move into `docs/`.

### Files To Move or Rewrite Under docs/

- move `ARCHITECTURE.md` into `docs/architecture/system-overview.md`
- move `EXAMPLE.md` into `docs/operations/setup-and-verify.md` or
  `docs/testing/test-map.md` depending on final content split
- move `lessons/*.md` into `docs/lessons/`
- add a new `docs/reference/code-map.md`
- add a new `docs/reference/naming-conventions.md`
- add a new `docs/reference/module-dependency-map.md`
- add a new `docs/data/finance-fixture-walkthrough.md`
- add a new `docs/data/mutation-cases.md`
- add a new `docs/data/failure-cases.md`
- add a new `docs/operations/tracing-and-logging.md`

### Documentation Quality Rules

Every Markdown file under `docs/` should:

- start with a clear H1
- state the lesson or subsystem it belongs to
- explain the real fixture, not a toy abstraction
- include at least one concrete path reference
- include at least one small code example or inline coding explanation where it
  helps a learner follow the control flow
- stay aligned with the current tests and shipped outputs

## Actual Test Data Documentation Scope

The new docs should explain the finance arena with the real sample, not fake
illustrations.

Required examples to document explicitly:

- deterministic success rows from the fixture
- mutation success rows using spacing, emoji, and reordered labels
- side-metadata repairs using `adjusted_amount` and `resolution_amount`
- unresolved failures that stay in `finance_mutation_failures.csv`

Minimum concrete cases to show in docs:

- `INV-101` as a plain deterministic row
- `INV-404` as a token-canonicalized zero map case
- `INV-502` as an approved adjusted amount case
- `INV-106` or `INV-203` as an approved resolution amount case
- `INV-112` and `INV-312` as true failures

Reference metrics that docs must stay aligned with:

- 5 finance input files
- 60 input rows total
- 55 rows in `finance_master.csv`
- 25 rows in `finance_mutation_success.csv`
- 5 rows in `finance_mutation_failures.csv`

## Logging and Tracing Plan

### Target Outcome

Move from mixed print-style diagnostics to a trace model that explains one run
across the whole loop.

### Add Shared Tracing Contract

Create a shared tracing layer under `self_evolving_data_engineer/shared/`.

Core fields:

- `trace_id`
- `run_id`
- `round_id`
- `stage`
- `component`
- `invoice_id` when row scoped
- `decision`
- `score_before`
- `score_after`
- `source_file`
- `output_file`
- `model`
- `latency_ms`

### Instrumentation Targets

- CLI entry and exit
- provider resolution
- proposal request and response
- rerank candidate generation and selection
- deterministic row normalization
- mutation playbook rule match
- anomaly failure routing
- referee checks and metrics
- snapshot capture and restore
- commit, revert, timeout, and skip paths

### Trace Outputs

Add explicit trace artifacts, preferably JSONL, under `.output/traces/`.

Suggested files:

- `.output/traces/run-events.jsonl`
- `.output/traces/row-decisions.jsonl`
- `.output/traces/proposal-events.jsonl`

### Logging Policy

- keep console output plain text only
- keep learner-facing messages concise
- keep structured trace data machine-readable
- document how console logs map to stored trace records

## Execution Phases

### Phase 0 — Freeze Current Baseline

- capture current tree and docs inventory
- capture current import graph for root Python files
- capture current test baseline with
  `python -m unittest tests.test_python_compat tests.test_cleanloop_exports`

### Phase 1 — Documentation Consolidation

- create `docs/` subtree
- move non-README root docs into `docs/`
- move lesson docs into `docs/lessons/`
- update root `README.md` to point into the new docs tree

Exit condition:

- root only keeps `README.md` as documentation
- all moved docs still open cleanly and cross-links resolve

### Phase 2 — Course-Aligned Package Extraction

- create `self_evolving_data_engineer/`
- extract shared helpers first
- extract lesson 02 runtime modules next because that is the densest learning surface
- keep root wrappers intact so tests and commands keep working

Exit condition:

- imports resolve
- public commands still run through existing entry files

### Phase 3 — Lesson-Specific Splits

- split lesson 01, 03, 04, 05, 06, and 07 surfaces
- add module docstrings and minimal inline comments only where the teaching flow
  benefits from explanation
- avoid large unrelated logic changes while moving files

Exit condition:

- each course lesson has an obvious folder and code map
- each extracted module has a single teaching purpose

### Phase 4 — Tracing Upgrade

- add shared tracing helpers
- instrument loop, runtime, judge, reranker, sandbox, and reset
- persist trace files in `.output/traces/`
- add docs for reading traces during the course

Exit condition:

- one learner can follow a run from CLI invocation to export files with trace IDs

### Phase 5 — Fixture-Centered Documentation Rewrite

- rewrite docs around the real finance fixture and export contract
- add code map and naming conventions docs
- add inline coding walkthroughs lesson by lesson
- remove stale counts and provider descriptions from older docs

Exit condition:

- the docs explain the real sample, the real tests, and the real runtime seams

### Phase 6 — Validation and Cleanup

- rerun focused unit tests after each extraction slice
- rerun the full touched Python suite at the end
- clean dead imports and outdated references
- verify that root wrappers still preserve the lesson command surface

Exit condition:

- tests pass
- docs match current behavior
- no stale root docs remain except `README.md`

## Validation Gates

Run these gates during execution:

1. `python -m unittest tests.test_cleanloop_exports`
2. `python -m unittest tests.test_python_compat`
3. `python -m unittest tests.test_python_compat tests.test_cleanloop_exports`

Add or update tests as the refactor progresses:

- import-compatibility tests for root wrappers
- trace artifact existence and schema tests
- docs-path smoke checks if doc links become important to the learner flow

## Risks and Mitigations

### Risk 1

The refactor could break the existing learner command surface.

Mitigation:

keep root wrappers stable until the last cleanup phase.

### Risk 2

Docs can become stale again if they restate counts manually.

Mitigation:

tie docs to the actual fixture and current test expectations, and explicitly
review docs whenever the fixture changes.

### Risk 3

Splitting the runtime too aggressively could make the teaching flow harder to
follow.

Mitigation:

split by lesson story and single responsibility, not by micro-abstraction.

### Risk 4

Tracing can overwhelm learners if it is too noisy.

Mitigation:

separate concise console messages from structured trace files, and document the
high-value trace fields first.

## Recommended Execution Order

1. Consolidate docs under `docs/`.
2. Create the course-aligned package skeleton.
3. Extract lesson 02 runtime and judge pieces.
4. Extract lesson 01 CLI and AutoGen seams.
5. Extract orchestrator and observability modules.
6. Add tracing.
7. Rewrite the docs around the real fixture and tests.
8. Run final compatibility and regression validation.

## Deliverables

When execution is complete, this work should produce:

- one clean root README
- one complete `docs/` knowledge tree
- one course-aligned package structure under `self_evolving_data_engineer/`
- import-compatible root entry files
- richer trace artifacts and tracing docs
- lesson-by-lesson inline coding explanations tied to the real finance sample
