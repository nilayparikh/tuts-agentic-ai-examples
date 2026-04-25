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

All commands below were run on 2026-04-25 from the example root.

### Shared Commands

`python util.py verify`

Result:

- passed `5/5`
- verified Python `3.11.9`
- verified all required packages
- verified all five finance input files
- verified endpoint and model resolution
- live LLM check returned `"Hello"`

Snippet:

```text
Verification Passed - 5/5
Ready for: python util.py -e cleanloop loop
```

`python util.py status`

Result:

- completed successfully
- reported Python `3.11.9`
- reported `.venv` and `.env` present
- reported current CleanLoop, Prompt Evolution, and Skill Mastery artifacts

### CleanLoop Commands

`python util.py -e cleanloop evaluate`

Result:

- command worked
- the current saved output at validation time scored `7/8`
- one deterministic judge check still failed: `matches_reference_output`

Snippet:

```text
Score: 7/8 - 1 Failing
Run: python util.py -e cleanloop loop to fix automatically
```

`python util.py -e cleanloop loop --max-iterations 1`

Result after repair:

- command worked
- AutoGen proposal path executed successfully
- one proposal was returned
- the candidate scored `5/8` and was reverted because it did not improve the baseline

Snippet:

```text
[LLM_ATTEMPT] Attempt 1/1: AutoGen proposer
[CODE_FOUND] yes
[MUTATION_SCORE] Candidate scored 5/8
[REVERT_MUTATION] Reverted mutation with score 5/8
```

`python util.py -e cleanloop loop --max-iterations 1 --rerank --candidates 2`

Result after repair:

- command worked
- reranker generated two candidates
- the selected candidate improved the round score from `5/8` to `7/8`
- the improved mutation was committed for that run

Snippet:

```text
[LLM_ATTEMPT] Attempt 1/2: AutoGen candidate 1: conservative
[LLM_ATTEMPT] Attempt 2/2: AutoGen candidate 2: value-first
[MUTATION_SCORE] Candidate scored 7/8
[COMMIT_MUTATION] Committed improved mutation at 7/8
```

`python util.py -e cleanloop challenge --levels 1`

Result after repair:

- command worked
- generated one adversarial CSV for level `1`

Snippet:

```text
Generating 1 adversarial CSVs across levels: [1]
Created: adversarial_d1_01.csv
```

`python util.py -e cleanloop sandbox --timeout 10`

Result:

- command worked
- genome completed in an isolated subprocess
- sandboxed output scored `7/8`

Snippet:

```text
OK: Genome completed successfully
NOTE: Score: 7/8
```

`python util.py -e cleanloop autonomy --rounds 3`

Result:

- command worked
- simulation finished in `SUPERVISED` mode with final score `0.40`

Snippet:

```text
Final: SUPERVISED (score: 0.40)
```

`python util.py -e cleanloop dashboard`

Result:

- command worked
- Streamlit launched successfully
- dashboard exposed a local URL on port `8501`

Snippet:

```text
Local URL: http://localhost:8501
```

`python util.py -e cleanloop reset`

Result:

- command worked
- deleted `cleanloop/.output`
- restored `cleanloop/clean_data.py` from `clean_data_starter.py`

Snippet:

```text
OK: Deleted cleanloop\.output
OK: Restored cleanloop/clean_data.py from clean_data_starter.py
```

## Validation Repairs Applied

The validation pass surfaced and fixed these issues:

1. GitHub Models was being routed to `AzureAIChatCompletionClient`, which does
   not support the structured-output path used by the loop.
2. Some OpenAI-compatible providers rejected AutoGen `json_schema` structured
   output even though plain JSON mode worked.
3. `python util.py -e cleanloop challenge --levels ...` did not match the
   actual challenger CLI.

The example now handles those three cases.

## Post-Validation State

After validation, the example was cleaned back to a neutral state:

- `cleanloop/.output/` was cleared via `python util.py -e cleanloop reset`
- `cleanloop/clean_data.py` was restored from `clean_data_starter.py`
- the temporary adversarial CSV generated during validation was removed
