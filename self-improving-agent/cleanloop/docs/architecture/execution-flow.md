# Traced Execution Flow

This document reconstructs the real CleanLoop execution path from the shipped
runtime code and the current artifacts under `.output/`.

It is grounded in these files:

- `.output/finance_eval_history.json`
- `.output/finance_strategy.json`
- `.output/logs/finance_round_logs.jsonl`
- `.output/traces/run-events.jsonl`
- `.output/traces/row-decisions.jsonl`
- `.output/traces/proposal-events.jsonl`

## Reference Runs Used In This Diagram

- Starter baseline runtime: `dc729b9ec5574972b551e92bfc452c80`
  - `allow_mutations=false`
  - `30` `deterministic_row`
  - `30` `requires_mutation_playbook`
- Successful full runtime: `bcbafd7446364124808b4280c7865c36`
  - `allow_mutations=true`
  - `30` `deterministic_row`
  - `25` `mutation_fixed`
  - `5` `mutation_failure`
- Latest loop run: `1da2e0c0a3b741d4a4940beb8eaf248a`
  - `max_iterations=2`
  - `candidate_count=3`
  - `use_reranker=false`
  - both rounds reverted

## Run

### Commands

```powershell
python util.py reset
python util.py evaluate
python util.py loop --max-iterations 1
python util.py loop --max-iterations 1 --rerank --candidates 2
python util.py dashboard
python util.py sandbox --timeout 10
python util.py autonomy --rounds 5
```

### Output

```text
$ python util.py evaluate
Ran genome. Output: Y:\.sources\localm-tuts\courses\_examples\self-improving-agent\cleanloop\.output\finance_master.csv
    CleanLoop Evaluation: 13/14
    [FAIL] matches_reference_output: matched=30, missing=25, unexpected=0, output_rows=30, reference_rows=55

$ python util.py loop --max-iterations 1
[CURRENT_SCORE] Score 13/14
[REQUESTING_LLM_PROPOSAL] Requesting mutation proposal from model microsoft/Phi-4
[HYPOTHESIS_SELECTED] Implement deterministic normalization and a mutation playbook to reconcile missing and unexpected rows.
[REVERT_MUTATION] Reverted mutation with score 0/1
History saved to Y:\.sources\localm-tuts\courses\_examples\self-improving-agent\cleanloop\.output\finance_eval_history.json

$ python util.py loop --max-iterations 1 --rerank --candidates 2
    Reranker: generating 2 candidates...
[LLM_ATTEMPT] Attempt 1/2: AutoGen candidate 1: conservative
[LLM_ATTEMPT] Attempt 2/2: AutoGen candidate 2: value-first
[REVERT_MUTATION] Reverted mutation with score 13/14

$ python util.py dashboard
    Local URL: http://localhost:8501

$ python util.py sandbox --timeout 10
    [OK] Genome completed successfully

$ python util.py autonomy --rounds 5
Final: SUPERVISED (score: 0.48)
```

### Explanation

1. `reset` and `evaluate` recreate the starter baseline used by the `Lesson 02 Slice - Runtime Row Routing` diagram.
2. `loop --max-iterations 1` exercises the non-reranked path used by `Lesson 03 Slice - One Loop Round`. The key validation is the revert after a worse candidate.
3. `loop --max-iterations 1 --rerank --candidates 2` exercises the search branch used by `Lesson 06 Slice - Re-Ranker Search Path`.
4. `dashboard`, `sandbox`, and `autonomy` connect the observability and safety slices back to [Lesson 04](../lessons/04-observability-feedback.md) and [Lesson 07](../lessons/07-production-safety.md).

