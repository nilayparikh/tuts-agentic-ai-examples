/**
 * LoanDashboard — All processed loans: stats summary + list + detail drawer.
 *
 * Shows every application that ran through the multi-agent pipeline:
 * auto-approved, auto-declined, escalated (with human decision), and rejected.
 */

import { useCallback, useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Chip from "@mui/material/Chip";
import IconButton from "@mui/material/IconButton";
import Drawer from "@mui/material/Drawer";
import Toolbar from "@mui/material/Toolbar";
import AppBar from "@mui/material/AppBar";
import Divider from "@mui/material/Divider";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import Tooltip from "@mui/material/Tooltip";
import LinearProgress from "@mui/material/LinearProgress";
import Avatar from "@mui/material/Avatar";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import { alpha } from "@mui/material/styles";

import RefreshIcon from "@mui/icons-material/Refresh";
import SearchIcon from "@mui/icons-material/Search";
import CloseIcon from "@mui/icons-material/Close";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CancelIcon from "@mui/icons-material/Cancel";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import GavelIcon from "@mui/icons-material/Gavel";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import PersonIcon from "@mui/icons-material/Person";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import SecurityIcon from "@mui/icons-material/Security";
import AssignmentIcon from "@mui/icons-material/Assignment";

import { fetchLoans, fetchStats } from "../api";
import type { ProcessedLoanRecord, Stats } from "../types";
import { DECISION_COLORS, scoreColor, glass } from "../theme";

const POLL_MS = 5000;
const DRAWER_WIDTH = 640;

// ── Helper components ──────────────────────────────────────────────────────

function DecisionChip({ decision }: { decision: string }) {
  const cfg =
    DECISION_COLORS[decision as keyof typeof DECISION_COLORS] ??
    DECISION_COLORS.REJECTED;

  const icons: Record<string, React.ReactNode> = {
    APPROVED: <CheckCircleIcon sx={{ fontSize: 14 }} />,
    DECLINED: <CancelIcon sx={{ fontSize: 14 }} />,
    PENDING_REVIEW: <GavelIcon sx={{ fontSize: 14 }} />,
    PENDING: <HourglassEmptyIcon sx={{ fontSize: 14 }} />,
    INFO_REQUESTED: <WarningAmberIcon sx={{ fontSize: 14 }} />,
    REJECTED: <CancelIcon sx={{ fontSize: 14 }} />,
  };

  return (
    <Chip
      size="small"
      icon={icons[decision] as React.ReactElement}
      label={decision.replace(/_/g, " ")}
      sx={{
        background: cfg.bg,
        color: cfg.text,
        border: `1px solid ${alpha(cfg.main, 0.3)}`,
        "& .MuiChip-icon": { color: cfg.text },
        fontWeight: 700,
        fontSize: "0.68rem",
        letterSpacing: "0.04em",
      }}
    />
  );
}

function RiskGauge({ score }: { score: number }) {
  const color = scoreColor(score);
  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1, minWidth: 100 }}>
      <Box sx={{ flex: 1 }}>
        <LinearProgress
          variant="determinate"
          value={score}
          sx={{
            height: 6,
            borderRadius: 3,
            bgcolor: alpha(color, 0.15),
            "& .MuiLinearProgress-bar": { bgcolor: color, borderRadius: 3 },
          }}
        />
      </Box>
      <Typography variant="body2" fontWeight={700} sx={{ color, minWidth: 28 }}>
        {score}
      </Typography>
    </Box>
  );
}

