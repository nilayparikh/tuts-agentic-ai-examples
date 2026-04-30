# Export Contract Tests

The export contract tests prove that the current finance fixture is teaching the intended anomaly model.

## Assertions That Matter Most

- master export uses canonical columns only
- mutation success rows keep required business fields populated
- unresolved failures preserve raw diagnostics
- the output counts remain `78 / 48 / 9`

## Representative Rows Used By Tests

- deterministic: `INV-101`
- mutation success: `INV-404`, `INV-502`, `INV-203`
- failures: `INV-112`, `INV-312`

## Run Command

```bash
python -m unittest tests.test_cleanloop_exports
```
