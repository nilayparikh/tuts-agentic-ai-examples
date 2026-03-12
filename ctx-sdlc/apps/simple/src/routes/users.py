"""User routes — read-only user listing."""

from flask import Blueprint, jsonify, abort

from ..db.connection import get_db

users_bp = Blueprint("users", __name__)


@users_bp.get("/")
def list_users():
    """GET /api/users — list all users."""
    db = get_db()
    rows = db.execute("SELECT id, name, email, role FROM users ORDER BY name").fetchall()
    return jsonify([dict(r) for r in rows])


@users_bp.get("/<user_id>")
def get_user(user_id: str):
    """GET /api/users/:id — get a single user."""
    db = get_db()
    row = db.execute("SELECT id, name, email, role FROM users WHERE id = ?", (user_id,)).fetchone()
    if not row:
        abort(404)
    return jsonify(dict(row))