function KpiCard({
  label,
  value,
  icon,
  color,
  sublabel,
}: {
  label: string;
  value: number;
  icon: React.ReactNode;
  color: string;
  sublabel?: string;
}) {
  return (
    <Card
      sx={{
        height: "100%",
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
        <Box sx={{ display: "flex", justifyContent: "space-between", mb: 1.5 }}>
          <Box
            sx={{
              width: 44,
              height: 44,
              borderRadius: 2,
              background: alpha(color, 0.15),
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color,
            }}
          >
            {icon}
          </Box>
        </Box>
        <Typography variant="h3" fontWeight={700} sx={{ color }}>
          {value}
        </Typography>
        <Typography variant="body2" color="text.secondary" fontWeight={500}>
          {label}
        </Typography>
        {sublabel && (
          <Typography variant="caption" color="text.secondary">
            {sublabel}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

// ── Loan Detail Drawer ────────────────────────────────────────────────────

function LoanDetailDrawer({
  loan,
  onClose,
}: {
  loan: ProcessedLoanRecord | null;
  onClose: () => void;
}) {
  const open = Boolean(loan);

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      sx={{
        "& .MuiDrawer-paper": {
          width: { xs: "100vw", sm: DRAWER_WIDTH },
          background: "transparent",
          boxShadow: "none",
        },
      }}
    >
      {loan && <DetailContent loan={loan} onClose={onClose} />}
    </Drawer>
  );
}

function DetailContent({
  loan,
  onClose,
}: {
  loan: ProcessedLoanRecord;
  onClose: () => void;
}) {
  const decisionColor =
    DECISION_COLORS[loan.decision as keyof typeof DECISION_COLORS] ??
    DECISION_COLORS.REJECTED;

  const initials = loan.full_name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <Box
      sx={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        ...glass,
        borderLeft: `1px solid ${alpha("#6395ff", 0.2)}`,
      }}
    >
      {/* Header */}
      <AppBar
        position="static"
        elevation={0}
        sx={{
          background: alpha("#050d1a", 0.9),
          borderBottom: "1px solid",
          borderColor: "divider",
        }}
      >
        <Toolbar sx={{ gap: 1.5 }}>
          <Avatar
            sx={{
              bgcolor: alpha(decisionColor.main, 0.2),
              color: decisionColor.text,
              border: `2px solid ${alpha(decisionColor.main, 0.4)}`,
            }}
          >
            {initials}
          </Avatar>
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle1" fontWeight={700}>
              {loan.full_name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {loan.applicant_id}
            </Typography>
          </Box>
          <DecisionChip decision={loan.decision} />
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Scrollable body */}
      <Box sx={{ flex: 1, overflow: "auto", p: 3 }}>
        {/* Risk + Action summary */}
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr 1fr",
            gap: 2,
            mb: 3,
          }}
        >
          <StatBox
            label="Risk Score"
            value={String(loan.score)}
            color={scoreColor(loan.score)}
          />
          <StatBox
            label="Action"
            value={loan.action.replace(/_/g, " ")}
            color={decisionColor.main}
          />
          <StatBox
            label="Compliant"
            value={loan.compliant ? "Yes" : "No"}
            color={loan.compliant ? "#10b981" : "#ef4444"}
          />
        </Box>

        <PipelineTimeline loan={loan} />

        {/* Decision rationale */}
        <Section icon={<AssignmentIcon />} title="Decision Rationale">
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ lineHeight: 1.7 }}
          >
            {loan.reason}
          </Typography>
          {loan.reasoning && (
            <>
              <Divider sx={{ my: 1.5 }} />
              <Typography
                variant="caption"
                color="text.secondary"
                sx={{ display: "block", mb: 0.5 }}
              >
                AI Assessment
              </Typography>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ lineHeight: 1.7 }}
              >
                {loan.reasoning}
              </Typography>
            </>
          )}
        </Section>

        {/* Risk factors grid */}
        {(loan.risk_factors.length > 0 ||
          loan.compensating_factors.length > 0) && (
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 2,
              mt: 2,
            }}
          >
            {loan.risk_factors.length > 0 && (
              <Section
                icon={<TrendingUpIcon />}
                title="Risk Factors"
                accentColor="#ef4444"
              >
                <Stack spacing={0.5}>
                  {loan.risk_factors.map((f, i) => (
                    <Box
                      key={i}
                      sx={{
                        display: "flex",
                        alignItems: "flex-start",
                        gap: 0.75,
                      }}
                    >
                      <Box
                        sx={{
                          width: 6,
                          height: 6,
                          borderRadius: "50%",
                          bgcolor: "#ef4444",
                          mt: 0.75,
                          flexShrink: 0,
                        }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        {f}
                      </Typography>
                    </Box>
                  ))}
                </Stack>
              </Section>
            )}
            {loan.compensating_factors.length > 0 && (
              <Section
                icon={<TrendingDownIcon />}
                title="Compensating Factors"
                accentColor="#10b981"
              >
                <Stack spacing={0.5}>
                  {loan.compensating_factors.map((f, i) => (
                    <Box
                      key={i}
                      sx={{
                        display: "flex",
                        alignItems: "flex-start",
                        gap: 0.75,
                      }}
                    >
                      <Box
                        sx={{
                          width: 6,
                          height: 6,
                          borderRadius: "50%",
                          bgcolor: "#10b981",
                          mt: 0.75,
                          flexShrink: 0,
                        }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        {f}
                      </Typography>
                    </Box>
                  ))}
                </Stack>
              </Section>
            )}
          </Box>
        )}

        {/* Compliance flags */}
        {loan.flags.length > 0 && (
          <Section
            icon={<SecurityIcon />}
            title="Compliance Flags"
            sx={{ mt: 2 }}
          >
            <Stack spacing={1}>
              {loan.flags.map((flag, i) => {
                const flagColor =
                  flag.severity === "hard" ? "#ef4444" : "#f59e0b";
                return (
                  <Box
                    key={i}
                    sx={{
                      p: 1.5,
                      borderRadius: 2,
                      background: alpha(flagColor, 0.08),
                      borderLeft: `3px solid ${flagColor}`,
                    }}
                  >
                    <Box
                      sx={{
                        display: "flex",
                        gap: 1,
                        alignItems: "center",
                        mb: 0.25,
                      }}
                    >
                      <Chip
                        size="small"
                        label={flag.severity?.toUpperCase() ?? "FLAG"}
                        sx={{
                          height: 18,
                          fontSize: "0.6rem",
                          bgcolor: alpha(flagColor, 0.15),
                          color: flagColor,
                          fontWeight: 700,
                        }}
                      />
                      <Typography variant="caption" fontWeight={700}>
                        {flag.rule}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {flag.message}
                    </Typography>
                  </Box>
                );
              })}
            </Stack>
          </Section>
        )}

        {/* Compliance conditions */}
        {loan.conditions.length > 0 && (
          <Section
            icon={<SecurityIcon />}
            title="Required Conditions"
            sx={{ mt: 2 }}
          >
            <Stack spacing={0.5}>
              {loan.conditions.map((c, i) => (
                <Typography key={i} variant="body2" color="text.secondary">
                  {i + 1}. {c}
                </Typography>
              ))}
            </Stack>
          </Section>
        )}

        {/* Application data */}
        <Section icon={<PersonIcon />} title="Application Data" sx={{ mt: 2 }}>
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))",
              gap: 1,
            }}
          >
            {Object.entries(loan.application_data)
              .filter(([, v]) => v !== null && v !== undefined)
              .map(([key, value]) => (
                <Box
                  key={key}
                  sx={{
                    p: 1.25,
                    borderRadius: 2,
                    background: alpha("#6395ff", 0.06),
                    border: "1px solid",
                    borderColor: "divider",
                  }}
                >
                  <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{
                      display: "block",
                      textTransform: "uppercase",
                      fontSize: "0.6rem",
                      mb: 0.25,
                    }}
                  >
                    {key.replace(/_/g, " ")}
                  </Typography>
                  <Typography variant="body2" fontWeight={600}>
                    {typeof value === "number"
                      ? value.toLocaleString()
                      : String(value)}
                  </Typography>
                </Box>
              ))}
          </Box>
        </Section>

        {/* Thresholds */}
        {loan.thresholds && Object.keys(loan.thresholds).length > 0 && (
          <Section
            icon={<AccountBalanceIcon />}
            title="Decision Thresholds"
            sx={{ mt: 2 }}
          >
            <Box sx={{ display: "flex", gap: 2 }}>
              {loan.thresholds.auto_approve !== undefined && (
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Auto-Approve
                  </Typography>
                  <Typography
                    variant="body2"
                    fontWeight={700}
                    color="success.main"
                  >
                    Score &le; {loan.thresholds.auto_approve}
                  </Typography>
                </Box>
              )}
              {loan.thresholds.auto_decline !== undefined && (
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Auto-Decline
                  </Typography>
                  <Typography
                    variant="body2"
                    fontWeight={700}
                    color="error.main"
                  >
                    Score &ge; {loan.thresholds.auto_decline}
                  </Typography>
                </Box>
              )}
            </Box>
          </Section>
        )}

        {/* Human decision (if escalated) */}
        {loan.human_decision && (
          <Section
            icon={<GavelIcon />}
            title="Human Review Decision"
            accentColor={
              loan.human_decision === "APPROVED"
                ? "#10b981"
                : loan.human_decision === "DECLINED"
                  ? "#ef4444"
                  : "#3b82f6"
            }
            sx={{ mt: 2 }}
          >
            <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", mb: 1 }}>
              <DecisionChip decision={loan.human_decision} />
              {loan.human_decided_by && (
                <Typography variant="body2" color="text.secondary">
                  Reviewed by <strong>{loan.human_decided_by}</strong>
                </Typography>
              )}
              {loan.human_decided_at && (
                <Typography variant="body2" color="text.secondary">
                  {new Date(loan.human_decided_at).toLocaleString()}
                </Typography>
              )}
            </Box>
            {loan.human_decision_notes && (
              <Box
                sx={{
                  p: 1.5,
                  borderRadius: 2,
                  background: alpha("#6395ff", 0.06),
                  border: "1px solid",
                  borderColor: "divider",
                }}
              >
                <Typography variant="body2" color="text.secondary">
                  {loan.human_decision_notes}
                </Typography>
              </Box>
            )}
          </Section>
        )}

        {/* Timestamps */}
        <Box
          sx={{ mt: 3, pt: 2, borderTop: "1px solid", borderColor: "divider" }}
        >
          <Typography variant="caption" color="text.secondary">
            Processed: {new Date(loan.processed_at).toLocaleString()}
          </Typography>
          {loan.escalation_id && (
            <Typography variant="caption" color="text.secondary" sx={{ ml: 2 }}>
              Escalation ID: {loan.escalation_id.slice(0, 8)}…
            </Typography>
          )}
        </Box>
      </Box>
    </Box>
  );
}

