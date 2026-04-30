# Mutation Cases

The shipped playbook repairs known anomaly families without letting the model invent a new data pipeline every round.

## Contextual Recovery Cases

These tokens require local business metadata so the playbook can recover a real
numeric amount instead of writing a placeholder zero.

- `FREE TRIAL`
- `COMPLIMENTARY`
- `OFFSET`

Noisy variants are canonicalized first.

- `TRIAL FREE`
- `FREE-TRIAL`
- `OFFSET ZERO`

## Approved Adjusted Amount Cases

These rows read `adjusted_amount` when `approval_flag=approved`.

- `DISCOUNTED`
- `FX HOLD`
- `REVERSAL`

Representative row:

```csv
INV-502,Blue Yonder, discounted   ✅ ,USD,...,paid,discount,11890.00,approved
```

## Approved Resolution Amount Cases

These rows read `resolution_amount` when `resolution_flag=approved`.

- `FREE TRIAL`
- `COMPLIMENTARY`
- `OFFSET`
- `N/A`
- `PENDING`
- `TBD`
- `ERROR`
- `ERR`

Representative row:

```csv
INV-203,Initech Systems,TBD // validated,EUR,...,pending,...,30980.00,approved
```

## Lesson 02 Coding Focus

The canonicalization and repair logic now lives in the flat root helpers:

- [mutation_playbook.py#L106](../../mutation_playbook.py#L106)
- [mutation_playbook.py#L144](../../mutation_playbook.py#L144)
- [clean_data_runtime.py#L28](../../clean_data_runtime.py#L28)
