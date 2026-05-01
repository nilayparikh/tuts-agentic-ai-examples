"""challenger.py — Adversarial Data Generator (Challenger Agent).

Uses an LLM to generate progressively harder messy CSV files that
target the genome's known weaknesses. This creates an auto-curriculum:
as the cleaner improves, the challenger makes harder data.

Course alignment:
    - Lesson 05: self-challenging loop extension

Usage:
    Preferred from cleanloop/:
        python util.py challenge
        python util.py challenge --difficulty 3 --count 4
        python util.py challenge --levels 1 2 3

    Direct module alternative:
        python -m cleanloop.challenger
        python -m cleanloop.challenger --difficulty 3 --count 4
        python -m cleanloop.challenger --levels 1 2 3

Environment variables (from .env):
    LLM_ENDPOINT    — Agnostic OpenAI-compatible endpoint
    LLM_API_KEY     — Agnostic API key
    MODEL_NAME      — Model deployment or model name
    LLM_API_VERSION — Optional provider-specific API version
    OPENAI_BASE_URL — Legacy fallback
    OPENAI_API_KEY  — Legacy fallback
    AZURE_ENDPOINT  — Legacy fallback
    AZURE_API_KEY   — Legacy fallback
"""

# pylint: disable=duplicate-code

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import util  # noqa: E402
from cleanloop import datasets as cleanloop_datasets  # noqa: E402

util.load_env()

INPUT_DIR = PROJECT_ROOT / "cleanloop" / ".input"
OUTPUT_DIR = PROJECT_ROOT / "cleanloop" / ".output"
FINANCE_CHALLENGE_COLUMNS = (
    "invoice_id",
    "customer",
    "issued",
    "amount",
    "currency",
    "status",
    "adjusted_amount",
    "approval_flag",
    "resolution_amount",
    "resolution_flag",
)

SYSTEM_PROMPT = """\
You are an adversarial finance data quality tester. Generate messy invoice CSV
files for the CleanLoop finance arena. Each CSV must use exactly these columns:
invoice_id, customer, issued, amount, currency, status, adjusted_amount,
approval_flag, resolution_amount, resolution_flag.

Rules:
- Output ONLY the raw CSV content. No explanation, no markdown fences.
- Each file: 3-6 invoice rows plus the header.
- Use realistic finance messiness appropriate to the difficulty level.
- Keep invoice_id values unique and non-empty.
"""


# =====================================================================
# SECTION: Difficulty Ladder
# Lesson 05 — Five levels of adversarial data generation.
# Level 1 is mild (currency symbols). Level 5 is nightmare
# (BOM chars, embedded newlines, scientific notation).
# The auto-curriculum ratchets up difficulty as the genome improves.
# =====================================================================

DIFFICULTY_LEVELS: dict[int, str] = {
    1: (
        "Mild finance messiness: currency symbols inside amount values, "
        "one blank amount with status cancelled or void, and normal ISO dates."
    ),
    2: (
        "Moderate finance messiness: mixed date formats, currency symbols and "
        "currency codes in amount values, extra whitespace, and one approved adjusted_amount."
    ),
    3: (
        "Hard finance messiness: disputed invoices, FREE TRIAL or COMPLIMENTARY "
        "amount tokens, resolution_amount fields, and mixed approval flags."
    ),
    4: (
        "Very hard finance messiness: negative reversals, FX HOLD rows, blank "
        "cancelled invoices, mixed date formats, and quoted customer names with commas."
    ),
    5: (
        "Nightmare finance messiness: all prior issues plus pending chargebacks, "
        "scientific notation amounts, null-like tokens, embedded notes in quoted fields, "
        "and rows that should remain unresolved with diagnostics."
    ),
}


# =====================================================================
# SECTION: Adversarial Generation
# Lesson 05 — The challenger asks the LLM to generate messy data
# at the specified difficulty level. Higher temperature (0.8) gives
# more diverse outputs. The code strips markdown fences in case the
# LLM wraps the output.
# =====================================================================


def generate_messy_csv(
    client: Any,
    difficulty: int,
) -> str:
    """Generate one adversarial CSV file at the given difficulty level."""
    difficulty = max(1, min(5, difficulty))

    content = util.create_text_completion(
        client,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=DIFFICULTY_LEVELS[difficulty],
        temperature=0.8,
        max_tokens=500,
    )

    # Strip markdown fences if the LLM added them
    if content.startswith("```"):
        lines = content.split("\n")
        lines = [ln for ln in lines if not ln.strip().startswith("```")]
        content = "\n".join(lines)

    return content