function StatBox({
  label,
  value,
  color,
}: {
  label: string;
  value: string;
  color: string;
}) {
  return (
    <Box
      sx={{
        p: 1.5,
        borderRadius: 2,
        background: alpha(color, 0.08),
        border: `1px solid ${alpha(color, 0.2)}`,
        textAlign: "center",
      }}
    >
      <Typography variant="caption" color="text.secondary" display="block">
        {label}
      </Typography>
      <Typography variant="body1" fontWeight={700} sx={{ color }}>
        {value}
      </Typography>
    </Box>
  );
}

function Section({
  icon,
  title,
  accentColor,
  sx = {},
  children,
}: {
  icon: React.ReactNode;
  title: string;
  accentColor?: string;
  sx?: object;
  children: React.ReactNode;
}) {
  return (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        background: alpha("#0d1b34", 0.5),
        border: "1px solid",
        borderColor: "divider",
        ...sx,
      }}
    >
      <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1.5 }}>
        <Box sx={{ color: accentColor ?? "text.secondary", display: "flex" }}>
          {icon}
        </Box>
        <Typography
          variant="overline"
          sx={{ color: accentColor ?? "text.secondary", lineHeight: 1 }}
        >
          {title}
        </Typography>
      </Box>
      {children}
    </Box>
  );
}

