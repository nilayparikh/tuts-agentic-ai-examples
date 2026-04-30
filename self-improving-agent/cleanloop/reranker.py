"""reranker.py — Best-of-N Test-Time Self-Improvement.

Generates multiple candidate code fixes, evaluates each against the
assertion suite, and selects the best one. This is the "System 2"
upgrade to the standard single-shot proposal in loop.py.

Course alignment:
    - Lesson 06: test-time search and reranking

Usage:
    Preferred from cleanloop/:
        python util.py loop --rerank
        python util.py loop --rerank --candidates 5

    Direct module alternative:
        python -m cleanloop.reranker
        python -m cleanloop.reranker --candidates 5

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

import argparse
import importlib.util
import sys
import tempfile
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import autogen_runtime, util  # noqa: E402
from cleanloop import datasets as cleanloop_datasets  # noqa: E402

util.load_env()

GENOME_PATH = PROJECT_ROOT / "cleanloop" / "clean_data.py"
INPUT_DIR = PROJECT_ROOT / "cleanloop" / ".input"


def _expected_total_assertions() -> int:
    """Return the current finance referee assertion count."""
    return len(cleanloop_datasets.build_assertion_registry()) + 1


# =====================================================================
# SECTION: Best-of-N Candidate Proposal
# Lesson 06 — Generate N candidate fixes with increasing temperature.
# Low temperature (0.3) gives conservative fixes. High temperature
# (0.9) gives creative but risky rewrites. The diversity helps us
# explore the solution space more broadly.
#
# This function is called by loop.py when --use-reranker is set.
# It replaces the standard single-shot _propose_fix.
# =====================================================================


def propose(
    client: Any,
    model: str,
    genome_code: str,
    failed_assertions: list[str],
    n_candidates: int = 3,
    *,
    timeout_seconds: int | None = None,
) -> tuple[str | None, str, dict[str, object]]:
    """Generate N candidates and return the best (code, hypothesis).

    Called by loop.py as a drop-in replacement for _propose_fix.
    """
    config = cleanloop_datasets.get_dataset_config()
    agenda = cleanloop_datasets.build_program_text(config.name)
    failed_text = "\n".join(f"  - {f}" for f in failed_assertions)

    system = (
        "You are a self-improving data engineer agent.\n"
        f"## Selected Dataset\n{config.label} (`{config.name}`)\n\n"
        f"## Agenda\n{agenda}\n\n"
        "Return ONLY the complete clean_data.py in a ```python block.\n"
        "Before the code, write a ONE-LINE hypothesis."
    )
    user = (
        f"## Current Code\n```python\n{genome_code}\n```\n\n"
        f"## Failed Assertions\n{failed_text}\n\n"
        "Fix the code so all assertions pass."
    )

    print(f"  Reranker: generating {n_candidates} candidates...")
    return autogen_runtime.propose_reranked_mutation(
        client,
        model,
        system,
        user,
        n_candidates=n_candidates,
        evaluate_candidate=_evaluate_candidate,
        timeout_seconds=timeout_seconds,
    )


# =====================================================================
# SECTION: Isolated Candidate Evaluation
# Lesson 06 — Each candidate is evaluated in a temp directory so
# it can't corrupt the real genome. We dynamically load the candidate
# module, run it against the real input data, and evaluate with the
# real referee. This is the "judge" in generate-then-judge.
# =====================================================================


def _evaluate_candidate(candidate_code: str) -> tuple[int, int]:
    """Evaluate a candidate genome in an isolated temp directory."""
    config = cleanloop_datasets.get_dataset_config()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Write candidate genome
        genome_file = tmp / "clean_data.py"
        genome_file.write_text(candidate_code, encoding="utf-8")
        output_file = tmp / config.output_filename

        # Load and run the candidate in isolation
        try:
            spec = importlib.util.spec_from_file_location(
                "candidate_genome",
                genome_file,
            )
            if spec is None or spec.loader is None:
                return 0, _expected_total_assertions()
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.clean(INPUT_DIR, output_file)
        except Exception:  # pylint: disable=broad-exception-caught
            return 0, _expected_total_assertions()

        # Evaluate with the real referee
        sys.path.insert(0, str(PROJECT_ROOT / "cleanloop"))
        try:
            from cleanloop import prepare

            results = prepare.evaluate(output_file)
            return results["score"], results["total"]
        finally:
            if str(PROJECT_ROOT / "cleanloop") in sys.path:
                sys.path.remove(str(PROJECT_ROOT / "cleanloop"))


def _extract_code(text: str) -> str | None:
    """Extract Python code block from LLM response."""
    if "```python" not in text:
        return None
    start = text.index("```python") + len("```python")
    end = text.index("```", start)
    return text[start:end].strip()


def _extract_hypothesis(text: str) -> str:
    """Extract hypothesis line before the code block."""
    parts = text.split("```python")
    if len(parts) < 2:
        return "no hypothesis"
    lines = parts[0].strip().split("\n")
    for line in reversed(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped[:120]
    return "no hypothesis"


# =====================================================================
# SECTION: Standalone Demo
# Run reranking independently so you can inspect baseline failures,
# candidate generation, and the selected survivor without running the
# full mutation loop.
# =====================================================================


def main() -> None:
    """Run Best-of-N reranking as a standalone demo."""  # pylint: disable=too-many-locals
    parser = argparse.ArgumentParser(
        description="Reranker — Best-of-N candidate selection"
    )
    parser.add_argument(
        "--candidates",
        type=int,
        default=3,
        help="Number of candidates (default: 3)",
    )
    args = parser.parse_args()

    llm_config = util.resolve_llm_env()
    client = util.build_llm_client(
        llm_config["endpoint"],
        llm_config["api_key"],
        llm_config["api_version"],
    )
    model = llm_config["model"]

    genome_code = GENOME_PATH.read_text(encoding="utf-8")

    # Get current failures
    from cleanloop import prepare, clean_data

    importlib.reload(clean_data)
    output_dir = PROJECT_ROOT / "cleanloop" / ".output"
    output_dir.mkdir(exist_ok=True)
    config = cleanloop_datasets.get_dataset_config()
    output = output_dir / config.output_filename
    clean_data.clean(INPUT_DIR, output)
    results = prepare.evaluate(output)

    print(f"Baseline: {results['score']}/{results['total']}")
    code, hyp, diagnostics = propose(
        client,
        model,
        genome_code,
        results["failed"],
        args.candidates,
    )

    if code:
        out = PROJECT_ROOT / "output" / "best_candidate.py"
        out.write_text(code, encoding="utf-8")
        print(f"\nBest candidate saved to {out}")
        print(f"Hypothesis: {hyp}")
        print(f"Selected attempt: {diagnostics['selected_attempt']}")
    else:
        print("No candidate improved over baseline.")


if __name__ == "__main__":
    main()
