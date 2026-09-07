"""Offline mock email sender — logs only, never sends."""

from __future__ import annotations

from typing import Any

_SENT_LOG: list[dict[str, str]] = []


def send_email(*, to: str, subject: str, body: str) -> dict[str, Any]:
    """Record an email attempt locally. No SMTP / HTTP side effects."""
    record = {
        "to": str(to),
        "subject": str(subject),
        "body": str(body),
    }
    _SENT_LOG.append(record)
    return {
        "ok": True,
        "sent": False,
        "logged": True,
        "email": record,
        "note": "mock_send_email: logging only; no network",
    }


def clear_log() -> None:
    _SENT_LOG.clear()


def get_log() -> list[dict[str, str]]:
    return list(_SENT_LOG)
