/**
 * EscalationQueue — Human-in-the-loop review queue.
 *
 * Shows all borderline loan applications awaiting a human decision.
 * Reviewers can approve, decline, or request more information.
 */

import { useCallback, useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Divider from "@mui/material/Divider";
import Stack from "@mui/material/Stack";
import IconButton from "@mui/material/IconButton";
import Collapse from "@mui/material/Collapse";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import LinearProgress from "@mui/material/LinearProgress";
import Tooltip from "@mui/material/Tooltip";
import Badge from "@mui/material/Badge";
import Avatar from "@mui/material/Avatar";
import Snackbar from "@mui/material/Snackbar";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import { alpha } from "@mui/material/styles";

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CancelIcon from "@mui/icons-material/Cancel";
import InfoIcon from "@mui/icons-material/Info";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import RefreshIcon from "@mui/icons-material/Refresh";
import GavelIcon from "@mui/icons-material/Gavel";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import SecurityIcon from "@mui/icons-material/Security";
import PersonIcon from "@mui/icons-material/Person";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import DoneAllIcon from "@mui/icons-material/DoneAll";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import CloseIcon from "@mui/icons-material/Close";
import AssignmentIcon from "@mui/icons-material/Assignment";

import { fetchAll, fetchPending, submitDecision } from "../api";
import type { Decision, EscalatedApplication } from "../types";
import { scoreColor, glass } from "../theme";

const POLL_MS = 3000;
const DRAWER_WIDTH = 580;

// ── Single escalation card ─────────────────────────────────────────────────

function EscalationCard({
  application,
  onDecision,
}: {
  application: EscalatedApplication;
  onDecision: (id: string, decision: Decision, notes: string) => Promise<void>;
}) {
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [expanded, setExpanded] = useState(true);

  const riskColor = scoreColor(application.risk_score);
  const initial = application.full_name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  const handleAction = async (decision: Decision) => {
    setSubmitting(true);
    try {
      await onDecision(application.id, decision, notes);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card
      sx={{
        ...glass,
        border: "1px solid",
        borderColor: alpha("#f59e0b", 0.25),
        position: "relative",
        overflow: "visible",
        "&::before": {
          content: '""',
          position: "absolute",
          inset: 0,
          borderRadius: "inherit",
          background: `linear-gradient(135deg, ${alpha("#f59e0b", 0.04)}, transparent 60%)`,
          pointerEvents: "none",
        },
      }}
    >
      {/* Colored left accent */}
      <Box
        sx={{
          position: "absolute",
          left: 0,
          top: 0,
          bottom: 0,
          width: 4,
          borderRadius: "12px 0 0 12px",
          background: `linear-gradient(180deg, #f59e0b, ${alpha("#f59e0b", 0.3)})`,
        }}
      />

      <CardContent sx={{ pl: 3 }}>
        {/* Header row */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            mb: 2,
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            <Avatar
              sx={{
                width: 48,
                height: 48,
                bgcolor: alpha("#f59e0b", 0.15),
                color: "#fbbf24",
                border: `2px solid ${alpha("#f59e0b", 0.3)}`,
                fontWeight: 700,
              }}
            >
              {initial}
            </Avatar>
            <Box>
              <Typography variant="h6" fontWeight={700}>
                {application.full_name}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {application.applicant_id} &bull; Escalated{" "}
                {new Date(application.escalated_at).toLocaleString(undefined, {
                  month: "short",
                  day: "numeric",
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </Typography>
            </Box>
          </Box>

          {/* Risk score badge */}
          <Box sx={{ textAlign: "right" }}>
            <Box
              sx={{
                display: "inline-flex",
                flexDirection: "column",
                alignItems: "center",
                px: 2,
                py: 1,
                borderRadius: 2,
                background: alpha(riskColor, 0.12),
                border: `1px solid ${alpha(riskColor, 0.3)}`,
              }}
            >
              <Typography
                variant="h4"
                fontWeight={800}
                sx={{ color: riskColor, lineHeight: 1 }}
              >
                {application.risk_score}
              </Typography>
              <Typography
                variant="caption"
                color="text.secondary"
                sx={{ fontSize: "0.6rem" }}
              >
                RISK SCORE
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Risk score bar */}
        <Box sx={{ mb: 2.5 }}>
          <LinearProgress
            variant="determinate"
            value={application.risk_score}
            sx={{
              height: 8,
              borderRadius: 4,
              bgcolor: alpha(riskColor, 0.12),
              "& .MuiLinearProgress-bar": {
                bgcolor: riskColor,
                borderRadius: 4,
              },
            }}
          />
          <Box
            sx={{ display: "flex", justifyContent: "space-between", mt: 0.5 }}
          >
            <Typography variant="caption" color="success.main">
              Low risk (auto-approve &le; 40)
            </Typography>
            <Typography variant="caption" color="error.main">
              High risk (auto-decline &ge; 80)
            </Typography>
          </Box>
        </Box>

        {/* AI reasoning */}
        <Box
          sx={{
            p: 2,
            borderRadius: 2,
            background: alpha("#3b82f6", 0.06),
            border: "1px solid",
            borderColor: alpha("#3b82f6", 0.15),
            mb: 2,
          }}
        >
          <Box
            sx={{ display: "flex", alignItems: "center", gap: 0.75, mb: 0.75 }}
          >
            <GavelIcon sx={{ fontSize: 14, color: "primary.light" }} />
            <Typography variant="overline" color="primary.light">
              AI Risk Assessment
            </Typography>
          </Box>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ lineHeight: 1.7 }}
          >
            {application.reasoning}
          </Typography>
        </Box>

        {/* Expand / collapse details */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            cursor: "pointer",
            mb: expanded ? 1.5 : 0,
          }}
          onClick={() => setExpanded(!expanded)}
        >
          <Typography variant="caption" color="primary.light" fontWeight={600}>
            {expanded ? "Hide" : "Show"} full details
          </Typography>
          <ExpandMoreIcon
            sx={{
              fontSize: 16,
              color: "primary.light",
              transform: expanded ? "rotate(180deg)" : "none",
              transition: "transform 0.2s",
              ml: 0.5,
            }}
          />
        </Box>

        <Collapse in={expanded}>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {/* Risk factors */}
            {application.risk_factors.length > 0 && (
              <Grid size={{ xs: 12, sm: 6 }}>
                <Box
                  sx={{
                    p: 1.5,
                    borderRadius: 2,
                    background: alpha("#ef4444", 0.06),
                    border: "1px solid",
                    borderColor: alpha("#ef4444", 0.15),
                    height: "100%",
                  }}
                >
                  <Typography
                    variant="overline"
                    color="error.light"
                    sx={{ mb: 1, display: "block" }}
                  >
                    Risk Factors
                  </Typography>
                  <Stack spacing={0.5}>
                    {application.risk_factors.map((f, i) => (
                      <Box
                        key={i}
                        sx={{
                          display: "flex",
                          gap: 0.75,
                          alignItems: "flex-start",
                        }}
                      >
                        <Box
                          sx={{
                            width: 5,
                            height: 5,
                            borderRadius: "50%",
                            bgcolor: "error.main",
                            mt: 0.8,
                            flexShrink: 0,
                          }}
                        />
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          fontSize="0.8rem"
                        >
                          {f}
                        </Typography>
                      </Box>
                    ))}
                  </Stack>
                </Box>
              </Grid>
            )}

            {/* Compensating factors */}
            {application.compensating_factors.length > 0 && (
              <Grid size={{ xs: 12, sm: 6 }}>
                <Box
                  sx={{
                    p: 1.5,
                    borderRadius: 2,
                    background: alpha("#10b981", 0.06),
                    border: "1px solid",
                    borderColor: alpha("#10b981", 0.15),
                    height: "100%",
                  }}
                >
                  <Typography
                    variant="overline"
                    color="success.light"
                    sx={{ mb: 1, display: "block" }}
                  >
                    Compensating Factors
                  </Typography>
                  <Stack spacing={0.5}>
                    {application.compensating_factors.map((f, i) => (
                      <Box
                        key={i}
                        sx={{
                          display: "flex",
                          gap: 0.75,
                          alignItems: "flex-start",
                        }}
                      >
                        <Box
                          sx={{
                            width: 5,
                            height: 5,
                            borderRadius: "50%",
                            bgcolor: "success.main",
                            mt: 0.8,
                            flexShrink: 0,
                          }}
                        />
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          fontSize="0.8rem"
                        >
                          {f}
                        </Typography>
                      </Box>
                    ))}
                  </Stack>
                </Box>
              </Grid>
            )}
          </Grid>

          {/* Compliance flags */}
          {application.compliance_flags.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Box
                sx={{ display: "flex", alignItems: "center", gap: 0.75, mb: 1 }}
              >
                <SecurityIcon sx={{ fontSize: 14, color: "text.secondary" }} />
                <Typography variant="overline" color="text.secondary">
                  Compliance Flags
                </Typography>
              </Box>
              <Stack spacing={1}>
                {application.compliance_flags.map((flag, i) => {
                  const flagColor =
                    flag.severity === "hard" ? "#ef4444" : "#f59e0b";
                  return (
                    <Box
                      key={i}
                      sx={{
                        p: 1.5,
                        borderRadius: 2,
                        background: alpha(flagColor, 0.06),
                        borderLeft: `3px solid ${flagColor}`,
                        display: "flex",
                        gap: 1.5,
                        alignItems: "flex-start",
                      }}
                    >
                      <Chip
                        label={flag.severity?.toUpperCase() ?? "FLAG"}
                        size="small"
                        sx={{
                          height: 18,
                          fontSize: "0.6rem",
                          bgcolor: alpha(flagColor, 0.15),
                          color: flagColor,
                          fontWeight: 700,
                          flexShrink: 0,
                        }}
                      />
                      <Box>
                        <Typography
                          variant="caption"
                          fontWeight={700}
                          display="block"
                        >
                          {flag.rule}
                        </Typography>
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          fontSize="0.8rem"
                        >
                          {flag.message}
                        </Typography>
                      </Box>
                    </Box>
                  );
                })}
              </Stack>
            </Box>
          )}

          {/* Application data */}
          <Box sx={{ mb: 2 }}>
            <Box
              sx={{ display: "flex", alignItems: "center", gap: 0.75, mb: 1 }}
            >
              <PersonIcon sx={{ fontSize: 14, color: "text.secondary" }} />
              <Typography variant="overline" color="text.secondary">
                Application Data
              </Typography>
            </Box>
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))",
                gap: 1,
              }}
            >
              {Object.entries(application.application_data)
                .filter(([, v]) => v !== null && v !== undefined)
                .map(([key, value]) => (
                  <Box
                    key={key}
                    sx={{
                      p: 1,
                      borderRadius: 1.5,
                      background: alpha("#6395ff", 0.05),
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
                        fontSize: "0.58rem",
                        letterSpacing: "0.06em",
                        mb: 0.25,
                      }}
                    >
                      {key.replace(/_/g, " ")}
                    </Typography>
                    <Typography
                      variant="body2"
                      fontWeight={600}
                      fontSize="0.82rem"
                    >
                      {typeof value === "number"
                        ? value.toLocaleString()
                        : String(value)}
                    </Typography>
                  </Box>
                ))}
            </Box>
          </Box>
        </Collapse>
      </CardContent>

      <Divider />

      {/* Review actions */}
      <CardActions
        sx={{
          p: 2,
          pl: 3,
          flexDirection: "column",
          gap: 1.5,
          alignItems: "stretch",
        }}
      >
        <TextField
          size="small"
          multiline
          rows={2}
          placeholder="Add review notes explaining your decision (optional)..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          fullWidth
          disabled={submitting}
        />
        <Box sx={{ display: "flex", gap: 1.5, flexWrap: "wrap" }}>
          <Button
            variant="contained"
            color="success"
            startIcon={
              submitting ? <CircularProgress size={14} /> : <CheckCircleIcon />
            }
            disabled={submitting}
            onClick={() => handleAction("APPROVED")}
            sx={{ flex: 1, minWidth: 120 }}
          >
            Approve
          </Button>
          <Button
            variant="contained"
            color="error"
            startIcon={
              submitting ? <CircularProgress size={14} /> : <CancelIcon />
            }
            disabled={submitting}
            onClick={() => handleAction("DECLINED")}
            sx={{ flex: 1, minWidth: 120 }}
          >
            Decline
          </Button>
          <Button
            variant="outlined"
            color="primary"
            startIcon={<InfoIcon />}
            disabled={submitting}
            onClick={() => handleAction("INFO_REQUESTED")}
            sx={{ flex: 1, minWidth: 140 }}
          >
            Request Info
          </Button>
        </Box>
      </CardActions>
    </Card>
  );
}

