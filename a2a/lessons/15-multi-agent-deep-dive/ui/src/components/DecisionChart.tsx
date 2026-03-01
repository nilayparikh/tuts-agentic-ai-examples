import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import type { Stats } from "../types";

const COLORS: Record<string, string> = {
  Approved: "#16a34a",
  Declined: "#dc2626",
  Pending: "#f59e0b",
  "Info Req.": "#8b5cf6",
};

interface Props {
  stats: Stats;
}

export function DecisionChart({ stats }: Props) {
  const data = [
    { name: "Approved", value: stats.approved },
    { name: "Declined", value: stats.declined },
    { name: "Pending", value: stats.pending },
    { name: "Info Req.", value: stats.info_requested },
  ].filter((d) => d.value > 0);

  if (data.length === 0) {
    return (
      <div
        style={{
          height: 250,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#94a3b8",
        }}
      >
        No decisions recorded yet.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={55}
          outerRadius={90}
          paddingAngle={3}
          dataKey="value"
          label={({ name, percent }) =>
            `${name} ${(percent * 100).toFixed(0)}%`
          }
          labelLine={false}
        >
          {data.map((entry) => (
            <Cell key={entry.name} fill={COLORS[entry.name] ?? "#94a3b8"} />
          ))}
        </Pie>
        <Tooltip
          formatter={(value: number) => [value, "Applications"]}
          contentStyle={{
            borderRadius: "8px",
            border: "1px solid #e2e8f0",
            fontSize: "0.8rem",
          }}
        />
        <Legend
          verticalAlign="bottom"
          height={36}
          iconType="circle"
          iconSize={8}
          wrapperStyle={{ fontSize: "0.75rem" }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
