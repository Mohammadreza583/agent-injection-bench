#!/usr/bin/env python3
"""Run the agent harness on one episode (or a smoke pair)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.config import load_config
from agent.load import load_episode_by_id
from agent.loop import run_episode


def _run_one(episode_id: str, *, dry_run: bool, write: bool) -> dict:
    episode = load_episode_by_id(episode_id)
    return run_episode(episode, dry_run=dry_run, write=write)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run agent-injection-bench harness on an episode.")
    parser.add_argument("--id", help="Episode id, e.g. atk_002")
    parser.add_argument("--smoke", action="store_true", help="Run atk_002 + ben_002 only (pipeline check, not an eval).")
    parser.add_argument("--dry-run", action="store_true", help="Skip LLM call; write a dry-run trace.")
    parser.add_argument("--no-write", action="store_true", help="Do not write traces to disk.")
    args = parser.parse_args()

    if not args.smoke and not args.id:
        parser.error("Provide --id or --smoke")

    write = not args.no_write
    ids = ["atk_002", "ben_002"] if args.smoke else [args.id]
    results = []
    for eid in ids:
        try:
            out = _run_one(eid, dry_run=args.dry_run, write=write)
            results.append({"id": eid, "ok": True, "trace_path": out.get("trace_path"), "status": out["trace"]["status"]})
        except SystemExit as exc:
            # Missing API key
            print(str(exc), file=sys.stderr)
            return 2
        except Exception as exc:  # noqa: BLE001
            results.append({"id": eid, "ok": False, "error": f"{type(exc).__name__}: {exc}"})

    if args.smoke:
        print(json.dumps({"smoke": True, "note": "pipeline check only — not an evaluation", "results": results}, indent=2))
    else:
        print(json.dumps(results[0], indent=2))

    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    # Touch config early so dotenv is loaded for non-dry runs.
    load_config()
    raise SystemExit(main())
