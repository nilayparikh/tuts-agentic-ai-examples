# CleanLoop Agenda

[![Watch: AI That Improves Itself: The "Bounded Recipe" for Agents](https://img.youtube.com/vi/loYCwyRU_tM/maxresdefault.jpg)](https://www.youtube.com/watch?v=loYCwyRU_tM)

> <strong>Watch the video:</strong> <a href="https://www.youtube.com/watch?v=loYCwyRU_tM" target="_blank" rel="noopener noreferrer">AI That Improves Itself: The "Bounded Recipe" for Agents</a>
> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>

## Goal

Merge the five finance invoice CSVs into one normalized receivables table with
parseable dates and numeric values.

## What This Example Shows

This CleanLoop variant is now wired through AutoGen's AgentChat runtime instead
of a single raw completion call. The lesson still stays bounded: one mutable
genome, one fixed judge, one reranking stage, and one observable orchestrator
loop.

The example demonstrates:

1. Code mutation: the proposer suggests a concrete replacement for the
   `clean` function.
2. Genome improvement: the loop only commits a mutation when the referee score
   improves.
3. Orchestrator loop: the bounded run resets the starter genome, evaluates the
   current candidate, proposes a mutation, and re-evaluates it.
4. Loop observability: each round records attempt diagnostics, token usage, and
   log rows for the dashboard.
5. Judge: the finance referee remains the hard gate for score and pass/fail
   assertions.
6. Re-ranking: best-of-N candidate generation is available before the final
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

## Requirements

1. Use only the five finance\_\*.csv inputs.
2. Normalize every file into date, entity, value, category.
3. Preserve good rows even when amount strings contain symbols, sentinels, or notes.
4. Handle mixed date formats without inventing or dropping records.
5. Match the canonical finance reference in cleanloop/.gold/finance_expected.csv.

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

## Validation Commands

The full validated command set for this example is documented in
`cleanloop/EXAMPLE.md`.

The current validated snapshot starts from the weak starter genome at `5/8` on
`evaluate`, then reaches `7/8` on the reranked one-iteration loop before reset.
Use `EXAMPLE.md` for the exact command outputs from the latest validation pass.

- `verify` checks package imports, finance input files, credentials, and one live LLM call.
- `evaluate` runs the deterministic referee on the current output file.
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
