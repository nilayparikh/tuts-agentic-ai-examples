# Lesson 01 - Local Runner

## Learning Objectives

- Run Prompt Evolution Studio from its own folder.
- Confirm the local catalog loads.
- Understand how `.env` and `.venv` are resolved.

## Command

```powershell
cd prompt_evolution
python util.py scenarios
python util.py status
```

## Inputs

- `.data/context_packs.json`
- `.data/preference_axes.json`
- `.data/scenario_cases.json`
- `.env` or the shared parent `../.env`

## Outputs

The commands print the available scenarios and a local status snapshot. No LLM call is made.

```text
Scenarios:
- makerspace_missing_booking: Makerspace Missing Laser Booking
- coworking_guest_refund: Coworking Guest Booking Refund

Catalog:
  Contexts:        6
  Preference axes: 6
  Scenarios:       4
```

## Validation

This lesson validates command visibility. It checks that learners can run the project without starting from the parent example folder.

## Summary

The local `util.py` is the command surface for the project. It adds the parent package path, loads local settings first, and falls back to the shared parent `.env` and `.venv` when they exist.
