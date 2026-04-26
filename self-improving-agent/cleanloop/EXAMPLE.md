# CleanLoop Validation Notes

This file records the current validated command surface for the AutoGen-backed
CleanLoop example.

## AutoGen Wiring Audit

The current CleanLoop wiring is linked to AutoGen in these places:

- `cleanloop/util.py` builds AutoGen model clients.
- `cleanloop/util.py` uses `client.create(...)` for plain text completion checks.
- `cleanloop/autogen_runtime.py` uses `AssistantAgent` for mutation and judge calls.
- `cleanloop/autogen_runtime.py` uses `run_stream()` to collect event traces.
- `cleanloop/autogen_runtime.py` uses typed Pydantic models for mutation and reranker decisions.
- `cleanloop/loop.py` delegates proposal generation to `autogen_runtime.propose_single_mutation(...)`.
- `cleanloop/reranker.py` delegates candidate generation and selection to `autogen_runtime.propose_reranked_mutation(...)`.
- `cleanloop/verify.py` and `cleanloop/challenger.py` use the AutoGen model-client path through `cleanloop/util.py`.

There are no remaining direct OpenAI SDK calls in `cleanloop/`.

## Native Capability Audit

Native AutoGen capabilities used directly:

- `AssistantAgent`
- `run_stream()`
- AutoGen OpenAI-compatible model clients
- AutoGen Azure-backed model clients
- structured output when the provider supports `json_schema`

Custom logic that intentionally stays outside AutoGen:

- deterministic finance judging in `prepare.py`
- commit-or-revert orchestration in `loop.py`
- best-of-N scoring against the fixed judge
- dashboard log shaping and artifact persistence

This is the right boundary for the lesson. The example is not rebuilding
AutoGen team orchestration, `AgentTool`, selector chats, or workflow routing.
It uses AutoGen at the proposal and judge seam, then keeps the lesson's
selection pressure in deterministic Python.

## Provider Compatibility Note

Validation was run against a GitHub Models endpoint with `MODEL_NAME`
configured as `microsoft/Phi-4`.

Observed behavior:

- plain text completion works through AutoGen model clients
- AutoGen `AssistantAgent` with `output_content_type=...` did not work directly
  because the provider rejected `response_format.type=json_schema`
- the example now falls back to AutoGen model-client JSON mode using
  `response_format.type=json_object`, then validates the JSON with the same
  Pydantic schema locally

Observed warning:

- AutoGen warns that `microsoft/Phi-4` resolves internally to `phi4` for token
  estimation. The warning is not fatal, but it is useful to know when reading
  the command output.

## Command Validation

All commands below were run on 2026-04-26 from the `cleanloop/` folder.

### Shared Commands

`python util.py verify`

Result:

- passed `4/4`
- verified Python `3.11.9`
- verified all 7 required packages
- verified all five finance input files
- verified endpoint and model resolution
- live LLM check returned `"hello"`

Snippet:

```text
Result: 4/4 checks passed.

Ready for: python util.py loop
```

`python util.py status`

Result:

- completed successfully
- reported Python `3.11.9`
- reported `cleanloop/.env` present
- reported the finance arena with all five input files
- reported `.output` as missing in the reset baseline state

### CleanLoop Commands

`python util.py evaluate`

Result:

- command worked
- the starter-genome baseline now scores `11/11`
- the deterministic master export matches the canonical finance reference
- both mutation sidecars are present and readable

Snippet:

```text
CleanLoop Evaluation: 11/11
```

`python util.py loop --max-iterations 1`

Result after the three-export refresh:

- this command has not been revalidated since the starter genome reached `11/11`
- on the shipped finance arena, a fresh loop run now exits immediately unless you
  first add new anomalies or remove part of the mutation playbook

Recommended next step:

```text
python util.py challenge --levels 1
python util.py loop --max-iterations 1
```

`python util.py loop --max-iterations 1 --rerank --candidates 2`

Result after the three-export refresh:

- this command has not been revalidated since the starter genome reached `11/11`
- reranking is still useful after you generate harder anomalies with `challenge`
  or intentionally simplify the shipped mutation playbook

Recommended next step:

```text
python util.py challenge --levels 1 2
python util.py loop --max-iterations 1 --rerank --candidates 2
```

`python util.py challenge --levels 1`

Result after repair:

- command worked
- generated one adversarial CSV for level `1`

Snippet:

```text
Generating 1 adversarial CSVs across levels: [1]
Created: adversarial_d1_01.csv
```

`python util.py sandbox --timeout 10`

Result:

- command worked
- genome completed in an isolated subprocess
- sandboxed output scored `7/8`
- one deterministic judge check still failed: `matches_reference_output`

Snippet:

```text
[OK] Genome completed successfully
CleanLoop Evaluation: 7/8
```

`python util.py autonomy --rounds 3`

Result:

- command worked
- simulation finished in `SUPERVISED` mode with final score `0.27`

Snippet:

```text
Final: SUPERVISED (score: 0.27)
```

`python util.py dashboard`

Result:

- command worked
- Streamlit showed the optional first-run email prompt once
- Streamlit launched successfully
- dashboard exposed a local URL on port `8501`

Snippet:

```text
Local URL: http://localhost:8501
```

`python util.py reset`

Result:

- command worked
- deleted `cleanloop/.output`
- restored `cleanloop/clean_data.py` from `clean_data_starter.py`

Snippet:

```text
Deleted cleanloop/.output
Restored cleanloop/clean_data.py from clean_data_starter.py
```

## Validation Repairs Applied

The validation pass surfaced and fixed these issues:

1. GitHub Models was being routed to `AzureAIChatCompletionClient`, which does
   not support the structured-output path used by the loop.
2. Some OpenAI-compatible providers rejected AutoGen `json_schema` structured
   output even though plain JSON mode worked.
3. `python util.py challenge --levels ...` did not match the
   actual challenger CLI.

The example now handles those three cases.

## Post-Validation State

After validation, the example was cleaned back to a neutral state:

- `cleanloop/.output/` now contains the refreshed three-export baseline from the
  current starter genome
- `cleanloop/clean_data.py` and `cleanloop/clean_data_starter.py` are aligned
  on the deterministic-plus-mutation export contract
