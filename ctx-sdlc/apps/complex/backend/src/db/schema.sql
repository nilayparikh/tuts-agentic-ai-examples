-- ---------------------------------------------------------------------------
-- Loan Workbench — Database Schema
-- ---------------------------------------------------------------------------
-- SQLite DDL for the Loan Workbench platform.
-- Run via: npm run db:seed (which executes seed.ts → creates tables + data)
--
-- IMPORTANT: When adding columns, create a new migration file in
-- db/migrations/ and update the seed.ts to apply it.  Never modify this
-- file directly for incremental changes — it represents the CURRENT schema.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
    id          TEXT PRIMARY KEY,
    role        TEXT NOT NULL CHECK (role IN ('underwriter', 'analyst-manager', 'compliance-reviewer')),
    name        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    phone       TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS loan_applications (
    id                    TEXT PRIMARY KEY,
    borrower_name         TEXT NOT NULL,
    amount                REAL NOT NULL CHECK (amount > 0),
    loan_state            TEXT NOT NULL,
    status                TEXT NOT NULL DEFAULT 'intake'
                          CHECK (status IN ('intake', 'review', 'underwriting', 'decision', 'finalized')),
    assigned_underwriter  TEXT NOT NULL REFERENCES users(id),
    risk_score            REAL,
    created_at            TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at            TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS decisions (
    id              TEXT PRIMARY KEY,
    application_id  TEXT NOT NULL REFERENCES loan_applications(id),
    type            TEXT NOT NULL CHECK (type IN ('approved', 'declined', 'conditional')),
    rationale       TEXT NOT NULL,
    decided_by      TEXT NOT NULL REFERENCES users(id),
    decided_at      TEXT NOT NULL DEFAULT (datetime('now')),
    conditions      TEXT  -- JSON array, nullable
);

CREATE TABLE IF NOT EXISTS notification_preferences (
    user_id     TEXT NOT NULL REFERENCES users(id),
    event       TEXT NOT NULL CHECK (event IN ('approval', 'decline', 'document-request', 'manual-review-escalation')),
    channel     TEXT NOT NULL CHECK (channel IN ('email', 'sms')),
    enabled     INTEGER NOT NULL DEFAULT 1,
    updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_by  TEXT NOT NULL,
    PRIMARY KEY (user_id, event, channel)
);

CREATE TABLE IF NOT EXISTS audit_entries (
    id              TEXT PRIMARY KEY,
    action          TEXT NOT NULL,
    actor           TEXT NOT NULL,
    delegated_for   TEXT,
    timestamp       TEXT NOT NULL DEFAULT (datetime('now')),
    previous_value  TEXT,  -- JSON
    new_value       TEXT,  -- JSON
    source          TEXT NOT NULL
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_applications_status ON loan_applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_underwriter ON loan_applications(assigned_underwriter);
CREATE INDEX IF NOT EXISTS idx_decisions_application ON decisions(application_id);
CREATE INDEX IF NOT EXISTS idx_preferences_user ON notification_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_entries(actor);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_entries(timestamp);
