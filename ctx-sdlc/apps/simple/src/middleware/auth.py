"""Authentication middleware — resolves user from x-user-id header."""

from flask import request, g, jsonify


# Paths that skip authentication
SKIP_AUTH = {"/health"}


def auth_middleware():
    """Before-request hook: authenticate via x-user-id header."""
    if request.path in SKIP_AUTH:
        return None

    user_id = request.headers.get("x-user-id")
    if not user_id:
        return jsonify({"error": "Missing x-user-id header."}), 401

    from ..db.connection import get_db
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return jsonify({"error": f"Unknown user '{user_id}'."}), 401

    g.current_user = dict(user)
    return None
