"""
Lesson 09 — Threat-Intel Research Agent (Google ADK + Kimi-K2).

Build an LlmAgent with Google Agent Development Kit that:
  1. Searches a local threat knowledge base (``knowledge_base.py``)
  2. Retrieves detailed CVE records
  3. Synthesises structured threat-intelligence briefings

The agent runs on Azure-hosted Kimi-K2 via **LiteLlm** (no Vertex AI
or Google Cloud dependency).

Required env vars (loaded from ``_examples/.env``):
    AZURE_OPENAI_ENDPOINT          – Azure OpenAI resource URL
    AZURE_AI_API_KEY               – API key for the resource
    AZURE_AI_MODEL_DEPLOYMENT_NAME – e.g. ``Kimi-K2``
"""

from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool

from knowledge_base import get_cve_detail, search_threat_intel


# ─── Tool wrappers ───────────────────────────────────────────────
# Google ADK discovers param names / docstrings automatically.


def search_threats(query: str) -> str:
    """Search the threat-intelligence knowledge base.

    Accept a keyword, CVE ID fragment, product name, or tag and
    return matching records as a formatted string.
    """
    results = search_threat_intel(query)
    if not results:
        return "No matching threat records found."
    lines: list[str] = []
    for rec in results:
        lines.append(
            f"- {rec['cve_id']}  ({rec['severity']} / "
            f"CVSS {rec['cvss_score']})  {rec['title']}"
        )
    return "\n".join(lines)


def lookup_cve(cve_id: str) -> str:
    """Retrieve full details for one CVE identifier.

    Return a detailed record including description,
    affected products, mitigation, and references.
    """
    rec = get_cve_detail(cve_id)
    if rec is None:
        return f"CVE {cve_id} not found in the knowledge base."
    parts = [
        f"CVE:       {rec['cve_id']}",
        f"Title:     {rec['title']}",
        f"Severity:  {rec['severity']}  (CVSS {rec['cvss_score']})",
        f"Products:  {', '.join(rec['affected_products'])}",
        f"Description:\n  {rec['description']}",
        f"Mitigation:\n  {rec['mitigation']}",
        "References:\n  " + "\n  ".join(rec["references"]),
        f"Tags: {', '.join(rec['tags'])}",
    ]
    return "\n".join(parts)


# ─── LLM Configuration ──────────────────────────────────────────

_SYSTEM_INSTRUCTION = """\
You are **ThreatBriefing**, a cybersecurity threat-intelligence analyst.

## Behaviour
1. When the user provides a topic, product name, or CVE ID, use the
   **search_threats** tool to find relevant records.
2. For any CVE that looks important, call **lookup_cve** to get full
   details.
3. Synthesise the results into a structured **Threat Briefing**:
   - Executive Summary (2-3 sentences)
   - Affected Assets (list of products / versions)
   - Risk Rating (CRITICAL / HIGH / MEDIUM / LOW with CVSS range)
   - Recommended Actions (numbered steps)
   - References (URLs)
4. If no records match, say so clearly and offer to broaden the search.
5. Be concise, factual, and professional — no speculation.
"""


def _azure_model_string() -> str:
    """Build the ``azure/<deployment>`` model string for LiteLlm."""
    deployment = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2")
    return f"azure/{deployment}"


def _configure_litellm_env() -> None:
    """Map project env vars to the names that litellm expects.

    Our .env uses ``AZURE_OPENAI_ENDPOINT`` and ``AZURE_AI_API_KEY``,
    but litellm reads ``AZURE_API_BASE`` and ``AZURE_API_KEY``.
    """
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.environ.get("AZURE_AI_API_KEY", "")

    if endpoint:
        os.environ.setdefault("AZURE_API_BASE", endpoint)
    if api_key:
        os.environ.setdefault("AZURE_API_KEY", api_key)

    # litellm also wants an API-version for Azure
    os.environ.setdefault("AZURE_API_VERSION", "2025-04-01-preview")


def build_research_agent() -> LlmAgent:
    """Construct and return the ThreatBriefing LlmAgent.

    Call this **after** loading ``.env`` so the Azure credentials
    are available in ``os.environ``.
    """
    _configure_litellm_env()

    model = LiteLlm(model=_azure_model_string())

    agent = LlmAgent(
        name="ThreatBriefingAgent",
        description=(
            "Cybersecurity threat-intelligence analyst. Searches a "
            "curated vulnerability knowledge base and produces "
            "structured threat briefings with risk ratings and "
            "remediation steps."
        ),
        model=model,
        instruction=_SYSTEM_INSTRUCTION,
        tools=[
            FunctionTool(func=search_threats),
            FunctionTool(func=lookup_cve),
        ],
    )
    return agent