function DecisionStatusChip({
  status,
}: {
  status: EscalatedApplication["status"];
}) {
  const meta: Record<
    EscalatedApplication["status"],
    { color: string; label: string; icon: React.ReactElement }
  > = {
    PENDING: {
      color: "#f59e0b",
      label: "Pending",
      icon: <HourglassEmptyIcon sx={{ fontSize: 14 }} />,
    },
    APPROVED: {
      color: "#10b981",
      label: "Approved",
      icon: <CheckCircleIcon sx={{ fontSize: 14 }} />,
    },
    DECLINED: {
      color: "#ef4444",
      label: "Declined",
      icon: <CancelIcon sx={{ fontSize: 14 }} />,
    },
    INFO_REQUESTED: {
      color: "#3b82f6",
      label: "Info Requested",
      icon: <InfoIcon sx={{ fontSize: 14 }} />,
    },
  };

  const cfg = meta[status];

  return (
    <Chip
      size="small"
      icon={cfg.icon}
      label={cfg.label}
      sx={{
        background: alpha(cfg.color, 0.12),
        color: cfg.color,
        border: `1px solid ${alpha(cfg.color, 0.3)}`,
        "& .MuiChip-icon": { color: cfg.color },
        fontWeight: 700,
        letterSpacing: "0.04em",
        textTransform: "uppercase",
        fontSize: "0.65rem",
      }}
    />
  );
}

