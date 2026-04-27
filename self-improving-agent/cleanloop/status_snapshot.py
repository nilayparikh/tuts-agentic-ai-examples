"""Project status helpers for the learner-facing CleanLoop CLI."""

from __future__ import annotations

from pathlib import Path

from cleanloop import datasets as cleanloop_datasets
from cleanloop import util


def _count_rows(path: Path) -> int:
    """Return the number of non-header rows in one UTF-8 CSV file."""
    return max(len(path.read_text(encoding="utf-8").strip().splitlines()) - 1, 0)


def build_status_snapshot(input_dir: Path | None = None) -> dict[str, object]:
    """Capture the dataset and environment facts shown by `python util.py status`."""
    util.load_env()
    target_input_dir = input_dir or util.INPUT_DIR
    config = cleanloop_datasets.get_dataset_config()
    model = (
        util.os.getenv("MODEL_NAME")
        or util.os.getenv("AZURE_OPENAI_DEPLOY_NAME")
        or util.DEFAULT_MODEL
    )
    return {
        "dataset": config.name,
        "model": model,
        "python": util.sys.version.split()[0],
        "env_exists": util.ENV_FILE.exists(),
        "output_exists": util.OUTPUT_DIR.exists(),
        "input_rows": {
            path.name: _count_rows(path)
            for path in cleanloop_datasets.get_input_paths(target_input_dir)
        },
    }
