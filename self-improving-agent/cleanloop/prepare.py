"""prepare.py — The Referee (immutable).

Evaluates the genome's output against binary assertions.
This file is LOCKED — the agent must never modify it.

Lesson references:
  - Lesson 03: Lines 25-70   (assertion functions — the arena pattern)
  - Lesson 06: Lines 72-110  (evaluate entrypoint — called by loop.py)
  - Lesson 08: Lines 112-140 (result formatting — eval-driven development)

Usage:
    python -m cleanloop.prepare                  # standalone eval
    python -m cleanloop.prepare cleanloop/.output/finance_master.csv
"""

import sys
from collections import Counter
from pathlib import Path

import pandas as pd

from cleanloop import datasets as cleanloop_datasets

# ─── PATHS ────────────────────────────────────────────────────────────
INPUT_DIR = Path(__file__).parent / ".input"
GOLD_DIR = Path(__file__).parent / ".gold"
OUTPUT_DIR = Path(__file__).resolve().parent / ".output"
DEFAULT_DATASET = cleanloop_datasets.get_dataset_config()
OUTPUT_PATH = cleanloop_datasets.get_output_path(OUTPUT_DIR)


# =====================================================================
# SECTION: Binary Assertions
# Lesson 03 — Each assertion is a pure function: data in, bool out.
# The referee defines WHAT is correct. The genome defines HOW to get there.
# Key principle: assertions are unambiguous, machine-verifiable, and
# ungameable. A soft metric like "data quality score" would let the
# agent optimize for the metric instead of actual correctness.
# =====================================================================

def assert_has_required_columns(
    df: pd.DataFrame,
    required_columns: tuple[str, ...],
) -> tuple[bool, str]:
    """Check that all required columns exist in the output."""
    required = set(required_columns)
    actual = set(df.columns)
    missing = required - actual
    if missing:
        return False, f"missing columns: {missing}"
    return True, "all columns present"


def assert_numeric_column(df: pd.DataFrame, column: str) -> tuple[bool, str]:
    """Check that a column contains only numeric values."""
    if column not in df.columns:
        return False, f"{column} column missing"
    coerced = pd.to_numeric(df[column], errors="coerce")
    if coerced.notna().all():
        return True, f"{column} is numeric"
    invalid_count = int(coerced.isna().sum())
    return False, f"{invalid_count} non-numeric or missing values in {column}"


def assert_datetime_column(df: pd.DataFrame, column: str) -> tuple[bool, str]:
    """Check that every value in a datetime column can be parsed."""
    if column not in df.columns:
        return False, f"{column} column missing"
    try:
        pd.to_datetime(df[column], format="mixed", dayfirst=True)
        return True, f"all {column} values parseable"
    except Exception as exc:
        return False, f"parse error: {exc}"


def assert_no_nan(df: pd.DataFrame, col: str) -> tuple[bool, str]:
    """Check that a column has zero NaN values."""
    if col not in df.columns:
        return False, f"{col} column missing"
    nan_count = int(df[col].isna().sum())
    if nan_count == 0:
        return True, f"zero NaN in {col}"
    return False, f"{nan_count} NaN values in {col}"


def assert_matches_reference(metrics: dict[str, float | int]) -> tuple[bool, str]:
    """Check that the output exactly matches the canonical reference rows."""
    missing_rows = int(metrics.get("missing_rows", 0))
    unexpected_rows = int(metrics.get("unexpected_rows", 0))
    reference_rows = int(metrics.get("reference_rows", 0))
    output_rows = int(metrics.get("output_rows", 0))
    matched_rows = int(metrics.get("matched_rows", 0))

    if missing_rows == 0 and unexpected_rows == 0 and output_rows == reference_rows:
        return True, f"matched all {matched_rows} reference rows"

    return False, (
        f"matched={matched_rows}, missing={missing_rows}, unexpected={unexpected_rows}, "
        f"output_rows={output_rows}, reference_rows={reference_rows}"
    )


def _get_dataset_for_output(master_csv: Path):
    """Resolve the active dataset config from the output file path."""
    dataset_name = cleanloop_datasets.detect_dataset_from_output_path(master_csv)
    return cleanloop_datasets.get_dataset_config(dataset_name)


def _load_reference_df() -> pd.DataFrame:
    """Load the canonical cleaned finance output."""
    reference_path = cleanloop_datasets.get_reference_path(GOLD_DIR)
    return pd.read_csv(reference_path)


def _row_counter(df: pd.DataFrame, required_columns: tuple[str, ...]) -> Counter:
    """Build a multiset of normalized row tuples for reference comparison."""
    comparable = df.loc[:, list(required_columns)].fillna("").astype(str)
    return Counter(tuple(row) for row in comparable.itertuples(index=False, name=None))