function ProcessedEscalationCard({
  application,
  onOpen,
}: {
  application: EscalatedApplication;
  onOpen: (app: EscalatedApplication) => void;
}) {
  const decidedAt = application.decided_at
    ? new Date(application.decided_at).toLocaleString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      })
    : "—";

  return (
    <Card sx={{ ...glass, border: "1px solid", borderColor: "divider" }}>
      <CardContent sx={{ pb: 1.5 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", gap: 2 }}>
          <Box>
            <Typography variant="subtitle1" fontWeight={700}>
              {application.full_name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {application.applicant_id}
            </Typography>
          </Box>
          <DecisionStatusChip status={application.status} />
        </Box>

        <Box
          sx={{
            mt: 1.5,
            display: "grid",
            gap: 1,
            gridTemplateColumns: { xs: "1fr 1fr", sm: "repeat(4, 1fr)" },
          }}
        >
          <MetaCell label="Risk" value={String(application.risk_score)} />
          <MetaCell label="Reviewed By" value={application.decided_by ?? "—"} />
          <MetaCell label="Reviewed At" value={decidedAt} />
          <MetaCell
            label="Escalated"
            value={new Date(application.escalated_at).toLocaleString(
              undefined,
              {
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              },
            )}
          />
        </Box>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ mt: 1.5, lineHeight: 1.6 }}
        >
          {application.decision_notes || application.reasoning}
        </Typography>
      </CardContent>
      <CardActions sx={{ px: 2, pb: 2 }}>
        <Button
          size="small"
          variant="outlined"
          startIcon={<OpenInNewIcon />}
          onClick={() => onOpen(application)}
        >
          View Detail
        </Button>
      </CardActions>
    </Card>
  );
}

