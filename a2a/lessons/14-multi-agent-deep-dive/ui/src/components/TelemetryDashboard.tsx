import { useCallback, useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import RefreshIcon from "@mui/icons-material/Refresh";
import { alpha } from "@mui/material/styles";
import { fetchAll, fetchStats } from "../api";
import type { EscalatedApplication, Stats } from "../types";
import { AgentLatencyChart } from "./AgentLatencyChart";
import { DecisionChart } from "./DecisionChart";
import { TraceWaterfall } from "./TraceWaterfall";
import { glass } from "../theme";

const POLL_INTERVAL_MS = 5000;

const INITIAL_STATS: Stats = {
  total: 0,
  pending: 0,
  approved: 0,
  declined: 0,
  escalated: 0,
  human_approved: 0,
  human_declined: 0,
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
      <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: { xs: 2, md: 3 }, maxWidth: 1400, mx: "auto" }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Typography variant="h4" fontWeight={700}>
          Telemetry Dashboard
        </Typography>
        <Tooltip title="Refresh">
          <IconButton onClick={refresh}>
            <RefreshIcon />
          </IconButton>
        </Tooltip>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box
        sx={{
          mb: 3,
          display: "grid",
          gap: 2,
          gridTemplateColumns: {
            xs: "repeat(2, minmax(0, 1fr))",
            md: "repeat(3, minmax(0, 1fr))",
            lg: "repeat(5, minmax(0, 1fr))",
          },
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
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, lg: 6 }}>
          <ChartPanel title="Decision Distribution">
            <DecisionChart stats={stats} />
          </ChartPanel>
        </Grid>
        <Grid size={{ xs: 12, lg: 6 }}>
          <ChartPanel title="Agent Pipeline Latency">
            <AgentLatencyChart />
          </ChartPanel>
        </Grid>
      </Grid>

      <ChartPanel title="Pipeline Trace Waterfall">
        <TraceWaterfall applications={applications} />
      </ChartPanel>

      <Box sx={{ mt: 2, textAlign: "right" }}>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={refresh}
        >
          Refresh
        </Button>
      </Box>
    </Box>
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
    <Card
      sx={{
        ...glass,
        position: "relative",
        overflow: "hidden",
        "&::before": {
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 3,
          background: `linear-gradient(90deg, ${color}, ${alpha(color, 0.3)})`,
        },
      }}
    >
      <CardContent sx={{ p: 2.5 }}>
        <Typography
          variant="overline"
          color="text.secondary"
          sx={{ fontSize: "0.65rem" }}
        >
          {label}
        </Typography>
        <Typography
          variant="h3"
          fontWeight={700}
          sx={{ color, lineHeight: 1.2 }}
        >
          {value}
        </Typography>
      </CardContent>
    </Card>
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
    <Card sx={{ ...glass }}>
      <CardContent>
        <Typography
          variant="overline"
          color="text.secondary"
          sx={{ display: "block", mb: 1 }}
        >
          {title}
        </Typography>
        {children}
      </CardContent>
    </Card>
  );
}
