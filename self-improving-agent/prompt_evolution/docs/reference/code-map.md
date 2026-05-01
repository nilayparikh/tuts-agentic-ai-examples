# Prompt Evolution Code Map

| File               | Job                                                           |
| ------------------ | ------------------------------------------------------------- |
| `config.py`        | Load contexts, preferences, scenarios, and selection profiles |
| `evaluator.py`     | Score replies against policy, context, and preference signals |
| `hermes_client.py` | Adapt Hermes `AIAgent` to a small text runner                 |
| `loop.py`          | Draft, score, mutate instructions, and persist outputs        |
| `tracing.py`       | Write JSONL and OTEL-shaped trace artifacts                   |
| `dashboard.py`     | Render session, scenario, trace, LLM, and diff views          |
| `README.md`        | Human-readable agenda and mutable instruction block           |

## Mutable Artifact

The mutable instruction block lives in `README.md` under `## Mutable
Instructions`. `loop.py` reads that fenced text block at run start. The loop
does not edit the README in place. It writes the best evolved instruction text
to `.output/best_instructions.md`.

That choice keeps the demo safe. You can run the loop many times without
silently changing the lesson source.
