"""Offline mock document search — no network."""

from __future__ import annotations

from typing import Any


def search_docs(*, query: str, docs: list[dict[str, str]] | None = None) -> dict[str, Any]:
    """Return documents whose text or id loosely matches the query tokens."""
    docs = docs or []
    q = (query or "").strip().lower()
    tokens = [t for t in q.replace(",", " ").split() if len(t) > 1]
    hits: list[dict[str, str]] = []
    for doc in docs:
        blob = f"{doc.get('doc_id', '')}\n{doc.get('text', '')}".lower()
        if not tokens or any(t in blob for t in tokens):
            hits.append({"doc_id": doc.get("doc_id", ""), "text": doc.get("text", "")})
    if not hits and docs:
        # Fallback: return all docs so the agent can still answer.
        hits = [{"doc_id": d.get("doc_id", ""), "text": d.get("text", "")} for d in docs]
    return {
        "ok": True,
        "query": query,
        "n_hits": len(hits),
        "hits": hits,
        "note": "mock_search_docs: offline only; no URL fetch",
    }
