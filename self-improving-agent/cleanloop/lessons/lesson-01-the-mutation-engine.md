# Lesson 01 — The Mutation Engine

This lesson gives you the full entry map for CleanLoop before the deeper lessons zoom into one mechanism. The important move is simple: resolve the runtime, prove the endpoint works, and keep the mutation boundary separate from the fixed judge.

## Command Path

Run these commands from `_examples/self-improving-agent/cleanloop/`:

```bash
python util.py status
python util.py verify
```

Why these two commands come first:

- `status` tells you what artifacts already exist and what the active model is.
- `verify` proves Python, packages, credentials, and one live LLM call all work before the loop tries to mutate anything.

## Captured Output

From `python util.py status`:

```text
Self-Improving Agent — Project Status

CleanLoop Input Files:
  finance_invoices.csv            15 rows
  finance_invoices_flags.csv      15 rows
  finance_invoices_regional.csv   15 rows
  finance_invoices_collections.csv 15 rows
  finance_invoices_adjustments.csv 15 rows

Environment:
  Python:   3.11.9
  .env:     exists
  Model:    microsoft/Phi-4
```

From `python util.py verify`:

```text
CleanLoop — Environment Verification

Step 1/5 — Python version
  OK: Python 3.11.9
Step 2/5 — Required packages
  OK: All 6 packages installed
Step 4/5 — API credentials
  OK: Endpoint: https://models.github.ai/infer...
  OK: API Key:  gi****jn
Step 5/5 — LLM connectivity
  OK: LLM replied: "Hello" (1.2s)
```

This is the real entry contract for the course. Before you discuss mutation, you prove the runtime can see the finance arena and talk to the configured model endpoint.

## Code References

1. [local status command in cleanloop/util.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/util.py)

   Important lines:

   ```python
     def _cmd_status(_args: argparse.Namespace) -> int:
       config = cleanloop_datasets.get_dataset_config()
       print("CleanLoop — Project Status")
       print("\nInput Files:")
       for path in cleanloop_datasets.get_input_paths(INPUT_DIR):
         print(f"  {path.name:<32} {_count_data_rows(path):>4} rows")
   ```

   Impact: this is the first surface the learner should trust. It binds the course to one dataset and one active runtime instead of letting the lesson drift into abstract framework talk.

2. [local verify command in cleanloop/util.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/util.py)

   Important lines:

   ```python
     def _cmd_verify(_args: argparse.Namespace) -> int:
       return _run_module_main("cleanloop.verify", [])
   ```

   Impact: this is the operational gate before any mutation round. Every later lesson depends on the fact that the runtime, the inputs, and the endpoint are already proven.

3. [resolve_llm_env in cleanloop/util.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/util.py#L105-L107) and [build_llm_client in cleanloop/util.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/util.py#L190-L193)

   Important lines:

   ```python
   def resolve_llm_env() -> dict[str, str]:
       return _resolve_llm_env()

   def build_llm_client(endpoint: str, api_key: str, api_version: str) -> Any:
       return _build_llm_client(endpoint, api_key, api_version)
   ```

   Impact: these two wrappers are the narrow runtime seam for the whole course. The loop never hardcodes a provider. It resolves one endpoint config and builds one compatible client.

4. [propose_single_mutation in autogen_runtime.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/autogen_runtime.py#L86-L121)

   Important lines:

   ```python
   def propose_single_mutation(
       client: Any,
       model: str,
       system_prompt: str,
       user_prompt: str,
   ) -> tuple[str | None, str, dict[str, object]]:
       proposal, events, usage = _run_structured_agent(...)
       code = proposal.clean_data_py.strip() or None
       hypothesis = proposal.hypothesis.strip() or "no hypothesis"
   ```

   Impact: this is where AutoGen becomes concrete. The proposer returns a full candidate genome plus a structured hypothesis, not just raw text.

## How The Pieces Connect

`status` tells you what exists. `verify` tells you the runtime works. `resolve_llm_env` and `build_llm_client` decide how the model is reached. Then `propose_single_mutation` becomes the first place where AutoGen can actually influence the genome.

## Hands-On Lab

Challenge:

Start at the local `util.py` command surface, then trace the runtime into `cleanloop/util.py` and `autogen_runtime.py`. Write down the exact point where provider configuration ends and structured mutation begins.

Success looks like this:

- You can point to the command that validates the environment.
- You can name the runtime function that resolves endpoint settings.
- You can explain why the proposer still does not own correctness.
