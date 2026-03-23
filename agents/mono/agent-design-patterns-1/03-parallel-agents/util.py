"""Process manager for the parallel agents example.

Usage:
    python util.py --start   Start all agent servers (background)
    python util.py --stop    Stop all agent processes

Ports: 11301 (Museum), 11302 (Concert), 11303 (Restaurant),
       11304 (Synthesizer), 11305 (Orchestrator)
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PID_FILE = SCRIPT_DIR / ".pids.json"

# Start finders first, then synthesizer, then orchestrator
AGENTS = [
    {"name": "MuseumFinderAgent", "script": "museum_finder_server.py", "port": 11301},
    {"name": "ConcertFinderAgent", "script": "concert_finder_server.py", "port": 11302},
    {"name": "RestaurantFinderAgent", "script": "restaurant_finder_server.py", "port": 11303},
    {"name": "SynthesizerAgent", "script": "synthesizer_server.py", "port": 11304},
    {"name": "ParallelOrchestrator", "script": "orchestrator_server.py", "port": 11305},
]


def _find_python() -> str:
    """Return the path to the venv python executable."""
    venv_candidates = [SCRIPT_DIR.parent / ".venv", SCRIPT_DIR.parents[2] / ".venv"]
    for venv in venv_candidates:
        if sys.platform == "win32":
            python = venv / "Scripts" / "python.exe"
        else:
            python = venv / "bin" / "python"
        if python.exists():
            return str(python)
    return sys.executable


def _wait_for_port(port: int, timeout: float = 15.0) -> bool:
    """Wait until a port is accepting connections."""
    import socket

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1.0):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def start() -> int:
    """Start all agent servers as background processes."""
    python = _find_python()
    pids = {}
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    print("=" * 60)
    print("  Parallel Agents Pattern - Starting servers")
    print("=" * 60)

    for agent in AGENTS:
        script = SCRIPT_DIR / agent["script"]
        if not script.exists():
            print(f"ERROR: {script} not found")
            return 1

        print(f"  Starting {agent['name']} on port {agent['port']}...")
        proc = subprocess.Popen(
            [python, str(script)],
            cwd=str(SCRIPT_DIR),
            env=env,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
        )
        pids[agent["name"]] = proc.pid
        print(f"    PID: {proc.pid}")

    # Wait for all ports
    all_ready = True
    for agent in AGENTS:
        if _wait_for_port(agent["port"]):
            print(f"  {agent['name']} ready on port {agent['port']}")
        else:
            print(f"  WARNING: {agent['name']} not responding on port {agent['port']}")
            all_ready = False

    PID_FILE.write_text(json.dumps(pids), encoding="utf-8")

    print("-" * 60)
    if all_ready:
        print("  All 5 agents started successfully.")
        print("  Server logs stream in this terminal while the agents run.")
        print("  Finders: Museum(11301) Concert(11302) Restaurant(11303)")
        print("  Synthesizer: 11304  |  Orchestrator: 11305")
        print("  Run 'python client.py' to test.")
        print("  Run 'python util.py --stop' to stop.")
    else:
        print("  WARNING: Some agents failed to start.")
    print("=" * 60)
    return 0


def stop() -> int:
    """Stop all agent processes."""
    print("=" * 60)
    print("  Parallel Agents Pattern - Stopping servers")
    print("=" * 60)

    if not PID_FILE.exists():
        print("  No PID file found. Nothing to stop.")
        print("=" * 60)
        return 0

    pids = json.loads(PID_FILE.read_text(encoding="utf-8"))

    for name, pid in pids.items():
        try:
            if sys.platform == "win32":
                os.kill(pid, signal.CTRL_BREAK_EVENT)
            else:
                os.kill(pid, signal.SIGTERM)
            print(f"  Stopped {name} (PID {pid})")
        except OSError:
            print(f"  {name} (PID {pid}) already stopped")

    PID_FILE.unlink(missing_ok=True)
    print("  All agents stopped.")
    print("=" * 60)
    return 0


def main() -> None:
    """Parse arguments and dispatch."""
    parser = argparse.ArgumentParser(description="Parallel Agents process manager")
    parser.add_argument("--start", action="store_true", help="Start agent servers")
    parser.add_argument("--stop", action="store_true", help="Stop agent servers")
    args = parser.parse_args()

    if args.start:
        sys.exit(start())
    elif args.stop:
        sys.exit(stop())
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