## Full Execution Diagram

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant C as "util.py _cmd_loop"
    participant R as "loop.run_loop"
    participant F as "loop._prepare_fresh_run"
    participant P as "prompt builders"
    participant G as "clean_data.clean"
    participant RT as "clean_data_runtime._clean_impl"
    participant LD as "read_finance_records"
    participant NM as "normalize_numeric_amount"
    participant MP as "apply_mutation_playbook"
    participant RR as "resolve_mutation_rule"
    participant J as "prepare.evaluate"
    participant A as "autogen_runtime.propose_single_mutation"
    participant S as "commit or revert gate"

    U->>C: python util.py loop --max-iterations 2
    C->>R: run_loop(max_iterations=2, use_reranker=false, n_candidates=3)
    R->>P: build_system_prompt(dataset="finance")
    Note over P: System message carries agenda, assertion registry, export contract, mutation playbook, and immutable boundary rules.

    R->>F: _prepare_fresh_run(config, output_path, history_path)
    F-->>R: remove stale finance artifacts
    F-->>R: restore clean_data.py from clean_data_starter.py

    R->>R: round 1 begins
    R->>G: _run_and_evaluate(clean_data, prepare, INPUT_DIR, output_path)
    G->>RT: clean_starter(input_dir, output_path)
    RT->>RT: _clean_impl allow_mutations=false
    RT->>LD: read_finance_records for 5 input files

    loop for each record
        RT->>NM: normalize_numeric_amount(record)
        alt numeric-like amount
            NM-->>RT: value, None
            RT->>RT: build_normalized_row(record, value)
            RT-->>RT: trace deterministic_row
        else needs mutation playbook and allow_mutations=false
            NM-->>RT: None, requires_mutation_playbook
            RT->>RT: build_failure_row for starter stop
            RT-->>RT: trace requires_mutation_playbook
        end
    end

    Note over RT: Baseline trace run dc729 produced 30 deterministic rows and 30 mutation-needed rows.
    RT-->>G: write finance_master.csv = 30 rows
    RT-->>G: write finance_mutation_success.csv = 0 rows
    RT-->>G: write finance_mutation_failures.csv = 30 rows
    G->>J: prepare.evaluate(finance_master.csv)
    J-->>R: score 13 of 14, failed = matches_reference_output
    Note over J: finance_eval_history.json recorded matched=30, missing=25, unexpected=0, output_rows=30, reference_rows=55.

    R->>R: build metacognition snapshot
    R->>P: build_user_prompt with current genome, failures, history, and focus_area=row_reconciliation
    R->>A: _propose_fix using system prompt and user prompt
    Note over A: Latest round-1 logs: model=microsoft/Phi-4, prompt_tokens=2686, completion_tokens=895, response_chars=3306.
    A-->>R: MutationProposal with hypothesis, clean_data_py, mutation_summary
    R->>R: validate candidate code
    R->>R: write candidate to clean_data.py and reload clean_data
    R->>G: _run_and_evaluate(mutated clean_data, prepare, INPUT_DIR, output_path)
    G-->>R: failed = can_run_genome date, score = 0 of 1
    R->>S: compare new_score=0 vs baseline score=13
    S-->>R: revert candidate
    R->>R: restore genome and output snapshots
    R-->>R: proposal-events.jsonl records candidate_generated then revert

    opt full runtime with mutations enabled
        U->>G: python util.py evaluate or direct clean_data.clean()
        G->>RT: clean(input_dir, output_path)
        RT->>RT: _clean_impl allow_mutations=true
        loop for each non-deterministic record
            RT->>MP: apply_mutation_playbook(record)
            MP->>RR: resolve_mutation_rule(record)
            alt strategy == adjusted_amount
                RR-->>MP: adjusted_amount rule
                MP->>MP: normalize_adjusted_amount(record)
            else strategy == resolution_amount
                RR-->>MP: resolution_amount rule
                MP->>MP: normalize_resolution_amount(record)
            else strategy == zero_value
                RR-->>MP: zero_value rule
                MP->>MP: repaired_value = 0.0
            end
            MP->>MP: build_normalized_row(record, repaired_value)
            alt rule succeeds
                MP-->>RT: mutated_row, mutation_fixed, mutation_hint
                RT-->>RT: trace mutation_fixed
            else rule unresolved
                MP-->>RT: None, anomaly_reason, mutation_hint
                RT-->>RT: trace mutation_failure
            end
        end
        Note over RT: Successful run bcbafd produced 30 deterministic_row, 25 mutation_fixed, 5 mutation_failure.
        RT-->>G: write finance_master.csv = 55 rows
        RT-->>G: write finance_mutation_success.csv = 25 rows
        RT-->>G: write finance_mutation_failures.csv = 5 rows
        G->>J: prepare.evaluate(finance_master.csv)
        J-->>U: fixed referee decides pass or fail against .gold/finance_expected.csv
    end
