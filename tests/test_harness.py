from __future__ import annotations

from agent.config import LLMConfig, load_config
from agent.load import load_episode_by_id
from agent.loop import run_episode
from agent.traces import build_trace


def test_load_config_defaults(monkeypatch):
    monkeypatch.delenv("AIB_LLM_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    cfg = load_config()
    assert isinstance(cfg, LLMConfig)
    assert cfg.configured is False


def test_dry_run_trace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    ep = load_episode_by_id("atk_002")
    # Force traces into temp by patching module path via write=False
    out = run_episode(ep, dry_run=True, write=False)
    assert out["trace"]["status"] == "dry_run"
    assert out["trace"]["episode_id"] == "atk_002"
    assert out["trace_path"] is None


def test_build_trace_fields():
    ep = load_episode_by_id("ben_002")
    tr = build_trace(
        episode=ep,
        model="m",
        provider="p",
        user_task=ep["user_query"],
        tool_calls=[],
        final_answer="ok",
        status="ok",
    )
    assert tr["episode_id"] == "ben_002"
    assert tr["episode_type"] == "benign"
    assert "timestamp" in tr
