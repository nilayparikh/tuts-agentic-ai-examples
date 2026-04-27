"""challenger.py — Adversarial Data Generator (Challenger Agent).

Uses an LLM to generate progressively harder messy CSV files that
target the genome's known weaknesses. This creates an auto-curriculum:
as the cleaner improves, the challenger makes harder data.

Course alignment:
    - Lesson 07: self-challenging loop extension

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
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import util

util.load_env()

INPUT_DIR = PROJECT_ROOT / "cleanloop" / ".input"

SYSTEM_PROMPT = """\
You are an adversarial data quality tester. Generate messy CSV files
with realistic data quality issues. Each CSV should have columns:
date, product, price, quantity — but with formatting problems.

Rules:
- Output ONLY the raw CSV content. No explanation, no markdown fences.
- Each file: 3-6 rows of data.
- Introduce realistic messiness appropriate to the difficulty level.
"""


# =====================================================================
# SECTION: Difficulty Ladder
# Lesson 07 — Five levels of adversarial data generation.
# Level 1 is mild (currency symbols). Level 5 is nightmare
# (BOM chars, embedded newlines, scientific notation).
# The auto-curriculum ratchets up difficulty as the genome improves.
# =====================================================================

DIFFICULTY_LEVELS: dict[int, str] = {
    1: (
        "Mild messiness: some currency symbols in price column "
        "($10.50, USD 22.00), one missing value."
    ),
    2: (
        "Moderate messiness: mixed date formats (ISO + European DD/MM), "
        "currency symbols AND codes, two missing values, extra whitespace."
    ),
    3: (
        "Hard messiness: NO header row, dates in three different formats, "
        "prices with text like 'free' or 'N/A', trailing commas, "
        "multiple missing values."
    ),
    4: (
        "Very hard: duplicate header rows mid-file, product names with "
        "commas (breaking naive CSV parsing), negative prices, dates as "
        "Unix timestamps, unicode currency symbols (EUR, GBP)."
    ),
    5: (
        "Nightmare: all of the above PLUS inconsistent row lengths, "
        "embedded newlines in quoted fields, mix of null representations "
        "('NULL', 'None', 'N/A', '', 'nan'), scientific notation for "
        "quantities (1e2 instead of 100), BOM character at file start."
    ),
}


# =====================================================================
# SECTION: Adversarial Generation
# Lesson 07 — The challenger asks the LLM to generate messy data
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

    if args.levels:
        print(f"Generating {len(levels)} adversarial CSVs across levels: {levels}")
        for level in levels:
            csv_content = generate_messy_csv(
                client,
                level,
            )
            filename = f"adversarial_d{level}_01.csv"
            path = INPUT_DIR / filename
            path.write_text(csv_content, encoding="utf-8")
            print(f"  Created: {path.name}")
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
            path = INPUT_DIR / filename
            path.write_text(csv_content, encoding="utf-8")
            print(f"  Created: {path.name}")

    print("\nDone. Run `python util.py loop` to test the genome against new data.")


if __name__ == "__main__":
    main()
