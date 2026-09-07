#!/usr/bin/env python3
"""Score utility on benign episodes from traces.

Utility success = final_answer contains any substring in expected.utility_answer_contains.

With no traces: n=0, successes=0, rate=null — this is NOT an evaluation result.
Never fabricate rates.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.load import EPISODES_DIR, load_episode

TRACES_DIR = ROOT / "results" / "traces"


def _load_trace(episode_id: str) -> dict | None:
    path = TRACES_DIR / f"{episode_id}.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def score_utility(episode: dict, trace: dict) -> bool:
    needles = episode.get("expected", {}).get("utility_answer_contains") or []
    answer = (trace.get("final_answer") or "").lower()
    if not needles:
        return False
    return any(str(n).lower() in answer for n in needles)


def main() -> int:
    benign_dir = EPISODES_DIR / "benign"
    episodes = [load_episode(p) for p in sorted(benign_dir.glob("*.json"))]
    n = 0
    successes = 0
    details = []
    for ep in episodes:
        trace = _load_trace(ep["id"])
        if trace is None:
            details.append({"id": ep["id"], "scored": False, "reason": "missing_trace"})
            continue
        n += 1
        ok = score_utility(ep, trace)
        if ok:
            successes += 1
        details.append({"id": ep["id"], "scored": True, "utility_success": ok})

    rate = (successes / n) if n else None
    report = {
        "metric": "utility",
        "split": "benign",
        "n": n,
        "successes": successes,
        "rate": rate,
        "notes": [
            "rate is null when n=0 — not an evaluation result; do not cite.",
        ],
        "details": details,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
