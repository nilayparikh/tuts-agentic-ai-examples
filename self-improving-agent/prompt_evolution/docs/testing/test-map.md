# Prompt Evolution Test Map

The focused unittest module is `tests/test_prompt_evolution.py` from the parent
example root.

Run it with:

```bash
python -m unittest tests.test_prompt_evolution
```

## Coverage Areas

| Area      | What The Tests Check                                                       |
| --------- | -------------------------------------------------------------------------- |
| Parser    | CLI accepts context, preferences, problems, and scenarios                  |
| Catalog   | Contexts, preferences, and scenario cases load from `.data/`               |
| Evaluator | Missing policies, forbidden promises, and preference mismatches score down |
| Feedback  | Explicit user feedback creates another mutation and draft round            |
| Tracing   | Loop runs write LLM, evaluator, session, diff, and trace artifacts         |
| Dashboard | Dashboard helpers work outside the repo root                               |

## Lint Targets

When changing Prompt Evolution code, run pylint and mypy against modified files:

```bash
pylint prompt_evolution/config.py prompt_evolution/loop.py \
  prompt_evolution/tracing.py prompt_evolution/dashboard.py
mypy prompt_evolution/config.py prompt_evolution/loop.py \
  prompt_evolution/tracing.py prompt_evolution/dashboard.py --ignore-missing-imports
```

The tests avoid live LLM calls. They use small fake Hermes runners so the loop
can be verified quickly and deterministically.