```

## Lesson-Aligned Diagram Slices

These are smaller execution slices that map cleanly to the lesson flow.

### Lesson 02 Slice — Runtime Row Routing

```mermaid
flowchart TD
    input[5 finance CSV inputs]
    read[read_finance_records]
    normalize[normalize_numeric_amount]
    deterministic[30 deterministic_row]
    playbook[apply_mutation_playbook]
    fixed[25 mutation_fixed]
    failed[5 mutation_failure]
    master[finance_master.csv 55 rows]
    success[finance_mutation_success.csv 25 rows]
    failure[finance_mutation_failures.csv 5 rows]

    input --> read --> normalize
    normalize -->|numeric-like| deterministic
    normalize -->|needs mutation playbook| playbook
    playbook -->|rule succeeds| fixed
    playbook -->|rule unresolved| failed
    deterministic --> master
    fixed --> master
    fixed --> success
    failed --> failure
```

### Lesson 03 Slice — One Loop Round

```mermaid
flowchart TD
    starter[restore starter genome]
    baseline[run starter genome]
    judge[prepare.evaluate]
    baselineScore[baseline score 13 of 14]
    meta[focus_area = row_reconciliation]
    prompt[build system and user prompts]
    llm[Phi-4 proposal]
    candidate[write candidate genome]
    rerun[re-run candidate]
    failed[can_run_genome date]
    decision{score improved?}
    revert[restore previous genome and outputs]

    starter --> baseline --> judge --> baselineScore --> meta --> prompt --> llm --> candidate --> rerun --> failed --> decision
    decision -->|no| revert
```

### Lesson 04 Slice — Artifact Feedback

```mermaid
flowchart LR
    runtime[clean_data_runtime]
    loopRun[loop.run_loop]
    runEvents[run-events.jsonl]
    rowDecisions[row-decisions.jsonl]
    proposalEvents[proposal-events.jsonl]
    evalHistory[finance_eval_history.json]
    strategy[finance_strategy.json]
    logs[finance_round_logs.jsonl]

    runtime --> runEvents
    runtime --> rowDecisions
    loopRun --> proposalEvents
    loopRun --> evalHistory
    loopRun --> strategy
    loopRun --> logs
```

### Lesson 05 Slice — Fixed Judge And Harder Arena

```mermaid
flowchart LR
    challenge[challenger.generate_messy_csv]
    input[adversarial CSV files written into .input]
    genome[clean_data.clean]
    outputs[master and mutation exports]
    judge[prepare.evaluate]
    gold[.gold/finance_expected.csv]
    results[score plus failed assertions]
    next[next mutation pressure]

    challenge --> input --> genome --> outputs --> judge --> results --> next
    gold --> judge
```

This slice combines two surfaces.

- The fixed judge path is already visible in current `.output` history and traces.
- The challenger path is defined in `challenger.py`, but the current `.output/`
  artifacts do not include a traced challenger run.

### Lesson 06 Slice — Re-Ranker Search Path

```mermaid
flowchart TD
    failures[failed assertions]
    genome[genome code]
    styles[candidate styles]
    propose[propose_single_mutation N times]
    isolate[temp directory per candidate]
    run[run candidate clean function]
    judge[prepare.evaluate]
    candidates[candidate score records]
    tie{equal top score?}
    auto[pick highest score]
    judgeTie[cleanloop_judge tie-break]
    selected[selected candidate]

    failures --> propose
    genome --> propose
    styles --> propose
    propose --> isolate --> run --> judge --> candidates --> tie
    tie -->|no| auto --> selected
    tie -->|yes| judgeTie --> selected
