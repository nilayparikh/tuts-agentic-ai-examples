"""Database connection and schema initialization."""

import sqlite3
from pathlib import Path
from flask import Flask, g


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    role        TEXT NOT NULL CHECK (role IN ('admin', 'member', 'viewer')),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tasks (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    description     TEXT,
    status          TEXT NOT NULL DEFAULT 'todo'
                    CHECK (status IN ('todo', 'in-progress', 'review', 'done')),
    priority        TEXT NOT NULL DEFAULT 'medium'
                    CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    assigned_to     TEXT REFERENCES users(id),
    created_by      TEXT NOT NULL REFERENCES users(id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned ON tasks(assigned_to);
"""


def get_db() -> sqlite3.Connection:
    """Get the database connection for the current request."""
    if "db" not in g:
        from flask import current_app
        db_path = current_app.config["DB_PATH"]
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None) -> None:
    """Close the database connection at end of request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app: Flask) -> None:
    """Initialize schema and register teardown."""
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.executescript(SCHEMA)
        _seed_db(db)


def _seed_db(db: sqlite3.Connection) -> None:
    """Seed demo data if tables are empty."""
    count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        return

    db.executescript("""
        INSERT INTO users (id, name, email, role) VALUES
            ('u-1', 'Alice Chen', 'alice@tasktracker.local', 'admin'),
            ('u-2', 'Bob Smith', 'bob@tasktracker.local', 'member'),
            ('u-3', 'Carol Davis', 'carol@tasktracker.local', 'viewer');

        INSERT INTO tasks (id, title, description, status, priority, assigned_to, created_by) VALUES
            ('t-1', 'Set up CI pipeline', 'Configure GitHub Actions for automated testing', 'in-progress', 'high', 'u-2', 'u-1'),
            ('t-2', 'Write API documentation', 'Document all REST endpoints', 'todo', 'medium', 'u-2', 'u-1'),
            ('t-3', 'Fix login bug', 'Users get 500 on expired sessions', 'review', 'critical', 'u-1', 'u-2');
    """)
