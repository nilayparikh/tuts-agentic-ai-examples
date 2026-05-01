"""Project status helpers for the learner-facing CleanLoop CLI."""

from __future__ import annotations

import json
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
    shipped_inputs = cleanloop_datasets.get_shipped_input_paths(target_input_dir)
    challenge_inputs = cleanloop_datasets.get_challenge_input_paths(target_input_dir)
    manifest_path = cleanloop_datasets.get_challenge_manifest_path(util.OUTPUT_DIR)
    challenge_manifest: dict[str, object] = {}
    if manifest_path.exists():
        challenge_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    return {
        "dataset": config.name,
        "model": model,
        "python": util.sys.version.split()[0],
        "env_exists": util.ENV_FILE.exists(),
        "output_exists": util.OUTPUT_DIR.exists(),
        "challenge_manifest_exists": manifest_path.exists(),
        "challenge_manifest": challenge_manifest,
        "input_rows": {path.name: _count_rows(path) for path in shipped_inputs},
        "challenge_input_rows": {
            path.name: _count_rows(path) for path in challenge_inputs
        },
    }
