"""Dashboard metric calculations for Skill Mastery.

Mirrors `cleanloop/dashboard_metrics.py` and `prompt_evolution/dashboard_metrics.py`.
Computes the summary numbers that the dashboard surface displays without
coupling them to Streamlit rendering. Tests can call these helpers directly to
assert that the metrics remain stable as the loop evolves.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any

from skill_mastery.dashboard_artifacts import DashboardArtifacts


@dataclass(frozen=True)
class SessionMetrics:
    """Headline metrics for one Skill Mastery session."""

    rounds_total: int
    best_round: int | None
    best_score: int | None
    best_total: int | None
    average_score_ratio: float
    llm_request_count: int
    mutation_round_count: int


@dataclass(frozen=True)
class IssueDistribution:
    """Distribution of evaluator issues across rounds."""

    rounds_with_issues: int
    rounds_clean: int
    most_common_issue: str | None
    issue_counts: dict[str, int]


def _ratio(score: Any, total: Any) -> float:
    """Return a safe score ratio for metric aggregation."""
    try:
        score_value = float(score)
        total_value = float(total)
    except (TypeError, ValueError):
        return 0.0
    if total_value <= 0:
        return 0.0
    return score_value / total_value


def compute_session_metrics(artifacts: DashboardArtifacts) -> SessionMetrics:
    """Return the headline metrics for the loaded session."""
    if artifacts.session is None:
        return SessionMetrics(
            rounds_total=0,
            best_round=None,
            best_score=None,
            best_total=None,
            average_score_ratio=0.0,
            llm_request_count=len(artifacts.llm_requests),
            mutation_round_count=0,
        )
    rounds = artifacts.session.get("rounds", []) or []
    if not isinstance(rounds, list):
        rounds = []
    best_round_number = artifacts.session.get("best_round")
    best_record: dict[str, Any] | None = None
    if isinstance(best_round_number, int):
        for entry in rounds:
            if isinstance(entry, dict) and entry.get("round") == best_round_number:
                best_record = entry
                break
    if best_record is None and rounds:
        dict_rounds = [entry for entry in rounds if isinstance(entry, dict)]
        if dict_rounds:
            best_record = max(
                dict_rounds,
                key=lambda item: (
                    int(item.get("score", 0)),
                    int(item.get("round", 0)),
                ),
            )
    average = (
        mean(
            _ratio(entry.get("score"), entry.get("total"))
            for entry in rounds
            if isinstance(entry, dict)
        )
        if rounds
        else 0.0
    )
    mutation_rounds = sum(
        1 for entry in rounds if isinstance(entry, dict) and entry.get("mutation_diff")
    )
    return SessionMetrics(
        rounds_total=len(rounds),
        best_round=best_record.get("round") if best_record else None,
        best_score=best_record.get("score") if best_record else None,
        best_total=best_record.get("total") if best_record else None,
        average_score_ratio=average,
        llm_request_count=len(artifacts.llm_requests),
        mutation_round_count=mutation_rounds,
    )


def compute_issue_distribution(artifacts: DashboardArtifacts) -> IssueDistribution:
    """Return how often each evaluator issue appeared across rounds."""
    counts: dict[str, int] = {}
    rounds_with_issues = 0
    rounds_clean = 0
    if artifacts.session is None:
        return IssueDistribution(
            rounds_with_issues=0,
            rounds_clean=0,
            most_common_issue=None,
            issue_counts=counts,
        )
    rounds = artifacts.session.get("rounds", []) or []
    if not isinstance(rounds, list):
        rounds = []
    for entry in rounds:
        if not isinstance(entry, dict):
            continue
        issues = entry.get("issues", [])
        if not isinstance(issues, list) or not issues:
            rounds_clean += 1
            continue
        rounds_with_issues += 1
        for issue in issues:
            key = str(issue)
            counts[key] = counts.get(key, 0) + 1
    most_common: str | None = None
    if counts:
        most_common = max(counts.items(), key=lambda item: item[1])[0]
    return IssueDistribution(
        rounds_with_issues=rounds_with_issues,
        rounds_clean=rounds_clean,
        most_common_issue=most_common,
        issue_counts=counts,
    )