function MetaCell({ label, value }: { label: string; value: string }) {
  return (
    <Box
      sx={{
        p: 1,
        borderRadius: 1.5,
        background: alpha("#6395ff", 0.05),
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
        }}
      >
        {label}
      </Typography>
      <Typography variant="body2" fontWeight={600} fontSize="0.78rem">
        {value}
      </Typography>
    </Box>
  );
}

function ProcessedDetailDrawer({
  application,
  onClose,
}: {
  application: EscalatedApplication | null;
  onClose: () => void;
}) {
  if (!application) return null;

  return (
    <Drawer
      anchor="right"
      open={Boolean(application)}
      onClose={onClose}
      sx={{
        "& .MuiDrawer-paper": {
          width: { xs: "100vw", sm: DRAWER_WIDTH },
          background: "transparent",
          boxShadow: "none",
        },
      }}
    >
      <Box
        sx={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
          ...glass,
          borderLeft: `1px solid ${alpha("#6395ff", 0.2)}`,
        }}
      >
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
            <Box sx={{ flex: 1 }}>
              <Typography variant="subtitle1" fontWeight={700}>
                {application.full_name}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {application.applicant_id}
              </Typography>
            </Box>
            <DecisionStatusChip status={application.status} />
            <IconButton size="small" onClick={onClose}>
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>

        <Box sx={{ p: 3, overflow: "auto" }}>
          <Box
            sx={{
              display: "grid",
              gap: 2,
              gridTemplateColumns: "1fr 1fr",
              mb: 2,
            }}
          >
            <MetaCell
              label="Risk Score"
              value={String(application.risk_score)}
            />
            <MetaCell label="Reviewer" value={application.decided_by ?? "—"} />
            <MetaCell
              label="Escalated At"
              value={new Date(application.escalated_at).toLocaleString()}
            />
            <MetaCell
              label="Decided At"
              value={
                application.decided_at
                  ? new Date(application.decided_at).toLocaleString()
                  : "—"
              }
            />
          </Box>

          <Box
            sx={{
              p: 2,
              borderRadius: 2,
              background: alpha("#3b82f6", 0.06),
              border: "1px solid",
              borderColor: alpha("#3b82f6", 0.15),
              mb: 2,
            }}
          >
            <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
              <AssignmentIcon sx={{ fontSize: 16, color: "primary.light" }} />
              <Typography variant="overline" color="primary.light">
                AI Reasoning
              </Typography>
            </Box>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ lineHeight: 1.7 }}
            >
              {application.reasoning}
            </Typography>
          </Box>

          {application.decision_notes && (
            <Box
              sx={{
                p: 2,
                borderRadius: 2,
                background: alpha("#10b981", 0.06),
                border: "1px solid",
                borderColor: alpha("#10b981", 0.15),
                mb: 2,
              }}
            >
              <Typography
                variant="overline"
                color="success.light"
                sx={{ display: "block", mb: 0.5 }}
              >
                Human Decision Notes
              </Typography>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ lineHeight: 1.7 }}
              >
                {application.decision_notes}
              </Typography>
            </Box>
          )}

          {application.compliance_flags.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography
                variant="overline"
                color="text.secondary"
                sx={{ display: "block", mb: 1 }}
              >
                Compliance Flags
              </Typography>
              <Stack spacing={1}>
                {application.compliance_flags.map((flag, index) => (
                  <Box
                    key={index}
                    sx={{
                      p: 1.5,
                      borderRadius: 2,
                      background: alpha(
                        flag.severity === "hard" ? "#ef4444" : "#f59e0b",
                        0.06,
                      ),
                      borderLeft: `3px solid ${flag.severity === "hard" ? "#ef4444" : "#f59e0b"}`,
                    }}
                  >
                    <Typography
                      variant="caption"
                      fontWeight={700}
                      display="block"
                    >
                      {flag.rule}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {flag.message}
                    </Typography>
                  </Box>
                ))}
              </Stack>
            </Box>
          )}

          <Typography variant="caption" color="text.secondary">
            Record ID: {application.id}
          </Typography>
        </Box>
      </Box>
    </Drawer>
  );
}

