import type { EscalatedApplication } from "../types";

/** Simulated per-agent pipeline step timing. */
interface PipelineStep {
  agent: string;
  startMs: number;
  durationMs: number;
  color: string;
}

const AGENT_COLORS: Record<string, string> = {
  Intake: "#3b82f6",
  "Risk Scorer": "#f59e0b",
  Compliance: "#8b5cf6",
  Decision: "#06b6d4",
  Escalation: "#ec4899",
};

/**
 * Generates simulated pipeline steps for a single application.
 * In a production system these would come from OpenTelemetry span data
 * collected via the OTLP exporter and queried from Jaeger / Tempo.
 */
function simulateSteps(riskScore: number): PipelineStep[] {
  const base = 50 + Math.random() * 30;
  const steps: PipelineStep[] = [];
  let offset = 0;

  const add = (agent: string, duration: number) => {
    steps.push({
      agent,
      startMs: offset,
      durationMs: duration,
      color: AGENT_COLORS[agent] ?? "#94a3b8",
    });
    offset += duration + 10; // 10ms network gap
  };

  add("Intake", base);
  add("Risk Scorer", base * 2.5 + Math.random() * 200); // LLM call
  add("Compliance", base * 1.2);
  add("Decision", base * 0.5);

  if (riskScore > 40 && riskScore <= 80) {
    add("Escalation", base * 0.8);
  }

  return steps;
}

interface Props {
  applications: EscalatedApplication[];
}

export function TraceWaterfall({ applications }: Props) {
  if (applications.length === 0) {
    return (
      <div style={{ padding: "2rem", textAlign: "center", color: "#94a3b8" }}>
        No trace data available yet.
      </div>
    );
  }

  // Show the 8 most recent
  const recent = applications.slice(-8).reverse();

  return (
    <div style={{ overflowX: "auto" }}>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          fontSize: "0.8rem",
        }}
      >
        <thead>
          <tr style={{ borderBottom: "2px solid #e2e8f0" }}>
            <th
              style={{
                textAlign: "left",
                padding: "0.5rem",
                color: "#64748b",
                width: "140px",
              }}
            >
              Applicant
            </th>
            <th
              style={{ textAlign: "left", padding: "0.5rem", color: "#64748b" }}
            >
              Pipeline Timeline
            </th>
            <th
              style={{
                textAlign: "right",
                padding: "0.5rem",
                color: "#64748b",
                width: "80px",
              }}
            >
              Total
            </th>
          </tr>
        </thead>
        <tbody>
          {recent.map((app) => {
            const steps = simulateSteps(app.risk_score);
            const totalMs =
              steps.length > 0
                ? (steps[steps.length - 1]?.startMs ?? 0) +
                  (steps[steps.length - 1]?.durationMs ?? 0)
                : 0;
            const maxMs = Math.max(totalMs, 1);

            return (
              <tr key={app.id} style={{ borderBottom: "1px solid #f1f5f9" }}>
                <td
                  style={{
                    padding: "0.5rem",
                    fontWeight: 500,
                    color: "#1e293b",
                  }}
                >
                  {app.full_name}
                  <div style={{ fontSize: "0.65rem", color: "#94a3b8" }}>
                    Score: {app.risk_score}
                  </div>
                </td>
                <td style={{ padding: "0.5rem" }}>
                  <div
                    style={{
                      position: "relative",
                      height: "24px",
                      background: "#f8fafc",
                      borderRadius: "4px",
                    }}
                  >
                    {steps.map((step, i) => {
                      const left = (step.startMs / maxMs) * 100;
                      const width = Math.max(
                        (step.durationMs / maxMs) * 100,
                        2,
                      );
                      return (
                        <div
                          key={i}
                          title={`${step.agent}: ${step.durationMs.toFixed(0)}ms`}
                          style={{
                            position: "absolute",
                            left: `${left}%`,
                            width: `${width}%`,
                            top: "3px",
                            bottom: "3px",
                            background: step.color,
                            borderRadius: "3px",
                            opacity: 0.85,
                            cursor: "pointer",
                          }}
                        />
                      );
                    })}
                  </div>
                </td>
                <td
                  style={{
                    padding: "0.5rem",
                    textAlign: "right",
                    fontFamily: "monospace",
                    color: "#475569",
                  }}
                >
                  {totalMs.toFixed(0)}ms
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Legend */}
      <div
        style={{
          display: "flex",
          gap: "1rem",
          marginTop: "0.75rem",
          flexWrap: "wrap",
        }}
      >
        {Object.entries(AGENT_COLORS).map(([agent, color]) => (
          <div
            key={agent}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.35rem",
              fontSize: "0.7rem",
            }}
          >
            <div
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "2px",
                background: color,
              }}
            />
            <span style={{ color: "#64748b" }}>{agent}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
