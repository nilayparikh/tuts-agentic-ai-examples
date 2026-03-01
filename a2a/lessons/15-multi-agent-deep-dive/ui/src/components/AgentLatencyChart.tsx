import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

/** Simulated average latency per agent in the pipeline. */
const AGENT_LATENCY = [
  { agent: "Intake", avgMs: 65, color: "#3b82f6" },
  { agent: "Risk Scorer", avgMs: 380, color: "#f59e0b" },
  { agent: "Compliance", avgMs: 95, color: "#8b5cf6" },
  { agent: "Decision", avgMs: 35, color: "#06b6d4" },
  { agent: "Escalation", avgMs: 55, color: "#ec4899" },
];

export function AgentLatencyChart() {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart
        data={AGENT_LATENCY}
        layout="vertical"
        margin={{ left: 20, right: 20 }}
      >
        <CartesianGrid strokeDasharray="3 3" horizontal={false} />
        <XAxis
          type="number"
          tick={{ fontSize: 11, fill: "#64748b" }}
          tickFormatter={(v: number) => `${v}ms`}
        />
        <YAxis
          type="category"
          dataKey="agent"
          tick={{ fontSize: 11, fill: "#64748b" }}
          width={90}
        />
        <Tooltip
          formatter={(value: number) => [`${value}ms`, "Avg Latency"]}
          contentStyle={{
            borderRadius: "8px",
            border: "1px solid #e2e8f0",
            fontSize: "0.8rem",
          }}
        />
        <Bar
          dataKey="avgMs"
          radius={[0, 6, 6, 0]}
          barSize={22}
          isAnimationActive={true}
        >
          {AGENT_LATENCY.map((entry, i) => (
            <Cell key={i} fill={entry.color} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
