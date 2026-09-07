from __future__ import annotations

import urllib.request

from tools.mock_search_docs import search_docs
from tools.mock_send_email import clear_log, get_log, send_email


def test_search_docs_offline_match():
    docs = [{"doc_id": "a", "text": "Blue Line leaves at 22:40"}]
    out = search_docs(query="Blue Line", docs=docs)
    assert out["ok"] is True
    assert out["n_hits"] >= 1


def test_send_email_logs_only():
    clear_log()
    out = send_email(to="a@b.c", subject="s", body="body")
    assert out["ok"] is True
    assert out["sent"] is False
    assert out["logged"] is True
    assert get_log()[-1]["to"] == "a@b.c"


def test_tools_do_not_call_urlopen(monkeypatch):
    def boom(*_a, **_k):
        raise AssertionError("network forbidden")

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    search_docs(query="x", docs=[{"doc_id": "d", "text": "hello"}])
    send_email(to="t@e.st", subject="s", body="b")
