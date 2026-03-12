"""Task routes — CRUD + status transitions."""

from flask import Blueprint, request, jsonify, g, abort

from ..services.task_service import get_all_tasks, get_task, create_task, transition_task

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.get("/")
def list_tasks():
    """GET /api/tasks — list all tasks."""
    return jsonify(get_all_tasks())


@tasks_bp.get("/<task_id>")
def get_single_task(task_id: str):
    """GET /api/tasks/:id — get a single task."""
    task = get_task(task_id)
    if not task:
        abort(404)
    return jsonify(task)


@tasks_bp.post("/")
def create_new_task():
    """POST /api/tasks — create a task.

    Viewers cannot create tasks.
    """
    user = g.current_user
    if user["role"] == "viewer":
        abort(403, description="Viewers cannot create tasks.")

    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        abort(400, description="'title' is required.")

    task = create_task(
        title=title,
        created_by=user["id"],
        description=data.get("description"),
        priority=data.get("priority", "medium"),
        assigned_to=data.get("assignedTo"),
    )
    return jsonify(task), 201


@tasks_bp.patch("/<task_id>/status")
def update_task_status(task_id: str):
    """PATCH /api/tasks/:id/status — transition task status.

    Only admin and members can transition.  Viewers are read-only.
    """
    user = g.current_user
    if user["role"] == "viewer":
        abort(403, description="Viewers cannot modify tasks.")

    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    if not new_status:
        abort(400, description="'status' is required.")

    try:
        task = transition_task(task_id, new_status)
        return jsonify(task)
    except ValueError as e:
        abort(400, description=str(e))
