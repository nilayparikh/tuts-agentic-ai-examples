import { useState } from "react";
import type { Decision, EscalatedApplication } from "../types";

interface Props {
  application: EscalatedApplication;
  onDecision: (id: string, decision: Decision, notes: string) => void;
}

const SEVERITY_COLORS: Record<string, string> = {
  hard: "#dc2626",
  soft: "#f59e0b",
};

const STATUS_STYLES: Record<string, { bg: string; color: string }> = {
  PENDING: { bg: "#fef3c7", color: "#92400e" },
  APPROVED: { bg: "#d1fae5", color: "#065f46" },
  DECLINED: { bg: "#fee2e2", color: "#991b1b" },
  INFO_REQUESTED: { bg: "#dbeafe", color: "#1e40af" },
};

export function ApplicationCard({ application, onDecision }: Props) {
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const status = STATUS_STYLES[application.status] ?? STATUS_STYLES.PENDING;

  const handleAction = async (decision: Decision) => {
    setSubmitting(true);
    try {
      await onDecision(application.id, decision, notes);
      setNotes("");
    } finally {
      setSubmitting(false);
    }
  };

  const riskColor =
    application.risk_score <= 40
      ? "#16a34a"
      : application.risk_score <= 80
        ? "#f59e0b"
        : "#dc2626";

  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #e2e8f0",
        borderRadius: "12px",
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "1rem 1.25rem",
          borderBottom: "1px solid #f1f5f9",
          background: "#fafbfc",
        }}
      >
        <div>
          <h3 style={{ margin: 0, fontSize: "1rem" }}>
            {application.full_name}
          </h3>
          <span style={{ fontSize: "0.75rem", color: "#64748b" }}>
            ID: {application.applicant_id} &middot; Escalated{" "}
            {new Date(application.escalated_at).toLocaleString()}
          </span>
        </div>
        <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
          <span
            style={{
              padding: "0.25rem 0.75rem",
              borderRadius: "9999px",
              fontSize: "0.75rem",
              fontWeight: 600,
              background: status.bg,
              color: status.color,
            }}
          >
            {application.status}
          </span>
          <div style={{ textAlign: "center" }}>
            <div
              style={{
                fontSize: "1.5rem",
                fontWeight: 700,
                color: riskColor,
                lineHeight: 1,
              }}
            >
              {application.risk_score}
            </div>
            <div style={{ fontSize: "0.65rem", color: "#94a3b8" }}>
              RISK SCORE
            </div>
          </div>
        </div>
      </div>

      {/* Body */}
      <div style={{ padding: "1.25rem" }}>
        {/* AI Reasoning */}
        <Section title="AI Risk Assessment">
          <p style={{ margin: 0, fontSize: "0.85rem", color: "#475569" }}>
            {application.reasoning}
          </p>
        </Section>

        {/* Risk Factors & Compensating Factors */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "1rem",
            marginTop: "1rem",
          }}
        >
          <Section title="Risk Factors" color="#dc2626">
            {application.risk_factors.length === 0 ? (
              <em style={{ color: "#94a3b8", fontSize: "0.8rem" }}>
                None identified
              </em>
            ) : (
              <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
                {application.risk_factors.map((f, i) => (
                  <li key={i} style={{ fontSize: "0.8rem", color: "#475569" }}>
                    {f}
                  </li>
                ))}
              </ul>
            )}
          </Section>
          <Section title="Compensating Factors" color="#16a34a">
            {application.compensating_factors.length === 0 ? (
              <em style={{ color: "#94a3b8", fontSize: "0.8rem" }}>
                None identified
              </em>
            ) : (
              <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
                {application.compensating_factors.map((f, i) => (
                  <li key={i} style={{ fontSize: "0.8rem", color: "#475569" }}>
                    {f}
                  </li>
                ))}
              </ul>
            )}
          </Section>
        </div>

        {/* Compliance Flags */}
        {application.compliance_flags.length > 0 && (
          <Section title="Compliance Flags" style={{ marginTop: "1rem" }}>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "0.5rem",
              }}
            >
              {application.compliance_flags.map((flag, i) => (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    gap: "0.5rem",
                    alignItems: "flex-start",
                    fontSize: "0.8rem",
                    padding: "0.5rem",
                    background: "#f8fafc",
                    borderRadius: "6px",
                    borderLeft: `3px solid ${SEVERITY_COLORS[flag.severity] ?? "#94a3b8"}`,
                  }}
                >
                  <span
                    style={{
                      fontWeight: 600,
                      textTransform: "uppercase",
                      fontSize: "0.65rem",
                      color: SEVERITY_COLORS[flag.severity],
                      flexShrink: 0,
                    }}
                  >
                    {flag.severity}
                  </span>
                  <span style={{ color: "#475569" }}>
                    <strong>{flag.rule}</strong>: {flag.message}
                  </span>
                </div>
              ))}
            </div>
          </Section>
        )}

        {/* Conditions */}
        {application.compliance_conditions.length > 0 && (
          <Section title="Required Conditions" style={{ marginTop: "1rem" }}>
            <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
              {application.compliance_conditions.map((c, i) => (
                <li key={i} style={{ fontSize: "0.8rem", color: "#475569" }}>
                  {c}
                </li>
              ))}
            </ul>
          </Section>
        )}

        {/* Application Data Summary */}
        <Section title="Application Data" style={{ marginTop: "1rem" }}>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
              gap: "0.5rem",
            }}
          >
            {Object.entries(application.application_data).map(
              ([key, value]) => (
                <div
                  key={key}
                  style={{
                    padding: "0.4rem 0.6rem",
                    background: "#f8fafc",
                    borderRadius: "6px",
                    fontSize: "0.8rem",
                  }}
                >
                  <span
                    style={{
                      color: "#94a3b8",
                      display: "block",
                      fontSize: "0.65rem",
                      textTransform: "uppercase",
                    }}
                  >
                    {key.replace(/_/g, " ")}
                  </span>
                  <span style={{ color: "#1e293b", fontWeight: 500 }}>
                    {typeof value === "number"
                      ? value.toLocaleString()
                      : String(value)}
                  </span>
                </div>
              ),
            )}
          </div>
        </Section>

        {/* Review Actions */}
        {application.status === "PENDING" && (
          <div
            style={{
              marginTop: "1.25rem",
              padding: "1rem",
              background: "#f8fafc",
              borderRadius: "8px",
              border: "1px solid #e2e8f0",
            }}
          >
            <label
              style={{
                display: "block",
                fontSize: "0.8rem",
                fontWeight: 600,
                color: "#475569",
                marginBottom: "0.5rem",
              }}
            >
              Review Notes
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Add notes explaining your decision…"
              rows={2}
              style={{
                width: "100%",
                padding: "0.5rem",
                border: "1px solid #cbd5e1",
                borderRadius: "6px",
                fontSize: "0.85rem",
                resize: "vertical",
                fontFamily: "inherit",
                boxSizing: "border-box",
              }}
            />
            <div
              style={{ display: "flex", gap: "0.5rem", marginTop: "0.75rem" }}
            >
              <ActionButton
                label="Approve"
                color="#16a34a"
                disabled={submitting}
                onClick={() => handleAction("APPROVED")}
              />
              <ActionButton
                label="Decline"
                color="#dc2626"
                disabled={submitting}
                onClick={() => handleAction("DECLINED")}
              />
              <ActionButton
                label="Request Info"
                color="#2563eb"
                disabled={submitting}
                onClick={() => handleAction("INFO_REQUESTED")}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/* ---------- Helpers ---------- */

function Section({
  title,
  color,
  style,
  children,
}: {
  title: string;
  color?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}) {
  return (
    <div style={style}>
      <h4
        style={{
          margin: "0 0 0.5rem 0",
          fontSize: "0.75rem",
          textTransform: "uppercase",
          letterSpacing: "0.05em",
          color: color ?? "#64748b",
        }}
      >
        {title}
      </h4>
      {children}
    </div>
  );
}

function ActionButton({
  label,
  color,
  disabled,
  onClick,
}: {
  label: string;
  color: string;
  disabled: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        padding: "0.5rem 1.25rem",
        background: color,
        color: "#fff",
        border: "none",
        borderRadius: "6px",
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.5 : 1,
        fontSize: "0.85rem",
        fontWeight: 500,
      }}
    >
      {label}
    </button>
  );
}