def _build_reference_metrics(
    df: pd.DataFrame,
    reference_df: pd.DataFrame,
    required_columns: tuple[str, ...],
) -> dict[str, float | int]:
    """Compute row-level match metrics against the canonical reference output."""
    output_counter = _row_counter(df, required_columns)
    reference_counter = _row_counter(reference_df, required_columns)
    matched_rows = sum((output_counter & reference_counter).values())
    missing_rows = sum((reference_counter - output_counter).values())
    unexpected_rows = sum((output_counter - reference_counter).values())
    reference_rows = len(reference_df)
    output_rows = len(df)
    cleanliness_score = matched_rows / reference_rows if reference_rows else 1.0
    output_precision = matched_rows / output_rows if output_rows else 0.0

    return {
        "reference_rows": reference_rows,
        "output_rows": output_rows,
        "matched_rows": matched_rows,
        "missing_rows": missing_rows,
        "unexpected_rows": unexpected_rows,
        "cleanliness_score": round(cleanliness_score, 6),
        "output_precision": round(output_precision, 6),
    }


def _build_checks(df: pd.DataFrame, metrics: dict[str, float | int]):
    """Build the finance-only assertion checks for one output DataFrame."""
    config = cleanloop_datasets.get_dataset_config()
    checks = [
        (
            "has_required_columns",
            lambda d: assert_has_required_columns(d, config.required_columns),
            df,
        )
    ]
    checks.extend(
        [
            ("value_is_numeric", lambda d: assert_numeric_column(d, "value"), df),
            ("date_is_parseable", lambda d: assert_datetime_column(d, "date"), df),
            ("no_nan_date", lambda d: assert_no_nan(d, "date"), df),
            ("no_nan_entity", lambda d: assert_no_nan(d, "entity"), df),
            ("no_nan_value", lambda d: assert_no_nan(d, "value"), df),
        ]
    )

    checks.append(
        (
            "matches_reference_output",
            lambda _: assert_matches_reference(metrics),
            df,
        )
    )
    return checks


# =====================================================================
# SECTION: Evaluation Entrypoint
# Lesson 06 — loop.py calls this function every iteration.
# It reads the genome's output CSV and runs every assertion.
# Returns a structured result dict that the loop uses for:
#   1. Deciding commit vs. revert
#   2. Building the next LLM prompt with failure details
#   3. Logging to dataset-specific history files for the dashboard
# =====================================================================

def evaluate(master_csv: Path) -> dict:
    """Run all binary assertions against the output CSV.

    Returns dict with 'passed' and 'failed' lists, plus 'score'.
    """
    results: dict[str, object] = {"passed": [], "failed": [], "metrics": {}}

    # Gate check: can we even read the file?
    try:
        df = pd.read_csv(master_csv)
    except Exception as exc:
        results["failed"].append(f"can_read_output: {exc}")
        return {**results, "score": 0, "total": 1}

    results["passed"].append("can_read_output")
    _get_dataset_for_output(master_csv)

    try:
        reference_df = _load_reference_df()
    except Exception as exc:
        results["failed"].append(f"can_load_reference: {exc}")
        return {**results, "score": len(results["passed"]), "total": len(results["passed"]) + len(results["failed"])}

    metrics = _build_reference_metrics(df, reference_df, DEFAULT_DATASET.required_columns)
    results["metrics"] = metrics

    # Run each assertion
    checks = _build_checks(df, metrics)

    for name, fn, data in checks:
        passed, detail = fn(data)
        if passed:
            results["passed"].append(f"{name}: {detail}")
        else:
            results["failed"].append(f"{name}: {detail}")

    total = len(results["passed"]) + len(results["failed"])
    results["score"] = len(results["passed"])
    results["total"] = total
    return results


# =====================================================================
# SECTION: Result Formatting
# Lesson 08 — Eval-driven development: how to read and interpret
# assertion results. This output format is designed for both
# human reading (terminal) and machine consumption (JSON).
# =====================================================================

def print_results(results: dict) -> None:
    """Print evaluation results in a human-readable format."""
    score = results.get("score", 0)
    total = results.get("total", 0)

    print(f"\n{'='*50}")
    print(f"  CleanLoop Evaluation: {score}/{total}")
    print(f"{'='*50}")

    if results["passed"]:
        print("\n  PASSED:")
        for item in results["passed"]:
            print(f"    [PASS] {item}")

    if results["failed"]:
        print("\n  FAILED:")
        for item in results["failed"]:
            print(f"    [FAIL] {item}")

    print()


# =====================================================================
# SECTION: Standalone Runner
# Run prepare.py directly to evaluate without the loop.
# =====================================================================

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else OUTPUT_PATH

    if not target.exists():
        # No output yet — run the genome to create one
        OUTPUT_DIR.mkdir(exist_ok=True)
        sys.path.insert(0, str(Path(__file__).parent))
        from cleanloop import clean_data  # pylint: disable=import-outside-toplevel
        clean_data.clean(INPUT_DIR, OUTPUT_PATH)
        print(f"Ran genome. Output: {OUTPUT_PATH}")

    result = evaluate(target)
    print_results(result)

    # Save results for dashboard consumption
