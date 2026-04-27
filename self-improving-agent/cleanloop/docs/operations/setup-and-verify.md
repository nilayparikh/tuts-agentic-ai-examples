# Setup and Verify

This project is now self-sufficient inside `cleanloop/`.

## Environment Files

CleanLoop already ships these local files.

- `.env.example`
- `.env`

The runtime loads `cleanloop/.env` first, then falls back to the parent example `.env` only if needed.

## Standalone Project

Install from inside `cleanloop/`:

```bash
pip install -e .
cleanloop verify
```

Direct local alternative:

```bash
python util.py verify
```

## What Verify Confirms

- Python 3.11+
- required packages
- endpoint and API key resolution
- one live LLM completion

## Inline Coding Anchor

Lesson 01 keeps the verify entrypoint narrow on purpose.

```python
from cleanloop import verify


def main() -> None:
    verify.main()
```

That is enough to keep the command surface stable while the code behind it becomes more modular.
