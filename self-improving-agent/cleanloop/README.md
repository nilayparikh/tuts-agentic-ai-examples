# CleanLoop Agenda

[![Watch: AI That Improves Itself: The "Bounded Recipe" for Agents](https://img.youtube.com/vi/loYCwyRU_tM/maxresdefault.jpg)](https://www.youtube.com/watch?v=loYCwyRU_tM)

> <strong>Watch the video:</strong> <a href="https://www.youtube.com/watch?v=loYCwyRU_tM" target="_blank" rel="noopener noreferrer">AI That Improves Itself: The "Bounded Recipe" for Agents</a>
> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>

## Goal

Run a deterministic finance cleaning pass first, then route mutation-fixed rows
and unresolved anomalies into separate export reports beside the canonical
master CSV.

## What This Example Shows

This CleanLoop variant is now wired through AutoGen's AgentChat runtime instead
of a single raw completion call. The lesson still stays bounded: one mutable
genome, one fixed judge, one reranking stage, and one observable orchestrator
loop.

The example demonstrates:

1. Deterministic pass: numeric-like rows are normalized directly into the
   canonical finance schema.
2. Mutation fallback: known textual anomalies are fixed into
   `finance_mutation_success.csv`, then merged into `finance_master.csv`.
3. Failure routing: unresolved anomalies are dumped into
   `finance_mutation_failures.csv` for later mutation review.
4. Genome improvement: the loop still mutates `clean_data.py`, but now it does
   so against an explicit export contract instead of a single loose CSV.
5. Loop observability: each round records attempt diagnostics, token usage, and
   log rows for the dashboard.
6. Judge: the finance referee remains the hard gate for score and pass/fail
   assertions.
7. Re-ranking: best-of-N candidate generation is available before the final
   mutation is selected.

## Course Alignment

Use this map when you move between the runnable example, the canonical course
plan in `content/ai/self-improving-agents/course/`, and the current slide deck
topics.

| Course lesson | Topic                 | Primary example anchor                                                               |
| ------------- | --------------------- | ------------------------------------------------------------------------------------ |
| 03            | Arena and baseline    | `.input/`, `.gold/`, `prepare.py`, `clean_data_starter.py`                           |
| 04            | Orchestrator loop     | `loop.py`                                                                            |
| 05            | Genome improvement    | `clean_data.py`                                                                      |
| 06            | Loop observability    | `dashboard.py`, `.output/finance_eval_history.json`, `.output/finance_strategy.json` |
| 07            | Self-challenging loop | `challenger.py`                                                                      |
| 08            | Test-time search      | `reranker.py`                                                                        |
| 09            | Safety and autonomy   | `sandbox.py`, `autonomy.py`                                                          |

The slide topics for self-challenging, test-time search, and production safety
cover the same extension path as lessons 07-09 in the course plan, even when
the deck numbering is on an older sequence.

## AutoGen Architecture

The AutoGen integration is intentionally narrow.

- `util.py` owns local `.env` loading and model client creation.
- `autogen_runtime.py` owns structured mutation proposals, judge selection, and
  stream/event serialization.
- `loop.py` remains the orchestrator and artifact writer.
- `reranker.py` produces multiple candidates, then asks AutoGen to select the
  best one.
- `prepare.py` stays the fixed judge. The model does not grade itself.

This keeps the teaching point clear: the agent can propose mutations, but the
score still comes from deterministic evaluation.

## Finance Arena

You are cleaning one progressive invoice arena, not choosing between datasets.

## Input Files

- finance_invoices.csv
- finance_invoices_flags.csv
- finance_invoices_regional.csv
- finance_invoices_collections.csv
- finance_invoices_adjustments.csv

## Required Output Columns

date, entity, value, category

## Output Files

- `finance_master.csv` — all deterministic rows plus mutation-fixed rows
- `finance_mutation_success.csv` — only rows fixed by the shipped mutation playbook
- `finance_mutation_failures.csv` — unresolved anomaly dump for review

## Requirements

1. Use only the five finance\_\*.csv inputs.
2. Write `finance_master.csv` with the canonical columns `date, entity, value, category`.
3. Write `finance_mutation_success.csv` with the same canonical schema.
4. Write `finance_mutation_failures.csv` as the unresolved anomaly dump.
5. Preserve good rows even when amount strings contain symbols, sentinels, or notes.
6. Handle mixed date formats without inventing or dropping records.
7. Match the canonical finance reference in cleanloop/.gold/finance_expected.csv.

## Mutation Playbook

The shipped starter genome uses a tiny mutation playbook for the known textual
amount tokens in this arena.

- `FREE TRIAL` → write `0.0`, preserve the current category, and report the row in `finance_mutation_success.csv`
- `COMPLIMENTARY` → write `0.0`, preserve the current category, and report the row in `finance_mutation_success.csv`
- `OFFSET` → write `0.0`, preserve the `disputed` category, and report the row in `finance_mutation_success.csv`
- `PENDING`, `TBD`, `ERROR`, `ERR`, `CHARGEBACK`, `REVERSAL`, blank values, and other unmapped tokens → dump the row in `finance_mutation_failures.csv`

## Constraints

- You may only modify the `clean` function in `clean_data.py`.
- Do not change function signatures or imports.
- Do not modify `cleanloop/prepare.py`, `cleanloop/datasets.py`, or this file.

## Self-Contained Runtime

This example now brings its own runtime helpers and environment file.

- Example-local env template: `cleanloop/.env.example`
- Example-local env file: `cleanloop/.env`
- Local runtime helpers: `cleanloop/util.py`
- AutoGen bridge: `cleanloop/autogen_runtime.py`

Supported endpoint families in the local runtime:

- GitHub Models via OpenAI-compatible APIs
- Azure OpenAI
- Azure AI Inference endpoints

## Setup

1. Install dependencies from the example root, or use the parent `requirements.txt`
   when you stay inside `cleanloop/`.
2. Fill `cleanloop/.env` with your endpoint, API key, model, and optional API version.
3. Run the verifier before the loop so credential and package issues fail early.

If you are working inside `_examples/self-improving-agent/cleanloop/`, install
dependencies like this:

```bash
pip install -r ../requirements.txt
python util.py verify
```

If you are using a slower OpenAI-compatible endpoint such as NVIDIA, you can
raise the verify-only timeout in `cleanloop/.env`:

```dotenv
CLEANLOOP_VERIFY_TIMEOUT_SECONDS=45
```

Then use the local `util.py` wrapper for the lesson commands:

```bash
python util.py status
python util.py verify
python util.py evaluate
python util.py loop --max-iterations 5
python util.py loop --max-iterations 5 --rerank --candidates 3
python util.py challenge --levels 1 2 3
python util.py sandbox --timeout 10
python util.py autonomy --rounds 10
python util.py dashboard
python util.py reset
```

## Running the Loop

Use the local wrapper for loop runs as well:

```bash
python util.py loop --max-iterations 5
```

Use reranking when you want best-of-N candidate selection before commit:

```bash
python util.py loop --max-iterations 5 --rerank --candidates 3
```

For normal usage in this example repo, prefer the local `util.py` wrapper in
`cleanloop/` because it loads `cleanloop/.env` first and keeps every lesson
command runnable from the example folder itself.

The shipped starter genome now satisfies the built-in finance arena. If you
want to see fresh mutation rounds, generate new adversarial inputs with
`python util.py challenge --levels ...` or deliberately simplify the mutation
playbook in `clean_data.py` before running `loop`.

## Validation Commands

The full validated command set for this example is documented in
`cleanloop/EXAMPLE.md`.

Use `evaluate` to verify the master export plus both mutation sidecars before
you run the loop. Use `EXAMPLE.md` for command surface notes and any refreshed
validation snippets.

- `verify` checks package imports, finance input files, credentials, and one live LLM call.
- `evaluate` checks `finance_master.csv` plus the two mutation sidecars.
- `loop` runs one bounded mutation loop.
- `loop --rerank` runs best-of-N proposal generation plus AutoGen judge selection.
- `challenge` generates adversarial CSV files through the AutoGen model client path.
- `sandbox` runs the genome in a subprocess before scoring it.
- `autonomy` simulates the trust ladder without changing the genome.
- `dashboard` launches the Streamlit monitor.
- `reset` deletes `.output` and restores `clean_data.py` from the starter genome.

## Observability

The loop persists round history and log artifacts so you can inspect what the
agent tried instead of treating the mutation as a black box.

- Master export: `cleanloop/.output/finance_master.csv`
- Mutation success report: `cleanloop/.output/finance_mutation_success.csv`
- Mutation failure dump: `cleanloop/.output/finance_mutation_failures.csv`
- Round history: `cleanloop/.output/finance_eval_history.json`
- Dashboard logs: surfaced through `cleanloop/dashboard.py`
- Attempt diagnostics: prompt size, response size, token counts, selected
  attempt, and abbreviated message stream

## AutoGen Notes

AutoGen is in maintenance mode, but this example uses it because the lesson ask
is specifically about the AutoGen framework. The integration stays close to the
current AgentChat APIs:

- `AssistantAgent` for proposal and judge-agent behavior
- `run_stream()` for observability and stream capture
- structured output models for mutation and reranking decisions when the provider accepts `json_schema`
- model clients from `autogen-ext` for OpenAI-compatible and Azure-backed endpoints

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

| Lesson | Video                                                                                                   | Example Folder  |
| ------ | ------------------------------------------------------------------------------------------------------- | --------------- |
| 01     | [AI That Improves Itself: The "Bounded Recipe" for Agents](https://www.youtube.com/watch?v=loYCwyRU_tM) | [cleanloop](./) |
