from __future__ import annotations

from agent.load import iter_episode_paths, load_episode, make_validator, validate_episode


def test_all_episodes_valid():
    v = make_validator()
    paths = iter_episode_paths(include_examples=True)
    assert len(paths) >= 42
    for path in paths:
        errs = validate_episode(load_episode(path), v)
        assert not errs, f"{path}: {errs}"


def test_attack_requires_injection_and_forbidden():
    v = make_validator()
    bad = {
        "id": "atk_999",
        "split": "attack",
        "user_query": "x",
        "retrieved_docs": [{"doc_id": "d", "text": "t"}],
        "injection": {"present": False},
        "expected": {"allowed_tools": ["search_docs"], "forbidden_tools": []},
    }
    assert validate_episode(bad, v)


def test_benign_requires_present_false():
    v = make_validator()
    bad = {
        "id": "ben_999",
        "split": "benign",
        "user_query": "x",
        "retrieved_docs": [{"doc_id": "d", "text": "t"}],
        "injection": {
            "present": True,
            "payload": "p",
            "target_tool": "send_email",
        },
        "expected": {"allowed_tools": ["search_docs"], "forbidden_tools": []},
    }
    assert validate_episode(bad, v)


def test_counts_20_each():
    from agent.load import EPISODES_DIR

    assert len(list((EPISODES_DIR / "attack").glob("*.json"))) == 20
    assert len(list((EPISODES_DIR / "benign").glob("*.json"))) == 20
