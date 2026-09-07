#!/usr/bin/env python3
"""Batch-run episodes through the harness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.config import load_config
from agent.load import EPISODES_DIR, load_episode, load_episode_by_id
from agent.loop import run_episode


def _ids_for_split(split: str) -> list[str]:
    d = EPISODES_DIR / split
    ids = []
    for path in sorted(d.glob("*.json")):
        ids.append(load_episode(path)["id"])
    return ids


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch-run agent-injection-bench episodes.")
    parser.add_argument("--split", choices=["attack", "benign", "all"], default="all")
    parser.add_argument("--ids", nargs="*", help="Optional explicit episode ids.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Optional cap on number of episodes.")
    args = parser.parse_args()

    if args.ids:
        ids = list(args.ids)
    elif args.split == "all":
        ids = _ids_for_split("attack") + _ids_for_split("benign")
    else:
        ids = _ids_for_split(args.split)

    if args.limit and args.limit > 0:
        ids = ids[: args.limit]

    write = not args.no_write
    cfg = load_config()
    if not args.dry_run and not cfg.configured:
        print(
            "LLM API key missing. Set AIB_LLM_API_KEY (or OPENAI_API_KEY). Use --dry-run without a key.",
            file=sys.stderr,
        )
        return 2

    results = []
    for eid in ids:
        episode = load_episode_by_id(eid)
        out = run_episode(episode, config=cfg, dry_run=args.dry_run, write=write)
        results.append(
            {
                "id": eid,
                "split": episode.get("split"),
                "status": out["trace"]["status"],
                "trace_path": out.get("trace_path"),
            }
        )

    print(
        json.dumps(
            {
                "n": len(results),
                "dry_run": args.dry_run,
                "note": "Batch run complete. Score separately with score_asr.py / score_utility.py — do not invent rates.",
                "results": results,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
