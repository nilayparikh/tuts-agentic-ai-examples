// ---------------------------------------------------------------------------
// Status Badge Component
// ---------------------------------------------------------------------------
// Returns an HTML string for an application status badge with color coding.
// ---------------------------------------------------------------------------

const STATUS_COLORS: Record<string, string> = {
  intake: "badge-gray",
  review: "badge-blue",
  underwriting: "badge-yellow",
  decision: "badge-orange",
  finalized: "badge-green",
};

export function renderStatusBadge(status: string): string {
  const colorClass = STATUS_COLORS[status] ?? "badge-gray";
  return `<span class="status-badge ${colorClass}">${status}</span>`;
}
