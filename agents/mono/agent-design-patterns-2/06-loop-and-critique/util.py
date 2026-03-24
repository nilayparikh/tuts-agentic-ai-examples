"""Process manager for the Loop & Critique example.

Usage:
    python util.py --start   Start all agent servers (background)
    python util.py --stop    Stop all agent processes

Ports: 11401 (Generator), 11402 (Critic), 11403 (LoopOrchestrator)
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict
from typing import List

SCRIPT_DIR = Path(__file__).resolve().parent
PID_FILE = SCRIPT_DIR / ".pids.json"

AGENTS = [
    {"name": "GeneratorAgent", "script": "generator_server.py", "port": 11401},
    {"name": "CriticAgent", "script": "critic_server.py", "port": 11402},
    {"name": "LoopOrchestrator", "script": "loop_server.py", "port": 11403},
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


def _wait_for_port_to_close(port: int, timeout: float = 10.0) -> bool:
    """Wait until a port stops accepting connections."""
    import socket

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1.0):
                time.sleep(0.3)
        except OSError:
            return True
    return False


def _read_pid_file() -> Dict[str, int]:
    """Return tracked agent PIDs from disk if the file exists."""
    if not PID_FILE.exists():
        return {}
    return json.loads(PID_FILE.read_text(encoding="utf-8"))


def _find_listener_pids(port: int) -> List[int]:
    """Return process ids that are listening on the given TCP port."""
    if sys.platform == "win32":
        command = (
            "Get-NetTCPConnection -LocalPort "
            f"{port} -State Listen -ErrorAction SilentlyContinue | "
            "Select-Object -ExpandProperty OwningProcess"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            check=False,
            capture_output=True,
            text=True,
        )
        values = result.stdout.splitlines()
    else:
        result = subprocess.run(
            ["lsof", "-ti", f"tcp:{port}"],
            check=False,
            capture_output=True,
            text=True,
        )
        values = result.stdout.splitlines()

    pids: List[int] = []
    for value in values:
        stripped = value.strip()
        if stripped.isdigit():
            pids.append(int(stripped))
    return sorted(set(pids))


def _terminate_pid(pid: int, *, force: bool = False) -> None:
    """Stop a process by pid using a soft or forced termination mode."""
    if sys.platform == "win32":
        command = ["taskkill", "/PID", str(pid), "/T"]
        if force:
            command.append("/F")
        subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    else:
        os.kill(pid, signal.SIGKILL if force else signal.SIGTERM)


def _stop_pid_group(pids: Dict[str, int], heading: str) -> None:
    """Stop a set of named processes and print a consistent status block."""
    if not pids:
        return

    print(heading)
    for name, pid in pids.items():
        try:
            _terminate_pid(pid)
            print(f"  Stopped {name} (PID {pid})")
        except OSError:
            print(f"  {name} (PID {pid}) already stopped")


def _cleanup_existing_processes() -> bool:
    """Stop tracked or stale listeners before starting new agent processes."""
    print("  Preflight cleanup...")
    tracked_pids = _read_pid_file()
    if tracked_pids:
        _stop_pid_group(tracked_pids, "  Stopping tracked processes from PID file...")
        PID_FILE.unlink(missing_ok=True)

    all_clear = True
    for agent in AGENTS:
        port = agent["port"]
        listener_pids = [pid for pid in _find_listener_pids(port) if pid != os.getpid()]
        if not listener_pids:
            continue

        print(
            f"  Port {port} is already in use. Terminating listener(s): "
            f"{', '.join(str(pid) for pid in listener_pids)}"
        )
        for pid in listener_pids:
            try:
                _terminate_pid(pid)
            except OSError:
                continue

        if not _wait_for_port_to_close(port):
            remaining = [pid for pid in _find_listener_pids(port) if pid != os.getpid()]
            if remaining:
                print(
                    f"  Port {port} still busy after graceful shutdown. Forcing "
                    f"listener(s): {', '.join(str(pid) for pid in remaining)}"
                )
                for pid in remaining:
                    try:
                        _terminate_pid(pid, force=True)
                    except OSError:
                        continue

        if _wait_for_port_to_close(port):
            print(f"  Port {port} is clear.")
        else:
            print(f"  ERROR: Port {port} is still busy after preflight cleanup.")
            all_clear = False

    return all_clear


def start() -> int:
    """Start all agent servers as background processes."""
    python = _find_python()
    pids = {}
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    print("=" * 60)
    print("  Loop & Critique Pattern - Starting servers")
    print("=" * 60)

    if not _cleanup_existing_processes():
        print("  ERROR: Preflight cleanup failed. Resolve busy ports and retry.")
        print("=" * 60)
        return 1

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
        print("  All agents started successfully.")
        print("  Server logs stream in this terminal while the agents run.")
        print("  Run 'python client.py' to test.")
        print("  Run 'python util.py --stop' to stop.")
    else:
        print("  WARNING: Some agents failed to start.")
    print("=" * 60)
    return 0


def stop() -> int:
    """Stop all agent processes."""
    print("=" * 60)
    print("  Loop & Critique Pattern - Stopping servers")
    print("=" * 60)

    if not PID_FILE.exists():
        print("  No PID file found. Nothing to stop.")
        print("=" * 60)
        return 0

    _stop_pid_group(_read_pid_file(), "  Stopping tracked processes...")

    PID_FILE.unlink(missing_ok=True)
    print("  All agents stopped.")
    print("=" * 60)
    return 0


def main() -> None:
    """Parse arguments and dispatch."""
    parser = argparse.ArgumentParser(description="Loop & Critique process manager")
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
