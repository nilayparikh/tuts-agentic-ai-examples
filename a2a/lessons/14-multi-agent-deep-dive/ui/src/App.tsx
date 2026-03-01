import { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  useNavigate,
  useLocation,
} from "react-router-dom";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import Chip from "@mui/material/Chip";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import DashboardIcon from "@mui/icons-material/Dashboard";
import GavelIcon from "@mui/icons-material/Gavel";
import TimelineIcon from "@mui/icons-material/Timeline";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import { alpha } from "@mui/material/styles";

import { LoanDashboard } from "./pages/LoanDashboard";
import { EscalationQueue } from "./pages/EscalationQueue";
import { Telemetry } from "./pages/Telemetry";

const DRAWER_WIDTH = 240;

interface NavItem {
  label: string;
  path: string;
  icon: React.ReactNode;
}

const NAV_ITEMS: NavItem[] = [
  { label: "Loan Dashboard", path: "/", icon: <DashboardIcon /> },
  { label: "Escalation Queue", path: "/escalations", icon: <GavelIcon /> },
  { label: "Telemetry", path: "/telemetry", icon: <TimelineIcon /> },
];

function SideNav({ onClose }: { open: boolean; onClose: () => void }) {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        display: { xs: "none", md: "flex" },
        "& .MuiDrawer-paper": {
          width: DRAWER_WIDTH,
          boxSizing: "border-box",
          pt: 1,
        },
      }}
    >
      {/* Logo */}
      <Box
        sx={{ px: 2.5, py: 2, display: "flex", alignItems: "center", gap: 1.5 }}
      >
        <AccountBalanceIcon sx={{ color: "primary.main", fontSize: 28 }} />
        <Box>
          <Typography variant="subtitle1" fontWeight={700} lineHeight={1.2}>
            LoanAI
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Multi-Agent Pipeline
          </Typography>
        </Box>
      </Box>

      <Divider sx={{ mx: 2, mb: 1 }} />

      <List sx={{ px: 1 }}>
        {NAV_ITEMS.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <ListItemButton
              key={item.path}
              selected={isActive}
              onClick={() => {
                navigate(item.path);
                onClose();
              }}
              sx={{ mb: 0.5 }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 36,
                  color: isActive ? "primary.light" : "text.secondary",
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.label}
                slotProps={{
                  primary: {
                    fontSize: "0.875rem",
                    fontWeight: isActive ? 600 : 400,
                    color: isActive ? "primary.light" : "text.primary",
                  },
                }}
              />
            </ListItemButton>
          );
        })}
      </List>

      <Box sx={{ flex: 1 }} />

      <Box
        sx={{
          p: 2,
          m: 2,
          borderRadius: 2,
          background: (t) => alpha(t.palette.primary.main, 0.08),
          border: "1px solid",
          borderColor: (t) => alpha(t.palette.primary.main, 0.15),
        }}
      >
        <Typography variant="caption" color="text.secondary" display="block">
          A2A Protocol
        </Typography>
        <Typography variant="caption" color="primary.light" fontWeight={600}>
          5 agents active
        </Typography>
      </Box>
    </Drawer>
  );
}

function TopBar({ onMenuClick }: { onMenuClick: () => void }) {
  const location = useLocation();
  const currentNav = NAV_ITEMS.find((n) => n.path === location.pathname);

  return (
    <AppBar
      position="fixed"
      sx={{ zIndex: (t) => t.zIndex.drawer + 1, display: { md: "none" } }}
    >
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          onClick={onMenuClick}
          sx={{ mr: 1 }}
        >
          <MenuIcon />
        </IconButton>
        <AccountBalanceIcon sx={{ mr: 1.5, color: "primary.light" }} />
        <Typography variant="h6" fontWeight={700} sx={{ flex: 1 }}>
          LoanAI
        </Typography>
        {currentNav && (
          <Chip
            label={currentNav.label}
            size="small"
            color="primary"
            variant="outlined"
          />
        )}
      </Toolbar>
    </AppBar>
  );
}

function Layout() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      {/* Desktop nav */}
      <SideNav open={mobileOpen} onClose={() => setMobileOpen(false)} />

      {/* Mobile nav */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
        sx={{ display: { xs: "block", md: "none" } }}
        ModalProps={{ keepMounted: true }}
      >
        <SideNav open={mobileOpen} onClose={() => setMobileOpen(false)} />
      </Drawer>

      {/* Mobile AppBar */}
      <TopBar onMenuClick={() => setMobileOpen(true)} />

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          minHeight: "100vh",
          pt: { xs: 8, md: 0 },
          overflow: "auto",
        }}
      >
        <Routes>
          <Route path="/" element={<LoanDashboard />} />
          <Route path="/escalations" element={<EscalationQueue />} />
          <Route path="/telemetry" element={<Telemetry />} />
        </Routes>
      </Box>
    </Box>
  );
}

export function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}
