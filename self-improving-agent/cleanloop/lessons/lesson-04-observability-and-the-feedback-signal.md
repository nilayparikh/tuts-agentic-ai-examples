# Lesson 04 — Observability and the Feedback Signal

This lesson is about turning one mutation round into evidence. If you cannot explain why the loop committed or reverted a candidate, you do not have a reliable system. You have a black box that edits code.

## Command Path

Use the history written by a real loop run, then inspect it with the dashboard:

```bash
python util.py loop --max-iterations 1 --rerank --candidates 2
python util.py dashboard
```

The first command creates the round history. The second command is the operator surface that turns raw history into something readable.

## Captured Output

From the reranked loop run:

```text
[LLM_ATTEMPT] Attempt 1/2: AutoGen candidate 1: conservative
[TOKEN_USAGE] prompt=2897, completion=1004, total=None
[LLM_ATTEMPT] Attempt 2/2: AutoGen candidate 2: value-first
[TOKEN_USAGE] prompt=2895, completion=1059, total=None
[COMMIT_MUTATION] Committed improved mutation at 7/8

History saved to ...\cleanloop\.output\finance_eval_history.json
```

This is the important observability shift. The loop is not only recording the final score. It is recording how many attempts happened, which attempt won, and where the token budget went.

## Code References

1. [load_history in dashboard.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/dashboard.py#L62-L65)

   Important lines:

   ```python
   def load_history() -> list[dict]:
       if not HISTORY_PATH.exists():
           return []
       return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
   ```

   Impact: the dashboard starts from one durable artifact, not from hidden in-memory state. That keeps replay and inspection simple.

2. [\_blueprint_rows in dashboard.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/dashboard.py#L83-L107)

   Important lines:

   ```python
   rows.append(
       {
           "Round": entry.get("round"),
           "Action": entry.get("action", ""),
           "LLM Path": llm.get("selected_attempt", "none"),
           "Tokens": llm.get("total_tokens"),
           "Hypothesis": entry.get("hypothesis", ""),
       }
   )
   ```

   Impact: this compresses one whole round into an operator-facing table. It is the best one-screen summary of how the loop behaved.

3. [build_judge_metric_rows in dashboard_metrics.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/dashboard_metrics.py#L42-L81)

   Important lines:

   ```python
   rows.append(
       {
           "Before Recall %": round(before_recall, 2),
           "After Recall %": round(after_recall, 2),
           "Before Precision %": round(before_precision, 2),
           "After Precision %": round(after_precision, 2),
       }
   )
   ```

   Impact: these are the numbers that tell you whether the latest mutation improved quality or just changed row counts.

4. [build_log_rows in dashboard_metrics.py](https://github.com/nilayparikh/tuts-agentic-ai-examples/blob/main/self-improving-agent/cleanloop/dashboard_metrics.py#L132-L153)

   Important lines:

   ```python
   rows.append(
       {
           "Round": entry.get("round"),
           "Tag": log.get("tag"),
           "Message": log.get("message"),
           "Prompt Tokens": log.get("prompt_tokens"),
       }
   )
   ```

   Impact: this is the bridge between console logs and dashboard logs. It keeps both surfaces grounded in the same structured event stream.

## How The Pieces Connect

The loop writes a history JSON artifact. `dashboard.py` reads it. `dashboard_metrics.py` turns raw history into recall, precision, row-gap, and log tables. That is the full feedback signal.

## Hands-On Lab

Challenge:

Run one reranked round, then open the dashboard and answer three questions using only the saved artifacts: which attempt won, how many tokens were spent, and whether recall or precision moved more.

Success looks like this:

- You can name the winning attempt label.
- You can find the token totals.
- You can explain what the score change means operationally.