function PipelineTimeline({ loan }: { loan: ProcessedLoanRecord }) {
  const steps: Array<{
    label: string;
    detail: string;
    state: "done" | "warn" | "final";
  }> = [
    {
      label: "Intake Validation",
      detail:
        loan.action === "INTAKE_REJECTED"
          ? "Application failed intake checks"
          : "Application accepted for review",
      state: loan.action === "INTAKE_REJECTED" ? "warn" : "done",
    },
    {
      label: "Risk Assessment",
      detail: `Risk score calculated at ${loan.score}`,
      state: "done",
    },
    {
      label: "Compliance Review",
      detail: loan.compliant
        ? "No blocking compliance rules triggered"
        : `${loan.flags.length} compliance flag${loan.flags.length !== 1 ? "s" : ""} found`,
      state: loan.compliant ? "done" : "warn",
    },
    {
      label: "Routing Decision",
      detail:
        loan.action === "ESCALATE"
          ? "Routed to human escalation"
          : loan.action.replace(/_/g, " "),
      state: loan.action === "ESCALATE" ? "warn" : "done",
    },
  ];

  if (loan.escalation_id) {
    steps.push({
      label: "Human Review",
      detail: loan.human_decision
        ? `Reviewer decided ${loan.human_decision.replace(/_/g, " ")}`
        : "Awaiting human decision",
      state: loan.human_decision ? "done" : "warn",
    });
  }

  steps.push({
    label: "Final Outcome",
    detail: loan.decision.replace(/_/g, " "),
    state: "final",
  });

  return (
    <Section icon={<GavelIcon />} title="Pipeline Timeline" sx={{ mb: 2 }}>
      <Stack spacing={1.25}>
        {steps.map((step, index) => {
          const color =
            step.state === "final"
              ? "#3b82f6"
              : step.state === "warn"
                ? "#f59e0b"
                : "#10b981";

          return (
            <Box
              key={step.label}
              sx={{
                display: "grid",
                gridTemplateColumns: "22px 1fr",
                gap: 1.25,
                alignItems: "start",
              }}
            >
              <Box
                sx={{
                  mt: 0.5,
                  width: 10,
                  height: 10,
                  borderRadius: "50%",
                  bgcolor: color,
                  boxShadow: `0 0 0 4px ${alpha(color, 0.2)}`,
                }}
              />
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Step {index + 1}
                </Typography>
                <Typography variant="body2" fontWeight={700}>
                  {step.label}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {step.detail}
                </Typography>
              </Box>
            </Box>
          );
        })}
      </Stack>
    </Section>
  );
}

