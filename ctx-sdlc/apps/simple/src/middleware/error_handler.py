"""Centralized error handling."""

from flask import Flask, jsonify


def register_error_handlers(app: Flask) -> None:
    """Register custom error handlers."""

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": str(e.description)}), 400

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": str(e.description)}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error."}), 500
