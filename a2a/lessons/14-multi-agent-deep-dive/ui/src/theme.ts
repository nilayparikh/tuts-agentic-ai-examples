/**
 * MUI dark glass-morphism theme for the Loan Approval Dashboard.
 */

import { alpha, createTheme } from "@mui/material/styles";

// ── Color palette ──────────────────────────────────────────────────────────
const navy = {
  950: "#020814",
  900: "#050d1a",
  800: "#0a1628",
  700: "#0f2040",
  600: "#162c58",
  500: "#1e3a70",
};

const blue = "#3b82f6";
const blueLight = "#60a5fa";
const purple = "#8b5cf6";

// ── Glass surface mixin ────────────────────────────────────────────────────
export const glass = {
  background: alpha("#0d1b34", 0.75),
  backdropFilter: "blur(20px) saturate(180%)",
  WebkitBackdropFilter: "blur(20px) saturate(180%)",
  border: `1px solid ${alpha("#6395ff", 0.18)}`,
};

export const glassLight = {
  background: alpha("#1a2f5a", 0.5),
  backdropFilter: "blur(12px)",
  WebkitBackdropFilter: "blur(12px)",
  border: `1px solid ${alpha("#6395ff", 0.12)}`,
};

// ── Theme ──────────────────────────────────────────────────────────────────
export const theme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: blue,
      light: blueLight,
      dark: "#2563eb",
    },
    secondary: {
      main: purple,
      light: "#a78bfa",
      dark: "#7c3aed",
    },
    success: {
      main: "#10b981",
      light: "#34d399",
      dark: "#059669",
    },
    warning: {
      main: "#f59e0b",
      light: "#fbbf24",
      dark: "#d97706",
    },
    error: {
      main: "#ef4444",
      light: "#f87171",
      dark: "#dc2626",
    },
    background: {
      default: navy[950],
      paper: alpha("#0d1b34", 0.8),
    },
    text: {
      primary: "#e2e8f0",
      secondary: "#94a3b8",
    },
    divider: alpha("#6395ff", 0.12),
  },

  typography: {
    fontFamily: '"Inter", "Segoe UI", system-ui, -apple-system, sans-serif',
    h1: { fontWeight: 700, letterSpacing: "-0.025em" },
    h2: { fontWeight: 700, letterSpacing: "-0.02em" },
    h3: { fontWeight: 600, letterSpacing: "-0.015em" },
    h4: { fontWeight: 600 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    overline: { letterSpacing: "0.12em", fontWeight: 600 },
  },

  shape: { borderRadius: 12 },

  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          background: `linear-gradient(135deg, ${navy[950]} 0%, ${navy[800]} 50%, #0a0f2e 100%)`,
          minHeight: "100vh",
          backgroundAttachment: "fixed",
        },
        "*::-webkit-scrollbar": { width: 6, height: 6 },
        "*::-webkit-scrollbar-track": {
          background: alpha("#6395ff", 0.05),
        },
        "*::-webkit-scrollbar-thumb": {
          background: alpha("#6395ff", 0.25),
          borderRadius: 3,
        },
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          ...glass,
          backgroundImage: "none",
        },
      },
    },

    MuiCard: {
      styleOverrides: {
        root: {
          ...glass,
          backgroundImage: "none",
          transition: "transform 0.2s ease, box-shadow 0.2s ease",
          "&:hover": {
            transform: "translateY(-2px)",
            boxShadow: `0 8px 32px ${alpha(blue, 0.2)}`,
          },
        },
      },
    },

    MuiAppBar: {
      styleOverrides: {
        root: {
          background: alpha(navy[900], 0.85),
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          borderBottom: `1px solid ${alpha("#6395ff", 0.15)}`,
          boxShadow: "none",
        },
      },
    },

    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: alpha(navy[800], 0.95),
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          borderRight: `1px solid ${alpha("#6395ff", 0.15)}`,
        },
      },
    },

    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 10,
          margin: "2px 8px",
          "&.Mui-selected": {
            background: alpha(blue, 0.15),
            borderLeft: `3px solid ${blue}`,
            "&:hover": { background: alpha(blue, 0.2) },
          },
          "&:hover": { background: alpha("#6395ff", 0.1) },
        },
      },
    },

    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: 600,
          borderRadius: 8,
        },
        contained: {
          boxShadow: "none",
          "&:hover": { boxShadow: `0 4px 20px ${alpha(blue, 0.35)}` },
        },
      },
    },

    MuiChip: {
      styleOverrides: {
        root: { fontWeight: 600, fontSize: "0.72rem" },
      },
    },

    MuiTableRow: {
      styleOverrides: {
        root: {
          "&:hover td": { background: alpha("#6395ff", 0.06) },
        },
      },
    },

    MuiTableCell: {
      styleOverrides: {
        head: {
          color: "#94a3b8",
          fontWeight: 700,
          fontSize: "0.7rem",
          textTransform: "uppercase",
          letterSpacing: "0.08em",
          borderBottom: `1px solid ${alpha("#6395ff", 0.15)}`,
          background: alpha("#0d1b34", 0.5),
        },
        body: {
          borderBottom: `1px solid ${alpha("#6395ff", 0.08)}`,
        },
      },
    },

    MuiTooltip: {
      styleOverrides: {
        tooltip: {
          ...glassLight,
          fontSize: "0.78rem",
        },
      },
    },

    MuiDialog: {
      styleOverrides: {
        paper: {
          background: alpha(navy[800], 0.97),
          backdropFilter: "blur(24px)",
          border: `1px solid ${alpha("#6395ff", 0.2)}`,
        },
      },
    },

    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            "& fieldset": {
              borderColor: alpha("#6395ff", 0.2),
            },
            "&:hover fieldset": {
              borderColor: alpha("#6395ff", 0.4),
            },
          },
        },
      },
    },
  },
});

/** Gradient accent colors for decision badges */
export const DECISION_COLORS = {
  APPROVED: { main: "#10b981", bg: alpha("#10b981", 0.15), text: "#34d399" },
  DECLINED: { main: "#ef4444", bg: alpha("#ef4444", 0.15), text: "#f87171" },
  PENDING_REVIEW: {
    main: "#f59e0b",
    bg: alpha("#f59e0b", 0.15),
    text: "#fbbf24",
  },
  INFO_REQUESTED: {
    main: "#3b82f6",
    bg: alpha("#3b82f6", 0.15),
    text: "#60a5fa",
  },
  REJECTED: { main: "#6b7280", bg: alpha("#6b7280", 0.15), text: "#9ca3af" },
  PENDING: { main: "#f59e0b", bg: alpha("#f59e0b", 0.15), text: "#fbbf24" },
} as const;

/** Map risk score to color */
export function scoreColor(score: number): string {
  if (score <= 40) return "#10b981";
  if (score <= 65) return "#f59e0b";
  return "#ef4444";
}