// ── Main page component ────────────────────────────────────────────────────

export function LoanDashboard() {
  const [loans, setLoans] = useState<ProcessedLoanRecord[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [filterDecision, setFilterDecision] = useState<string>("ALL");
  const [selectedLoan, setSelectedLoan] = useState<ProcessedLoanRecord | null>(
    null,
  );

  const refresh = useCallback(async () => {
    try {
      const [loansData, statsData] = await Promise.all([
        fetchLoans(),
        fetchStats(),
      ]);
      setLoans(loansData);
      setStats(statsData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, POLL_MS);
    return () => clearInterval(id);
  }, [refresh]);

  const filtered = loans.filter((l) => {
    const matchSearch =
      !search ||
      l.full_name.toLowerCase().includes(search.toLowerCase()) ||
      l.applicant_id.toLowerCase().includes(search.toLowerCase());
    const matchDecision =
      filterDecision === "ALL" || l.decision === filterDecision;
    return matchSearch && matchDecision;
  });

  return (
    <Box sx={{ p: { xs: 2, md: 3 }, maxWidth: 1400, mx: "auto" }}>
      {/* Page header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Box>
          <Typography variant="h4" fontWeight={700}>
            Loan Approval Dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            All applications processed through the multi-agent pipeline
          </Typography>
        </Box>
        <Tooltip title="Refresh">
          <IconButton onClick={refresh} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Tooltip>
      </Box>

      {error && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          {error} — Connect agents and run{" "}
          <code>python submit_test_batch.py</code>
        </Alert>
      )}

      {/* KPI cards */}
      {stats && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid size={{ xs: 6, sm: 4, md: 2 }}>
            <KpiCard
              label="Total Processed"
              value={stats.total}
              icon={<AccountBalanceIcon />}
              color="#3b82f6"
            />
          </Grid>
          <Grid size={{ xs: 6, sm: 4, md: 2 }}>
            <KpiCard
              label="Auto-Approved"
              value={stats.approved}
              icon={<CheckCircleIcon />}
              color="#10b981"
            />
          </Grid>
          <Grid size={{ xs: 6, sm: 4, md: 2 }}>
            <KpiCard
              label="Auto-Declined"
              value={stats.declined}
              icon={<CancelIcon />}
              color="#ef4444"
            />
          </Grid>
          <Grid size={{ xs: 6, sm: 4, md: 2 }}>
            <KpiCard
              label="Escalated"
              value={stats.escalated}
              icon={<GavelIcon />}
              color="#f59e0b"
              sublabel="Needs human review"
            />
          </Grid>
          <Grid size={{ xs: 6, sm: 4, md: 2 }}>
            <KpiCard
              label="Pending Review"
              value={stats.pending}
              icon={<HourglassEmptyIcon />}
              color="#8b5cf6"
            />
          </Grid>
          <Grid size={{ xs: 6, sm: 4, md: 2 }}>
            <KpiCard
              label="Human Approved"
              value={stats.human_approved}
              icon={<CheckCircleIcon />}
              color="#06b6d4"
              sublabel="After escalation"
            />
          </Grid>
        </Grid>
      )}

      {/* Filters row */}
      <Box sx={{ display: "flex", gap: 2, mb: 2, flexWrap: "wrap" }}>
        <TextField
          size="small"
          placeholder="Search by name or ID…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            },
          }}
          sx={{ minWidth: 240 }}
        />
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel>Decision</InputLabel>
          <Select
            value={filterDecision}
            label="Decision"
            onChange={(e) => setFilterDecision(e.target.value)}
          >
            <MenuItem value="ALL">All decisions</MenuItem>
            <MenuItem value="APPROVED">Approved</MenuItem>
            <MenuItem value="DECLINED">Declined</MenuItem>
            <MenuItem value="PENDING_REVIEW">Pending Review</MenuItem>
            <MenuItem value="REJECTED">Rejected</MenuItem>
          </Select>
        </FormControl>
        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ alignSelf: "center", ml: "auto" }}
        >
          {filtered.length} of {loans.length} loans
        </Typography>
      </Box>

      {/* Table */}
      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", py: 6 }}>
          <CircularProgress />
        </Box>
      ) : filtered.length === 0 ? (
        <Paper sx={{ p: 6, textAlign: "center" }}>
          <AccountBalanceIcon
            sx={{ fontSize: 48, color: "text.secondary", mb: 2 }}
          />
          <Typography variant="h6" color="text.secondary">
            No loan records yet
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Run <code>python submit_test_batch.py</code> to process test
            applications
          </Typography>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={refresh}
            sx={{ mt: 2 }}
          >
            Refresh
          </Button>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Applicant</TableCell>
                <TableCell>Decision</TableCell>
                <TableCell>Risk Score</TableCell>
                <TableCell>Action Taken</TableCell>
                <TableCell>Compliant</TableCell>
                <TableCell>Processed</TableCell>
                <TableCell>Human Review</TableCell>
                <TableCell align="right">Details</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filtered.map((loan) => (
                <TableRow
                  key={loan.id}
                  sx={{ cursor: "pointer" }}
                  onClick={() => setSelectedLoan(loan)}
                >
                  <TableCell>
                    <Box
                      sx={{ display: "flex", alignItems: "center", gap: 1.5 }}
                    >
                      <Avatar
                        sx={{
                          width: 32,
                          height: 32,
                          fontSize: "0.7rem",
                          bgcolor: alpha(
                            DECISION_COLORS[
                              loan.decision as keyof typeof DECISION_COLORS
                            ]?.main ?? "#6b7280",
                            0.2,
                          ),
                          color:
                            DECISION_COLORS[
                              loan.decision as keyof typeof DECISION_COLORS
                            ]?.text ?? "#9ca3af",
                        }}
                      >
                        {loan.full_name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")
                          .slice(0, 2)}
                      </Avatar>
                      <Box>
                        <Typography variant="body2" fontWeight={600}>
                          {loan.full_name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {loan.applicant_id}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <DecisionChip decision={loan.decision} />
                  </TableCell>
                  <TableCell>
                    <RiskGauge score={loan.score} />
                  </TableCell>
                  <TableCell>
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{
                        textTransform: "uppercase",
                        letterSpacing: "0.05em",
                      }}
                    >
                      {loan.action.replace(/_/g, " ")}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Box
                      sx={{ display: "flex", alignItems: "center", gap: 0.5 }}
                    >
                      {loan.compliant ? (
                        <>
                          <CheckCircleIcon
                            sx={{ fontSize: 16, color: "#10b981" }}
                          />
                          <Typography variant="caption" color="success.main">
                            Yes
                          </Typography>
                        </>
                      ) : (
                        <>
                          <CancelIcon sx={{ fontSize: 16, color: "#ef4444" }} />
                          <Typography variant="caption" color="error.main">
                            No
                          </Typography>
                        </>
                      )}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(loan.processed_at).toLocaleString(undefined, {
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    {loan.human_decision ? (
                      <DecisionChip decision={loan.human_decision} />
                    ) : loan.escalation_id ? (
                      <Chip
                        label="Pending"
                        size="small"
                        sx={{
                          background: alpha("#f59e0b", 0.1),
                          color: "#fbbf24",
                          fontSize: "0.65rem",
                        }}
                      />
                    ) : (
                      <Typography variant="caption" color="text.secondary">
                        —
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="View details">
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedLoan(loan);
                        }}
                      >
                        <OpenInNewIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Detail drawer */}
      <LoanDetailDrawer
        loan={selectedLoan}
        onClose={() => setSelectedLoan(null)}
      />
    </Box>
  );
}
