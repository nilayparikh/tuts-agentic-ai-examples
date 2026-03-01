import { useCallback, useEffect, useState } from "react";
import { fetchPending, submitDecision } from "../api";
import type { Decision, EscalatedApplication } from "../types";
import { ApplicationCard } from "./ApplicationCard";

const POLL_INTERVAL_MS = 3000;

export function ApprovalQueue() {
  const [pending, setPending] = useState<EscalatedApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const data = await fetchPending();
      setPending(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [refresh]);

  const handleDecision = async (
    id: string,
    decision: Decision,
    notes: string,
  ) => {
    try {
      await submitDecision(id, decision, "Reviewer", notes);
      setPending((prev) => prev.filter((app) => app.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit");
    }
  };

  if (loading) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <p>Loading pending applications…</p>
      </div>
    );
  }

  return (
    <div style={{ padding: "2rem", maxWidth: "1000px", margin: "0 auto" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1.5rem",
        }}
      >
        <h2>📋 Pending Human Review ({pending.length})</h2>
        <button
          onClick={refresh}
          style={{
            padding: "0.5rem 1rem",
            background: "#3b82f6",
            color: "#fff",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontSize: "0.85rem",
          }}
        >
          Refresh
        </button>
      </div>

      {error && (
        <div
          style={{
            padding: "1rem",
            background: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: "8px",
            color: "#991b1b",
            marginBottom: "1rem",
          }}
        >
          {error}
        </div>
      )}

      {pending.length === 0 ? (
        <div
          style={{
            padding: "3rem",
            textAlign: "center",
            background: "#fff",
            borderRadius: "12px",
            border: "1px solid #e2e8f0",
            color: "#64748b",
          }}
        >
          <p style={{ fontSize: "1.1rem" }}>No pending applications</p>
          <p style={{ fontSize: "0.85rem", marginTop: "0.5rem" }}>
            Submit test applications with{" "}
            <code>python submit_test_batch.py</code>
          </p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          {pending.map((app) => (
            <ApplicationCard
              key={app.id}
              application={app}
              onDecision={handleDecision}
            />
          ))}
        </div>
      )}
    </div>
  );
}
