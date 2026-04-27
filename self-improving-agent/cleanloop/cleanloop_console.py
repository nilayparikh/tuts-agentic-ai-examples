"""Bootstrap-aware console entrypoints for the standalone CleanLoop project."""

from __future__ import annotations

import subprocess

from cleanloop import util as cleanloop_util


def _run_with_bootstrap(argv: list[str]) -> int:
    """Preserve the shared-example venv bootstrap used by util.py."""
    if cleanloop_util.should_bootstrap_to_venv(["cleanloop", *argv]):
        result = subprocess.run(
            [
                str(cleanloop_util.get_python_path().resolve()),
                str(cleanloop_util.EXAMPLE_ROOT / "util.py"),
                *argv,
            ],
            cwd=str(cleanloop_util.PROJECT_ROOT),
            check=False,
        )
        return int(result.returncode)
    return cleanloop_util.main(argv)


def verify_main() -> int:
    """Run the dedicated verify command through the local CLI bootstrap."""
    return _run_with_bootstrap(["verify"])


def challenge_main() -> int:
    """Run the dedicated challenge command through the local CLI bootstrap."""
    return _run_with_bootstrap(["challenge"])


def sandbox_main() -> int:
    """Run the dedicated sandbox command through the local CLI bootstrap."""
    return _run_with_bootstrap(["sandbox"])


def autonomy_main() -> int:
    """Run the dedicated autonomy command through the local CLI bootstrap."""
    return _run_with_bootstrap(["autonomy"])
