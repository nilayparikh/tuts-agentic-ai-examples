"""Task service — business logic for task operations."""

import uuid
from datetime import datetime, timezone

from ..db.connection import get_db
from ..models.types import VALID_TRANSITIONS, TaskStatus


def get_all_tasks() -> list[dict]:
    """Return all tasks."""
    db = get_db()
    rows = db.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    return [dict(r) for r in rows]


def get_task(task_id: str) -> dict | None:
    """Return a single task or None."""
    db = get_db()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row) if row else None


def create_task(
    title: str,
    created_by: str,
    description: str | None = None,
    priority: str = "medium",
    assigned_to: str | None = None,
) -> dict:
    """Create a new task in 'todo' status."""
    db = get_db()
    task_id = f"t-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()

    db.execute(
        """INSERT INTO tasks (id, title, description, status, priority, assigned_to, created_by, created_at, updated_at)
           VALUES (?, ?, ?, 'todo', ?, ?, ?, ?, ?)""",
        (task_id, title, description, priority, assigned_to, created_by, now, now),
    )
    db.commit()
    return get_task(task_id)  # type: ignore[return-value]


def transition_task(task_id: str, new_status: TaskStatus) -> dict:
    """Transition a task to a new status, enforcing the workflow."""
    task = get_task(task_id)
    if not task:
        raise ValueError(f"Task '{task_id}' not found.")

    current: TaskStatus = task["status"]
    allowed = VALID_TRANSITIONS.get(current, [])

    if new_status not in allowed:
        raise ValueError(
            f"Cannot transition from '{current}' to '{new_status}'. "
            f"Allowed: {allowed}"
        )

    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
        (new_status, now, task_id),
    )
    db.commit()
    return get_task(task_id)  # type: ignore[return-value]
