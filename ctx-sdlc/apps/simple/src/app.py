"""Task Tracker — Flask application entry point.

A simple project management API with:
- Task CRUD operations
- User management with roles (admin, member, viewer)
- Task status workflow (todo → in-progress → review → done)
- SQLite persistence
- Basic authentication via x-user-id header
"""

from flask import Flask
from .db.connection import init_db
from .routes.tasks import tasks_bp
from .routes.users import users_bp
from .middleware.auth import auth_middleware
from .middleware.error_handler import register_error_handlers


def create_app(db_path: str = "data/task-tracker.db") -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path

    # Initialize database
    init_db(app)

    # Register middleware
    app.before_request(auth_middleware)

    # Register routes
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    # Register error handlers
    register_error_handlers(app)

    # Health check
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=3200, debug=True)
