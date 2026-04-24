"""challenger.py — Adversarial Data Generator (Challenger Agent).

Uses an LLM to generate progressively harder messy CSV files that
target the genome's known weaknesses. This creates an auto-curriculum:
as the cleaner improves, the challenger makes harder data.

Lesson references:
  - Lesson 09: Lines 25-55   (difficulty ladder — 5 levels of messiness)
  - Lesson 09: Lines 58-100  (generate function — LLM creates adversarial data)
  - Lesson 09: Lines 103-140 (main — batch generation with difficulty ratchet)

Usage:
    python -m cleanloop.challenger
    python -m cleanloop.challenger --difficulty 3 --count 4

Environment variables (from .env):
    AZURE_ENDPOINT  — Azure AI Foundry or Foundry Local endpoint
    AZURE_API_KEY   — API key
    MODEL_NAME      — Model deployment name (default: gpt-4o)
"""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

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
# Lesson 09 — Five levels of adversarial data generation.
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
# Lesson 09 — The challenger asks the LLM to generate messy data
# at the specified difficulty level. Higher temperature (0.8) gives
# more diverse outputs. The code strips markdown fences in case the
# LLM wraps the output.
# =====================================================================

def generate_messy_csv(
    client: OpenAI,
    model: str,
    difficulty: int,
) -> str:
    """Generate one adversarial CSV file at the given difficulty level."""
    difficulty = max(1, min(5, difficulty))

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": DIFFICULTY_LEVELS[difficulty]},
        ],
        temperature=0.8,
        max_tokens=500,
    )
    content = (response.choices[0].message.content or "").strip()

    # Strip markdown fences if the LLM added them
    if content.startswith("```"):
        lines = content.split("\n")
        lines = [ln for ln in lines if not ln.strip().startswith("```")]
        content = "\n".join(lines)

    return content


# =====================================================================
# SECTION: Batch Generation CLI
# Lesson 09 — Generate a batch of adversarial files and save them
# directly to the input/ folder. Then re-run the loop to see if
# the genome can handle the new challenges.
# =====================================================================

def main() -> None:
    """Generate adversarial CSV files and save to input/."""
    parser = argparse.ArgumentParser(
        description="Challenger — Adversarial CSV generator"
    )
    parser.add_argument(
        "--difficulty", type=int, default=2,
        help="Difficulty 1-5 (default: 2)",
    )
    parser.add_argument(
        "--count", type=int, default=2,
        help="Number of files to generate (default: 2)",
    )
    args = parser.parse_args()

    client = OpenAI(
        base_url=os.environ["AZURE_ENDPOINT"],
        api_key=os.environ["AZURE_API_KEY"],
    )
    model = os.getenv("MODEL_NAME", "gpt-4o")

    print(
        f"Generating {args.count} adversarial CSVs "
        f"at difficulty {args.difficulty}"
    )

    INPUT_DIR.mkdir(exist_ok=True)
    for i in range(1, args.count + 1):
        csv_content = generate_messy_csv(client, model, args.difficulty)
        filename = f"adversarial_d{args.difficulty}_{i:02d}.csv"
        path = INPUT_DIR / filename
        path.write_text(csv_content, encoding="utf-8")
        print(f"  Created: {path.name}")

    print(
        f"\nDone. Run `python -m cleanloop.loop` "
        f"to test the genome against new data."
    )


if __name__ == "__main__":
    main()
