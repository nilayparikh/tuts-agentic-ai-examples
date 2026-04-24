"""Deterministic scoring for prompt evolution response drafts."""

from __future__ import annotations

from dataclasses import dataclass

from prompt_evolution.config import PreferenceOption, SelectionProfile


@dataclass(frozen=True)
class EvaluationResult:
    """Scoring summary for one candidate support reply."""

    total_score: int
    max_score: int
    issues: list[str]
    strengths: list[str]


def _contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    """Return whether any configured phrase appears in the normalized text."""
    return any(phrase.lower() in text for phrase in phrases)


def _bullet_line_count(text: str) -> int:
    """Count the obvious bullet-like lines in the response text."""
    prefixes = ("- ", "* ", "1. ", "2. ", "3. ")
    return sum(1 for line in text.splitlines() if line.lstrip().startswith(prefixes))


def _has_short_paragraphs(text: str) -> bool:
    """Treat blank-line-separated short paragraphs as a structure match."""
    paragraphs = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    if len(paragraphs) < 2:
        return False
    return all(len(paragraph.split(".")) <= 4 for paragraph in paragraphs)


def _matches_tone(option_slug: str, text: str) -> bool:
    """Score the requested tone using lightweight phrase heuristics."""
    markers = {
        "warm": ("sorry", "thanks for flagging", "happy to help", "i understand"),
        "direct": ("here's what", "next step", "please", "we can"),
        "calm": ("we can sort this out", "let's get this resolved", "i'll help"),
    }
    return _contains_any(text, markers.get(option_slug, ()))


def _matches_structure(option_slug: str, raw_text: str) -> bool:
    """Score the requested structure using plain-text layout checks."""
    if option_slug == "bullets":
        return _bullet_line_count(raw_text) >= 2
    if option_slug == "checklist":
        return "[ ]" in raw_text or "- [ ]" in raw_text
    if option_slug == "short_paragraphs":
        return _has_short_paragraphs(raw_text)
    return True


def _matches_initiative(option_slug: str, text: str) -> bool:
    """Score how proactive the response is."""
    markers = {
        "next_step": ("next step", "please reply", "head to", "bring"),
        "options_first": ("option 1", "option 2", "you can either"),
        "handoff_ready": ("escalate", "hand this to", "membership lead", "duty manager"),
    }
    return _contains_any(text, markers.get(option_slug, ()))


def _matches_detail(option_slug: str, raw_text: str) -> bool:
    """Score detail level using rough word-count bands."""
    word_count = len(raw_text.split())
    if option_slug == "concise":
        return word_count <= 120
    if option_slug == "balanced":
        return 70 <= word_count <= 220
    if option_slug == "detailed":
        return word_count >= 150
    return True


def _matches_generic_option(option: PreferenceOption, text: str) -> bool:
    """Score non-special preference axes by matching their shipped signal phrases."""
    if not option.signals:
        return True
    return _contains_any(text, option.signals)


def evaluate_response(profile: SelectionProfile, response_text: str) -> EvaluationResult:
    """Score a candidate response against policies and selected preferences."""
    normalized = response_text.lower()
    total_score = 0
    max_score = 0
    issues: list[str] = []
    strengths: list[str] = []

    for policy in profile.context.required_policy_points:
        max_score += 2
        if _contains_any(normalized, policy.keywords):
            total_score += 2
            strengths.append(f"Policy covered: {policy.description}")
        else:
            issues.append(f"Missing policy coverage: {policy.description}")

    max_score += 1
    if _contains_any(normalized, profile.context.reference_terms):
        total_score += 1
        strengths.append("Grounds the reply in the selected service context.")
    else:
        issues.append("Missing context grounding from the selected service pack.")

    for claim in profile.context.forbidden_claims:
        if claim.lower() in normalized:
            issues.append(f"Forbidden policy promise detected: {claim}")
            total_score = max(total_score - 1, 0)

    for axis_slug, option_slug in profile.selected_preferences.items():
        max_score += 1
        if axis_slug == "tone":
            matched = _matches_tone(option_slug, normalized)
        elif axis_slug == "structure":
            matched = _matches_structure(option_slug, response_text)
        elif axis_slug == "initiative":
            matched = _matches_initiative(option_slug, normalized)
        elif axis_slug == "detail":
            matched = _matches_detail(option_slug, response_text)
        else:
            option = profile.resolved_preferences.get(axis_slug)
            matched = _matches_generic_option(option, normalized) if option else True

        if matched:
            strengths.append(f"{axis_slug.replace('_', ' ').title()} matches '{option_slug}'.")
            total_score += 1
        elif axis_slug == "structure":
            issues.append(
                f"Structure mismatch for '{option_slug}' bullet or layout preference."
            )
        elif axis_slug == "detail":
            issues.append(f"Detail level mismatch for '{option_slug}'.")
        else:
            issues.append(
                f"{axis_slug.replace('_', ' ').title()} mismatch for '{option_slug}'."
            )

    return EvaluationResult(
        total_score=total_score,
        max_score=max_score,
        issues=issues,
        strengths=strengths,
    )
