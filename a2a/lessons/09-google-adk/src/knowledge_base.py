"""
Lesson 09 — Simulated threat intelligence knowledge base.

Provides two research tools that the ResearchAgent can call:
  - search_threat_intel : keyword search across CVEs and advisories
  - get_cve_detail      : detailed lookup by CVE-ID

All data is synthetic — no external API calls required.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ─── Data Model ──────────────────────────────────────────────────


@dataclass
class ThreatEntry:  # pylint: disable=too-many-instance-attributes
    """A single threat intelligence record."""

    cve_id: str
    title: str
    severity: str  # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    cvss_score: float
    affected_products: list[str] = field(default_factory=list)
    description: str = ""
    mitigation: str = ""
    references: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialise to plain dict."""
        return {
            "cve_id": self.cve_id,
            "title": self.title,
            "severity": self.severity,
            "cvss_score": self.cvss_score,
            "affected_products": self.affected_products,
            "description": self.description,
            "mitigation": self.mitigation,
            "references": self.references,
            "tags": self.tags,
        }


# ─── Synthetic Knowledge Base ────────────────────────────────────

THREAT_DB: list[ThreatEntry] = [
    ThreatEntry(
        cve_id="CVE-2024-3094",
        title="XZ Utils Backdoor (liblzma)",
        severity="CRITICAL",
        cvss_score=10.0,
        affected_products=[
            "xz-utils 5.6.0",
            "xz-utils 5.6.1",
            "liblzma 5.6.0-5.6.1",
        ],
        description=(
            "A supply-chain backdoor was inserted into xz-utils "
            "versions 5.6.0 and 5.6.1. The malicious code modifies "
            "the liblzma build process to inject a backdoor into "
            "the resulting library, which is linked by OpenSSH's "
            "sshd via systemd. This allows remote code execution "
            "by an attacker with a specific Ed448 key."
        ),
        mitigation=(
            "Downgrade xz-utils to 5.4.x immediately. Audit SSH "
            "access logs for anomalous connections. Rebuild from "
            "verified sources. Apply vendor patches as released."
        ),
        references=[
            "https://nvd.nist.gov/vuln/detail/CVE-2024-3094",
            "https://www.openwall.com/lists/oss-security/2024/03/29/4",
        ],
        tags=[
            "supply-chain",
            "backdoor",
            "ssh",
            "linux",
            "critical",
        ],
    ),
    ThreatEntry(
        cve_id="CVE-2024-4577",
        title="PHP CGI Argument Injection (Windows)",
        severity="CRITICAL",
        cvss_score=9.8,
        affected_products=[
            "PHP 8.1 < 8.1.29",
            "PHP 8.2 < 8.2.20",
            "PHP 8.3 < 8.3.8",
        ],
        description=(
            "On Windows systems running PHP in CGI mode, an "
            "attacker can exploit a character encoding mismatch "
            "(Best-Fit mapping) to inject arguments via crafted "
            "query strings, bypassing the CVE-2012-1823 fix. "
            "This leads to remote code execution."
        ),
        mitigation=(
            "Upgrade PHP to the patched version for your branch "
            "(8.1.29+, 8.2.20+, 8.3.8+). If using Apache, add "
            "RewriteRule to block query strings containing "
            "percent-encoded hyphens."
        ),
        references=[
            "https://nvd.nist.gov/vuln/detail/CVE-2024-4577",
            "https://www.php.net/ChangeLog-8.php",
        ],
        tags=[
            "rce",
            "php",
            "cgi",
            "windows",
            "critical",
        ],
    ),
    ThreatEntry(
        cve_id="CVE-2024-21762",
        title="Fortinet FortiOS Out-of-Bound Write",
        severity="CRITICAL",
        cvss_score=9.6,
        affected_products=[
            "FortiOS 7.4.0-7.4.2",
            "FortiOS 7.2.0-7.2.6",
            "FortiOS 7.0.0-7.0.13",
            "FortiOS 6.4.0-6.4.14",
        ],
        description=(
            "An out-of-bound write vulnerability in FortiOS "
            "SSL-VPN allows a remote unauthenticated attacker "
            "to execute arbitrary code via specially crafted "
            "HTTP requests. Actively exploited in the wild."
        ),
        mitigation=(
            "Upgrade FortiOS to 7.4.3+, 7.2.7+, 7.0.14+, or "
            "6.4.15+. Disable SSL-VPN as a temporary workaround. "
            "Monitor CISA KEV catalog for exploitation indicators."
        ),
        references=[
            "https://nvd.nist.gov/vuln/detail/CVE-2024-21762",
            "https://www.fortiguard.com/psirt/FG-IR-24-015",
        ],
        tags=[
            "vpn",
            "fortinet",
            "rce",
            "actively-exploited",
            "critical",
        ],
    ),
    ThreatEntry(
        cve_id="CVE-2024-6387",
        title="OpenSSH regreSSHion (Race Condition in sshd)",
        severity="HIGH",
        cvss_score=8.1,
        affected_products=[
            "OpenSSH 8.5p1-9.7p1",
            "glibc-based Linux distributions",
        ],
        description=(
            "A signal handler race condition in sshd allows "
            "unauthenticated remote code execution as root on "
            "glibc-based Linux systems. The vulnerability is a "
            "regression of CVE-2006-5051 reintroduced in "
            "OpenSSH 8.5p1. Exploitation requires ~10K attempts "
            "over several hours."
        ),
        mitigation=(
            "Upgrade OpenSSH to 9.8p1+. Set LoginGraceTime to 0 "
            "(prevents exploitation but enables DoS). Apply vendor "
            "patches. Monitor for brute-force SSH login patterns."
        ),
        references=[
            "https://nvd.nist.gov/vuln/detail/CVE-2024-6387",
            "https://www.qualys.com/2024/07/01/cve-2024-6387",
        ],
        tags=[
            "ssh",
            "race-condition",
            "rce",
            "linux",
            "high",
        ],
    ),
    ThreatEntry(
        cve_id="CVE-2024-38063",
        title="Windows TCP/IP IPv6 Remote Code Execution",
        severity="CRITICAL",
        cvss_score=9.8,
        affected_products=[
            "Windows 10 (all supported versions)",
            "Windows 11 (all supported versions)",
            "Windows Server 2016-2022",
        ],
        description=(
            "An integer underflow in the Windows TCP/IP stack "
            "allows remote code execution via specially crafted "
            "IPv6 packets. No user interaction or authentication "
            "required. The vulnerability is wormable."
        ),
        mitigation=(
            "Apply the August 2024 Patch Tuesday update "
            "(KB5041585 / KB5041592). As a temporary measure, "
            "disable IPv6 on interfaces that do not require it. "
            "Monitor network for anomalous IPv6 traffic patterns."
        ),
        references=[
            "https://nvd.nist.gov/vuln/detail/CVE-2024-38063",
            "https://msrc.microsoft.com/update-guide/CVE-2024-38063",
        ],
        tags=[
            "windows",
            "tcp-ip",
            "ipv6",
            "wormable",
            "rce",
            "critical",
        ],
    ),
]

CVE_INDEX: dict[str, ThreatEntry] = {t.cve_id: t for t in THREAT_DB}


# ─── Search Functions ────────────────────────────────────────────


def search_threat_intel(query: str) -> list[dict]:
    """Search the threat intelligence knowledge base.

    Match against CVE IDs, titles, descriptions, tags,
    and affected products.  Returns a list of matching
    entries as dicts.
    """
    q = query.lower()
    results = []
    for entry in THREAT_DB:
        searchable = " ".join(
            [
                entry.cve_id.lower(),
                entry.title.lower(),
                entry.description.lower(),
                " ".join(entry.tags),
                " ".join(p.lower() for p in entry.affected_products),
            ]
        )
        if q in searchable or any(word in searchable for word in q.split()):
            results.append(entry.to_dict())
    return results


def get_cve_detail(cve_id: str) -> dict | None:
    """Look up a specific CVE by its ID.

    Return the full entry dict or None if not found.
    """
    entry = CVE_INDEX.get(cve_id.upper())
    return entry.to_dict() if entry else None
