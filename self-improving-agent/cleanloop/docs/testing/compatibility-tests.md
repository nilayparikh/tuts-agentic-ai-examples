# Compatibility Tests

Compatibility coverage protects the learner-facing surface while the code is being split into lesson modules.

## What This Suite Guards

- local CLI commands
- verify behavior
- reference output evaluation
- reset semantics
- dataset resolution
- loop-side regressions already fixed in this example

## Run Commands

```bash
python -m unittest tests.test_python_compat
python -m unittest tests.test_python_compat tests.test_cleanloop_exports
```
