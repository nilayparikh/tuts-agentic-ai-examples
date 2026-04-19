// ---------------------------------------------------------------------------
// Database Seed Script
// ---------------------------------------------------------------------------
// Populates the database with demo data for development and testing.
// The seed data exercises edge cases: California loans, delegated users,
// finalized applications, and users without saved preferences.
//
// Run: npm run db:seed
// ---------------------------------------------------------------------------

import { getDb, closeDb } from "./connection.js";

export function seedDatabase(): void {
  const db = getDb();

  const insertUser = db.prepare(
    `INSERT OR IGNORE INTO users (id, role, name, email, phone) VALUES (?, ?, ?, ?, ?)`,
  );

  const insertApp = db.prepare(
    `INSERT OR IGNORE INTO loan_applications (id, borrower_name, amount, loan_state, status, assigned_underwriter, risk_score, created_at, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
  );

  const insertPref = db.prepare(
    `INSERT OR IGNORE INTO notification_preferences (user_id, event, channel, enabled, updated_at, updated_by)
     VALUES (?, ?, ?, ?, ?, ?)`,
  );

  const insertDecision = db.prepare(
    `INSERT OR IGNORE INTO decisions (id, application_id, type, rationale, decided_by, decided_at, conditions)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
  );

  const insertAudit = db.prepare(
    `INSERT OR IGNORE INTO audit_entries (id, action, actor, delegated_for, timestamp, previous_value, new_value, source)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
  );

  const seedAll = db.transaction(() => {
    // ── Users ──
    insertUser.run(
      "u-1",
      "underwriter",
      "Dana Chu",
      "dana.chu@loanworkbench.local",
      "+15551234001",
    );
    insertUser.run(
      "u-2",
      "analyst-manager",
      "Raj Patel",
      "raj.patel@loanworkbench.local",
      "+15551234002",
    );
    insertUser.run(
      "u-3",
      "compliance-reviewer",
      "Kim Nakamura",
      "kim.nakamura@loanworkbench.local",
      null,
    );

    // ── Loan Applications ──
    const now = new Date().toISOString();
    insertApp.run(
      "app-1",
      "Acme Corp",
      500000,
      "CA",
      "underwriting",
      "u-1",
      72.5,
      now,
      now,
    );
    insertApp.run(
      "app-2",
      "Beta LLC",
      150000,
      "NY",
      "intake",
      "u-1",
      null,
      now,
      now,
    );
    insertApp.run(
      "app-3",
      "Gamma Inc",
      2000000,
      "CA",
      "decision",
      "u-2",
      85.0,
      now,
      now,
    );
    insertApp.run(
      "app-4",
      "Delta Co",
      75000,
      "TX",
      "finalized",
      "u-1",
      91.2,
      now,
      now,
    );

    // ── Notification Preferences ──
    insertPref.run("u-1", "approval", "email", 1, now, "u-1");
    insertPref.run("u-1", "approval", "sms", 1, now, "u-1");
    insertPref.run("u-1", "decline", "email", 1, now, "u-1");
    insertPref.run("u-2", "approval", "email", 1, now, "u-2");
    insertPref.run("u-2", "manual-review-escalation", "sms", 1, now, "u-2");
    // u-3 intentionally has NO preferences → tests default behavior

    // ── Decisions ──
    insertDecision.run(
      "dec-1",
      "app-3",
      "conditional",
      "High loan amount requires additional collateral verification.",
      "u-2",
      now,
      JSON.stringify(["Collateral appraisal", "Updated revenue statements"]),
    );
    insertDecision.run(
      "dec-2",
      "app-4",
      "approved",
      "Loan meets policy thresholds and required documentation is complete.",
      "u-2",
      now,
      null,
    );

    // ── Audit Trail ──
    insertAudit.run(
      "aud-1",
      "application.created",
      "u-1",
      null,
      now,
      null,
      JSON.stringify({ applicationId: "app-1", status: "underwriting" }),
      "seed-script",
    );
    insertAudit.run(
      "aud-2",
      "decision.recorded",
      "u-2",
      null,
      now,
      null,
      JSON.stringify({ applicationId: "app-4", type: "approved" }),
      "seed-script",
    );
  });

  seedAll();
  console.log("✓ Database seeded with demo data.");
}

// Run directly: tsx backend/src/db/seed.ts
if (process.argv[1]?.endsWith("seed.ts")) {
  seedDatabase();
  closeDb();
}
