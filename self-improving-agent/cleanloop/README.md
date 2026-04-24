# CleanLoop Agenda

[![Watch: AI That Improves Itself: The "Bounded Recipe" for Agents](https://img.youtube.com/vi/loYCwyRU_tM/maxresdefault.jpg)](https://www.youtube.com/watch?v=loYCwyRU_tM)

> <strong>Watch the video:</strong> <a href="https://www.youtube.com/watch?v=loYCwyRU_tM" target="_blank" rel="noopener noreferrer">AI That Improves Itself: The "Bounded Recipe" for Agents</a>
> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>

## Goal

Merge the five finance invoice CSVs into one normalized receivables table with
parseable dates and numeric values.

## Finance Arena

You are cleaning one progressive invoice arena, not choosing between datasets.

## Input Files

- finance_invoices.csv
- finance_invoices_flags.csv
- finance_invoices_regional.csv
- finance_invoices_collections.csv
- finance_invoices_adjustments.csv

## Required Output Columns

date, entity, value, category

## Requirements

1. Use only the five finance\_\*.csv inputs.
2. Normalize every file into date, entity, value, category.
3. Preserve good rows even when amount strings contain symbols, sentinels, or notes.
4. Handle mixed date formats without inventing or dropping records.
5. Match the canonical finance reference in cleanloop/.gold/finance_expected.csv.

## Constraints

- You may only modify the `clean` function in `clean_data.py`.
- Do not change function signatures or imports.
- Do not modify `cleanloop/prepare.py`, `cleanloop/datasets.py`, or this file.

## Series Navigation

| Lesson | Video                                                                                                   | Example Folder  |
| ------ | ------------------------------------------------------------------------------------------------------- | --------------- |
| 01     | [AI That Improves Itself: The "Bounded Recipe" for Agents](https://www.youtube.com/watch?v=loYCwyRU_tM) | [cleanloop](./) |
