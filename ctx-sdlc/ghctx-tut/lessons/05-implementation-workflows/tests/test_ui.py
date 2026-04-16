"""Lesson 05 — Playwright UI and API verification tests.

Validates that the notification-preference write hardening works end-to-end:
  - Backend health check
  - Notification preference read API
  - Write rule enforcement (mandatory-event, LEGAL-218)
  - Frontend preferences page renders correctly
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error

import pytest
from playwright.sync_api import sync_playwright, expect

BACKEND = "http://localhost:3100"
FRONTEND = "http://localhost:5173"
DEFAULT_LOAN_STATE = "NY"
RULE_REJECTION_STATUSES = {400, 422}


# ── Helper ──────────────────────────────────────────────────────────────────

def api_request(
    method: str,
    path: str,
    body: dict | None = None,
    user: str = "u-1",
) -> tuple[int, dict | list]:
    """Make an API request and return (status_code, parsed_body)."""
    url = f"{BACKEND}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Content-Type": "application/json",
            "x-user-id": user,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def preference_request(
    body: dict,
    user: str = "u-1",
) -> tuple[int, dict | list]:
    """Write a preference while tolerating variants that require direct loanState input."""
    if "/preferences" and "loanState" not in body:
        body = {**body, "loanState": DEFAULT_LOAN_STATE}
    return api_request("PUT", "/api/notifications/preferences", body, user=user)


def error_text(payload: dict | list) -> str:
    """Collapse variant backend error payloads into one comparable string."""
    if not isinstance(payload, dict):
        return ""
    parts = [
        str(payload.get("error", "")),
        str(payload.get("reason", "")),
        str(payload.get("message", "")),
    ]
    details = payload.get("details")
    if isinstance(details, list):
        parts.extend(str(item) for item in details)
    return " ".join(part for part in parts if part)


def assert_rule_rejection(status: int, payload: dict | list) -> None:
    """Accept equivalent business-rule rejection variants across implementations."""
    assert status in RULE_REJECTION_STATUSES
    assert error_text(payload)


# ── API Tests ───────────────────────────────────────────────────────────────

class TestHealthCheck:
    def test_health_endpoint(self) -> None:
        status, body = api_request("GET", "/health")
        assert status == 200
        assert body["status"] == "ok"


class TestNotificationPreferencesAPI:
    def test_get_preferences_for_user(self) -> None:
        status, body = api_request("GET", "/api/notifications/preferences/u-1")
        assert status == 200
        assert isinstance(body, list)
        assert len(body) > 0

    def test_set_preference_success(self) -> None:
        status, body = preference_request({
            "userId": "u-1",
            "event": "document-request",
            "channel": "email",
            "enabled": True,
        })
        assert status == 200
        assert body["event"] == "document-request"
        assert body["channel"] == "email"
        assert body["enabled"] is True

    def test_delegated_session_blocked(self) -> None:
        """Delegated sessions cannot modify preferences."""
        url = f"{BACKEND}/api/notifications/preferences"
        data = json.dumps({
            "userId": "u-2",
            "event": "approval",
            "channel": "email",
            "enabled": False,
            "loanState": DEFAULT_LOAN_STATE,
        }).encode()
        req = urllib.request.Request(
            url,
            data=data,
            method="PUT",
            headers={
                "Content-Type": "application/json",
                "x-user-id": "u-1",
                "x-delegated-for": "u-2",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                pytest.fail(f"Expected 403, got {resp.status}")
        except urllib.error.HTTPError as exc:
            assert exc.code == 403

    def test_compliance_reviewer_cannot_write(self) -> None:
        """Compliance reviewers are read-only for preferences."""
        status, body = preference_request({
            "userId": "u-3",
            "event": "approval",
            "channel": "email",
            "enabled": True,
        }, user="u-3")
        assert status == 403


class TestWriteRuleEnforcement:
    def test_mandatory_event_last_channel_blocked(self) -> None:
        """Cannot disable the last channel for manual-review-escalation."""
        # First ensure escalation has only one channel enabled (email)
        preference_request({
            "userId": "u-1",
            "event": "manual-review-escalation",
            "channel": "email",
            "enabled": True,
        })
        preference_request({
            "userId": "u-1",
            "event": "manual-review-escalation",
            "channel": "sms",
            "enabled": False,
        })
        # Now try to disable the last remaining channel
        status, body = preference_request({
            "userId": "u-1",
            "event": "manual-review-escalation",
            "channel": "email",
            "enabled": False,
        })
        assert_rule_rejection(status, body)
        assert "at least one" in error_text(body).lower()

    def test_legal_218_ca_decline_sms_blocked(self) -> None:
        """LEGAL-218: Cannot enable decline SMS for California loans."""
        status, body = preference_request({
            "userId": "u-1",
            "event": "decline",
            "channel": "sms",
            "enabled": True,
            "loanState": "CA",
        })
        assert_rule_rejection(status, body)
        assert "LEGAL-218" in error_text(body)

    def test_legal_218_california_spelled_out(self) -> None:
        """LEGAL-218 also matches 'California' (case-insensitive)."""
        status, body = preference_request({
            "userId": "u-1",
            "event": "decline",
            "channel": "sms",
            "enabled": True,
            "loanState": "California",
        })
        assert_rule_rejection(status, body)
        assert "LEGAL-218" in error_text(body)

    def test_decline_sms_allowed_outside_ca(self) -> None:
        """Decline SMS is allowed for non-CA states."""
        status, body = preference_request({
            "userId": "u-1",
            "event": "decline",
            "channel": "sms",
            "enabled": True,
            "loanState": "NY",
        })
        assert status == 200

    def test_false_positive_escalation_sms_disabled(self) -> None:
        """Disabling escalation SMS is allowed when email remains enabled."""
        # Ensure both channels enabled first
        preference_request({
            "userId": "u-1",
            "event": "manual-review-escalation",
            "channel": "email",
            "enabled": True,
        })
        preference_request({
            "userId": "u-1",
            "event": "manual-review-escalation",
            "channel": "sms",
            "enabled": True,
        })
        # Disabling SMS should succeed because email is still enabled
        status, body = preference_request({
            "userId": "u-1",
            "event": "manual-review-escalation",
            "channel": "sms",
            "enabled": False,
        })
        assert status == 200


# ── Frontend UI Tests ───────────────────────────────────────────────────────

class TestFrontendUI:
    def test_dashboard_loads(self) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(FRONTEND, wait_until="networkidle")
            assert page.title() != ""
            # Dashboard should have some content
            body_text = page.text_content("body") or ""
            assert len(body_text) > 0
            browser.close()

    def test_preferences_page_renders(self) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(FRONTEND, wait_until="networkidle")

            # Navigate to preferences (click nav link)
            prefs_link = page.locator("a[href*='preferences'], [data-page='preferences']")
            if prefs_link.count() > 0:
                prefs_link.first.click()
                page.wait_for_load_state("networkidle")

            # Check that preference toggles are rendered
            page.wait_for_selector(
                ".notification-toggle, .pref-list, .preferences-page",
                timeout=5000,
            )
            prefs_container = page.locator(
                ".notification-toggle, .pref-list, .preferences-page"
            )
            assert prefs_container.count() > 0
            browser.close()

    def test_preference_toggle_interaction(self) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            request_statuses: list[int] = []
            page.on(
                "response",
                lambda response: request_statuses.append(response.status)
                if "/api/notifications/preferences" in response.url
                and response.request.method == "PUT"
                else None,
            )
            page.goto(FRONTEND, wait_until="networkidle")

            # Navigate to preferences
            prefs_link = page.locator("a[href*='preferences'], [data-page='preferences']")
            if prefs_link.count() > 0:
                prefs_link.first.click()
                page.wait_for_load_state("networkidle")

            page.wait_for_selector(".toggle-input", timeout=5000)
            toggle = page.locator(
                "#toggle-document-request-email, #toggle-approval-email, #toggle-approval-sms"
            ).first
            expect(toggle).to_be_visible()

            initial_state = toggle.is_checked()
            toggle.click()
            page.wait_for_timeout(700)
            new_state = toggle.is_checked()

            # Accept two semantically valid outcomes across generated variants:
            # 1. backend accepts the write and the toggle flips
            # 2. backend rejects the stricter contract and the UI reverts cleanly
            if new_state == initial_state:
                assert any(status >= 400 for status in request_statuses), (
                    "Toggle reverted without an observed backend rejection."
                )
            else:
                assert any(status < 400 for status in request_statuses), (
                    "Toggle changed without an observed successful backend write."
                )

            browser.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
