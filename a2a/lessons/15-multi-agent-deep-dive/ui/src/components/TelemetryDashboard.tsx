import { useCallback, useEffect, useState } from "react";
import { fetchAll, fetchStats } from "../api";
import type { EscalatedApplication, Stats } from "../types";
import { AgentLatencyChart } from "./AgentLatencyChart";
import { DecisionChart } from "./DecisionChart";
import { TraceWaterfall } from "./TraceWaterfall";

const POLL_INTERVAL_MS = 5000;

const INITIAL_STATS: Stats = {
  total: 0,
  pending: 0,
  approved: 0,
  declined: 0,
  info_requested: 0,
};

export function TelemetryDashboard() {
  const [stats, setStats] = useState<Stats>(INITIAL_STATS);
  const [applications, setApplications] = useState<EscalatedApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const [s, apps] = await Promise.all([fetchStats(), fetchAll()]);
      setStats(s);
      setApplications(apps);
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

  if (loading) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <p>Loading telemetry data…</p>
      </div>
    );
  }

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1.5rem",
        }}
      >
        <h2>📊 Telemetry Dashboard</h2>
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

      {/* KPI Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
          gap: "1rem",
          marginBottom: "2rem",
        }}
      >
        <KPICard label="Total Processed" value={stats.total} color="#3b82f6" />
        <KPICard label="Pending Review" value={stats.pending} color="#f59e0b" />
        <KPICard label="Approved" value={stats.approved} color="#16a34a" />
        <KPICard label="Declined" value={stats.declined} color="#dc2626" />
        <KPICard
          label="Info Requested"
          value={stats.info_requested}
          color="#8b5cf6"
        />
      </div>

      {/* Charts Row */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "1.5rem",
          marginBottom: "2rem",
        }}
      >
        <ChartPanel title="Decision Distribution">
          <DecisionChart stats={stats} />
        </ChartPanel>
        <ChartPanel title="Agent Pipeline Latency">
          <AgentLatencyChart />
        </ChartPanel>
      </div>

      {/* Trace Waterfall */}
      <ChartPanel title="Pipeline Trace Waterfall">
        <TraceWaterfall applications={applications} />
      </ChartPanel>
    </div>
  );
}

/* ---------- Helpers ---------- */

function KPICard({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #e2e8f0",
        borderRadius: "12px",
        padding: "1.25rem",
        borderTop: `3px solid ${color}`,
      }}
    >
      <div
        style={{
          fontSize: "0.7rem",
          textTransform: "uppercase",
          color: "#94a3b8",
          letterSpacing: "0.05em",
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: "2rem",
          fontWeight: 700,
          color,
          lineHeight: 1.2,
          marginTop: "0.25rem",
        }}
      >
        {value}
      </div>
    </div>
  );
}

function ChartPanel({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #e2e8f0",
        borderRadius: "12px",
        padding: "1.25rem",
      }}
    >
      <h3
        style={{
          margin: "0 0 1rem 0",
          fontSize: "0.85rem",
          textTransform: "uppercase",
          letterSpacing: "0.05em",
          color: "#64748b",
        }}
      >
        {title}
      </h3>
      {children}
    </div>
  );
}
