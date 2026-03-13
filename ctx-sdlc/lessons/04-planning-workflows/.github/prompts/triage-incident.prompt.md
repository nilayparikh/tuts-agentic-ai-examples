---
name: triage-incident
description: "Triage a production incident by checking NFR compliance, observability gaps, and blast radius"
agent: planner
tools:
  - search/codebase
  - read/problems
  - search/usages
  - read/readFile
argument-hint: "Describe the incident symptoms"
---

# Triage Incident

Incident report: ${input:incident:Describe the production incident symptoms}

## Triage Steps

1. Read [NFRs](../../specs/non-functional-requirements.md) — especially NFR-2 (resilience) and NFR-5 (observability).
2. Read [architecture](../../docs/architecture.md) — identify which services are in the blast radius.
3. Search `app/backend/src/services/` and `app/backend/src/middleware/` for error handling and fallback logic.
4. Check whether existing metrics (NFR-5 table) would surface this incident.

## Triage Requirements

- Determine if the incident violates an explicit NFR or reveals a gap in coverage.
- Identify whether fail-closed behavior is activating correctly or masking a deeper issue.
- Check whether observability metrics exist to diagnose this incident or if new metrics are needed.
- Distinguish between **user-facing impact** and **internal system impact**.

## Output Format

- **Severity assessment**: Based on user impact and NFR violations.
- **Likely root cause**: With evidence from code and specs.
- **Blast radius**: Which users, roles, and workflows are affected.
- **Immediate mitigation**: What can be done now to reduce impact.
- **Observability gaps**: Metrics or logs that should exist but don't.
- **Follow-up tasks**: Longer-term fixes with spec/NFR references.
