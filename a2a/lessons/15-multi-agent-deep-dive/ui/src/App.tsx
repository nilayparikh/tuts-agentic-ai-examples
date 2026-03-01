import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import { ApprovalQueue } from "./components/ApprovalQueue";
import { TelemetryDashboard } from "./components/TelemetryDashboard";

const navStyle = {
  display: "flex",
  gap: "1rem",
  padding: "1rem 2rem",
  background: "#1a1a2e",
  color: "#fff",
  alignItems: "center",
} as const;

const linkStyle = {
  color: "#94a3b8",
  textDecoration: "none",
  padding: "0.5rem 1rem",
  borderRadius: "6px",
  fontSize: "0.9rem",
  fontWeight: 500,
} as const;

const activeLinkStyle = {
  ...linkStyle,
  color: "#fff",
  background: "#334155",
} as const;

function Home() {
  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "1rem" }}>
        🏦 Multi-Agent Loan Approval System
      </h1>
      <p style={{ marginBottom: "1.5rem", color: "#475569" }}>
        A production-grade loan approval pipeline powered by five specialized
        A2A agents with human-in-the-loop escalation and OpenTelemetry
        observability.
      </p>
      <div
        style={{ display: "grid", gap: "1rem", gridTemplateColumns: "1fr 1fr" }}
      >
        <NavLink to="/approvals" style={{ textDecoration: "none" }}>
          <div
            style={{
              padding: "1.5rem",
              background: "#fff",
              borderRadius: "12px",
              border: "1px solid #e2e8f0",
              cursor: "pointer",
            }}
          >
            <h3>📋 Approval Queue</h3>
            <p style={{ color: "#64748b", fontSize: "0.9rem" }}>
              Review and decide on escalated loan applications
            </p>
          </div>
        </NavLink>
        <NavLink to="/dashboard" style={{ textDecoration: "none" }}>
          <div
            style={{
              padding: "1.5rem",
              background: "#fff",
              borderRadius: "12px",
              border: "1px solid #e2e8f0",
              cursor: "pointer",
            }}
          >
            <h3>📊 Telemetry Dashboard</h3>
            <p style={{ color: "#64748b", fontSize: "0.9rem" }}>
              View traces, latencies, and decision distributions
            </p>
          </div>
        </NavLink>
      </div>
    </div>
  );
}

export function App() {
  return (
    <BrowserRouter>
      <nav style={navStyle}>
        <span
          style={{ fontWeight: 700, fontSize: "1.1rem", marginRight: "1rem" }}
        >
          🏦 Loan Approval
        </span>
        <NavLink
          to="/"
          end
          style={({ isActive }) => (isActive ? activeLinkStyle : linkStyle)}
        >
          Home
        </NavLink>
        <NavLink
          to="/approvals"
          style={({ isActive }) => (isActive ? activeLinkStyle : linkStyle)}
        >
          Approval Queue
        </NavLink>
        <NavLink
          to="/dashboard"
          style={({ isActive }) => (isActive ? activeLinkStyle : linkStyle)}
        >
          Dashboard
        </NavLink>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/approvals" element={<ApprovalQueue />} />
        <Route path="/dashboard" element={<TelemetryDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