// ── Main page ──────────────────────────────────────────────────────────────

export function EscalationQueue() {
  const [pending, setPending] = useState<EscalatedApplication[]>([]);
  const [allEscalations, setAllEscalations] = useState<EscalatedApplication[]>(
    [],
  );
  const [selectedProcessed, setSelectedProcessed] =
    useState<EscalatedApplication | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<{ message: string; color: string } | null>(
    null,
  );

  const refresh = useCallback(async () => {
    try {
      const [pendingData, allData] = await Promise.all([
        fetchPending(),
        fetchAll(),
      ]);
      setPending(pendingData);
      setAllEscalations(allData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, POLL_MS);
    return () => clearInterval(id);
  }, [refresh]);

  const handleDecision = async (
    id: string,
    decision: Decision,
    notes: string,
  ) => {
    try {
      await submitDecision(id, decision, "Reviewer", notes);
      setPending((prev) => prev.filter((app) => app.id !== id));
      const labels: Record<Decision, string> = {
        APPROVED: "approved",
        DECLINED: "declined",
        INFO_REQUESTED: "marked for more info",
      };
      const colors: Record<Decision, string> = {
        APPROVED: "#10b981",
        DECLINED: "#ef4444",
        INFO_REQUESTED: "#3b82f6",
      };
      setToast({
        message: `Application ${labels[decision]}`,
        color: colors[decision],
      });
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to submit decision",
      );
    }
  };

  const processed = allEscalations
    .filter((app) => app.status !== "PENDING")
    .sort((a, b) => {
      const aTime = new Date(a.decided_at ?? a.escalated_at).getTime();
      const bTime = new Date(b.decided_at ?? b.escalated_at).getTime();
      return bTime - aTime;
    });

  return (
    <Box sx={{ p: { xs: 2, md: 3 }, maxWidth: 1400, mx: "auto" }}>
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Box>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
            <Typography variant="h4" fontWeight={700}>
              Escalation Queue
            </Typography>
            {!loading && pending.length > 0 && (
              <Badge badgeContent={pending.length} color="warning">
                <HourglassEmptyIcon sx={{ color: "#f59e0b" }} />
              </Badge>
            )}
          </Box>
          <Typography variant="body2" color="text.secondary">
            Borderline applications requiring human judgment
          </Typography>
        </Box>
        <Tooltip title="Refresh">
          <IconButton onClick={refresh} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Tooltip>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
          <CircularProgress />
        </Box>
      ) : pending.length === 0 ? (
        <Box
          sx={{
            ...glass,
            p: 8,
            borderRadius: 3,
            textAlign: "center",
            border: "1px solid",
            borderColor: "divider",
          }}
        >
          <DoneAllIcon
            sx={{ fontSize: 64, color: "success.main", mb: 2, opacity: 0.8 }}
          />
          <Typography
            variant="h5"
            fontWeight={700}
            color="success.main"
            gutterBottom
          >
            All caught up!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            No applications are currently pending human review.
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Submit a test batch with <code>python submit_test_batch.py</code> to
            generate escalations.
          </Typography>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={refresh}
            sx={{ mt: 3 }}
          >
            Check again
          </Button>
        </Box>
      ) : (
        <>
          {/* Context bar */}
          <Box
            sx={{
              p: 2,
              mb: 3,
              borderRadius: 2,
              background: alpha("#f59e0b", 0.08),
              border: "1px solid",
              borderColor: alpha("#f59e0b", 0.2),
              display: "flex",
              alignItems: "center",
              gap: 1.5,
            }}
          >
            <WarningAmberIcon sx={{ color: "#fbbf24" }} />
            <Box>
              <Typography
                variant="body2"
                fontWeight={600}
                color="warning.light"
              >
                {pending.length} application{pending.length !== 1 ? "s" : ""}{" "}
                awaiting your review
              </Typography>
              <Typography variant="caption" color="text.secondary">
                These applications have borderline risk scores and require a
                human decision. Review the AI assessment, risk factors, and
                compliance flags before deciding.
              </Typography>
            </Box>
          </Box>

          <Stack spacing={3}>
            {pending.map((app) => (
              <EscalationCard
                key={app.id}
                application={app}
                onDecision={handleDecision}
              />
            ))}
          </Stack>
        </>
      )}

      <Box sx={{ mt: 4 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 2,
          }}
        >
          <Box>
            <Typography variant="h5" fontWeight={700}>
              Processed Reviews
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Completed human decisions with reviewer notes and rationale
            </Typography>
          </Box>
          <Typography variant="caption" color="text.secondary">
            {processed.length} reviewed
          </Typography>
        </Box>

        {processed.length === 0 ? (
          <Box
            sx={{
              ...glass,
              p: 3,
              borderRadius: 2,
              border: "1px solid",
              borderColor: "divider",
            }}
          >
            <Typography variant="body2" color="text.secondary">
              No completed reviews yet. Once you approve/decline/request info,
              records appear here with full details.
            </Typography>
          </Box>
        ) : (
          <Stack spacing={2}>
            {processed.map((app) => (
              <ProcessedEscalationCard
                key={app.id}
                application={app}
                onOpen={setSelectedProcessed}
              />
            ))}
          </Stack>
        )}
      </Box>

      <ProcessedDetailDrawer
        application={selectedProcessed}
        onClose={() => setSelectedProcessed(null)}
      />

      {/* Success toast */}
      <Snackbar
        open={Boolean(toast)}
        autoHideDuration={3000}
        onClose={() => setToast(null)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          severity="success"
          onClose={() => setToast(null)}
          sx={{
            background: toast ? alpha(toast.color, 0.15) : undefined,
            border: "1px solid",
            borderColor: toast ? alpha(toast.color, 0.3) : undefined,
            color: toast?.color,
          }}
        >
          {toast?.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