```

The current `.output` history shows `use_reranker=false` for the latest loop
run, so this slice is a code-path explanation derived from `reranker.py` and
`autogen_runtime.py`, not a traced artifact from the current log set.

### Lesson 07 Slice — Safety, Trust, And Recovery

```mermaid
flowchart LR
    genome[clean_data.py]
    sandbox[run_sandboxed]
    outcome[success or crash or timeout]
    evaluate[optional prepare.evaluate after sandbox success]
    trust[TrustState record_round]
    resetCmd[python util.py reset]
    restore[reset_to_starter]
    starter[clean_data_starter.py]
    kept[.output preserved]

    genome --> sandbox --> outcome
    outcome -->|success| evaluate --> trust
    outcome -->|failure| trust
    resetCmd --> restore
    starter --> restore
    restore --> genome
    restore --> kept
```

The current architecture artifacts do not include saved sandbox runs or reset
audit files, so this slice is grounded in `sandbox.py`, `autonomy.py`, and
`reset_workflow.py` rather than in `.output/traces`.

## Actual Call Chain

1. `util.py::_cmd_loop()` calls `loop.run_loop()`.
2. `loop.run_loop()` calls `build_system_prompt()` once, then `_prepare_fresh_run()`.
3. Each round calls `_run_and_evaluate()`.
4. `_run_and_evaluate()` calls `clean_data.clean()` and then `prepare.evaluate()`.
5. In the starter baseline, `clean_data.clean()` delegates to `clean_data_runtime.clean_starter()`, which calls `_clean_impl(... allow_mutations=false)`.
6. `_clean_impl()` calls `read_finance_records()`, `normalize_numeric_amount()`, `build_normalized_row()`, `build_failure_row()`, and `write_rows()`.
7. In the mutation-enabled path, `_clean_impl()` also calls `apply_mutation_playbook()`.
8. `apply_mutation_playbook()` calls `resolve_mutation_rule()`, then either `normalize_adjusted_amount()` or `normalize_resolution_amount()` when the rule requires local business context.
9. After baseline evaluation, `loop.run_loop()` calls `_build_metacognition_snapshot()`, `build_user_prompt()`, and `_propose_fix()`.
10. `_propose_fix()` calls `autogen_runtime.propose_single_mutation()`, which calls `_run_structured_agent()` and returns a structured `MutationProposal`.
11. The loop validates and writes the candidate, re-runs `_run_and_evaluate()`, then commits or reverts based on the fixed score delta.

## What Each Message Sends

### System Prompt To The LLM

`build_system_prompt()` sends the operating contract:

- dataset agenda
- assertion registry
- export contract
- mutation playbook
- immutable boundary rules
- output format rule: one-line hypothesis plus full `clean_data.py`

### User Prompt To The LLM

`build_user_prompt()` sends round-specific evidence:

- current `clean_data.py`
- failed assertions
- passed assertions
- up to three previous attempts
- metacognition snapshot with `focus_area` and `guidance`

### Response From The LLM

`autogen_runtime.propose_single_mutation()` expects a structured payload:

- `hypothesis`
- `clean_data_py`
- `mutation_summary`

The current logs show the model returned code, but the selected candidate still
failed at runtime with `can_run_genome: 'date'`, so the selection gate rejected
it.

## Actual Counts That Matter

### Starter Baseline In The Current Loop

- input files scanned: `5`
- deterministic rows exported: `30`
- rows stopped for mutation work: `30`
- master rows written: `30`
- fixed referee score before mutation: `13/14`
- failing assertion: `matches_reference_output`
- missing rows against reference: `25`

### Full Mutation-Capable Runtime

- deterministic rows: `30`
- mutation-fixed rows: `25`
- mutation-failure rows: `5`
- master rows written: `55`
- mutation-success export rows: `25`
- mutation-failure export rows: `5`

## Why The Current Loop Reverts

The latest logged loop does not fail because the idea of mutation is wrong. It
fails because the generated candidate does not preserve the runtime contract of
the shipped genome.

The fixed judge never even gets to the full assertion suite after mutation. The
candidate first collapses at `_run_and_evaluate()` with `can_run_genome: 'date'`.
That turns the round into a hard revert instead of an incremental score test.