def _utc_now() -> str:
    """Return the current UTC timestamp for manifest artifacts."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def validate_finance_csv(content: str) -> dict[str, object]:
    """Validate that generated challenge content matches the finance arena shape."""
    errors: list[str] = []
    rows = list(csv.reader(content.splitlines()))
    if not rows:
        return {"valid": False, "row_count": 0, "errors": ["empty csv"]}

    header = [cell.strip() for cell in rows[0]]
    if tuple(header) != FINANCE_CHALLENGE_COLUMNS:
        errors.append("header does not match finance challenge contract")

    body = [row for row in rows[1:] if any(cell.strip() for cell in row)]
    if not body:
        errors.append("no invoice rows generated")
    for index, row in enumerate(body, start=2):
        if len(row) != len(FINANCE_CHALLENGE_COLUMNS):
            errors.append(f"row {index} has {len(row)} columns")
            continue
        if not row[0].strip():
            errors.append(f"row {index} has blank invoice_id")

    return {"valid": not errors, "row_count": len(body), "errors": errors}


def _write_challenge_manifest(records: list[dict[str, object]]) -> Path:
    """Persist the current active challenge-file manifest."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = cleanloop_datasets.get_challenge_manifest_path(OUTPUT_DIR)
    payload = {
        "generated_at": _utc_now(),
        "active_inputs": [
            path.name for path in cleanloop_datasets.get_input_paths(INPUT_DIR)
        ],
        "challenge_files": records,
    }
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return manifest_path


def _save_challenge_file(
    *,
    filename: str,
    level: int,
    content: str,
) -> dict[str, object]:
    """Validate and save one generated challenge file."""
    validation = validate_finance_csv(content)
    record: dict[str, object] = {
        "file": filename,
        "level": level,
        "valid": validation["valid"],
        "row_count": validation["row_count"],
        "errors": validation["errors"],
    }
    if validation["valid"]:
        path = INPUT_DIR / filename
        path.write_text(content.strip() + "\n", encoding="utf-8")
        record["path"] = str(path)
        print(f"  Created: {path.name} ({validation['row_count']} rows)")
        return record

    print(f"  Rejected: {filename}")
    for error in cast(list[str], validation["errors"]):
        print(f"    - {error}")
    return record


# =====================================================================
# SECTION: Batch Generation CLI
# Generate a batch of adversarial files and save them directly to input/ so the
# next loop run faces targeted pressure instead of repeating easy fixtures.
# =====================================================================


def main() -> None:
    """Generate adversarial CSV files and save to input/."""
    parser = argparse.ArgumentParser(
        description="Challenger — Adversarial CSV generator"
    )
    parser.add_argument(
        "--levels",
        type=int,
        nargs="+",
        help="Generate one adversarial CSV for each listed difficulty level",
    )
    parser.add_argument(
        "--difficulty",
        type=int,
        default=2,
        help="Difficulty 1-5 (default: 2)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=2,
        help="Number of files to generate (default: 2)",
    )
    args = parser.parse_args()

    llm_config = util.resolve_llm_env()
    client = util.build_llm_client(
        llm_config["endpoint"],
        llm_config["api_key"],
        llm_config["api_version"],
    )

    INPUT_DIR.mkdir(exist_ok=True)
    levels = [max(1, min(5, level)) for level in (args.levels or [args.difficulty])]
    records: list[dict[str, object]] = []

    if args.levels:
        print(f"Generating {len(levels)} adversarial CSVs across levels: {levels}")
        for level in levels:
            csv_content = generate_messy_csv(
                client,
                level,
            )
            filename = f"adversarial_d{level}_01.csv"
            records.append(
                _save_challenge_file(
                    filename=filename,
                    level=level,
                    content=csv_content,
                )
            )
    else:
        print(
            f"Generating {args.count} adversarial CSVs "
            f"at difficulty {args.difficulty}"
        )
        for i in range(1, args.count + 1):
            csv_content = generate_messy_csv(
                client,
                args.difficulty,
            )
            filename = f"adversarial_d{args.difficulty}_{i:02d}.csv"
            records.append(
                _save_challenge_file(
                    filename=filename,
                    level=args.difficulty,
                    content=csv_content,
                )
            )

    manifest_path = _write_challenge_manifest(records)
    print(f"\nManifest: {manifest_path}")
    print(
        "Done. Run `python util.py evaluate` or `python util.py loop` "
        "to test the wider arena."
    )


if __name__ == "__main__":
    main()
