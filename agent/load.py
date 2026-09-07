"""Episode loading and schema validation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "episode.schema.json"
EPISODES_DIR = ROOT / "data" / "episodes"
EXAMPLES_DIR = ROOT / "examples"


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def make_validator() -> Draft7Validator:
    return Draft7Validator(load_schema())


def load_episode(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Episode must be a JSON object: {path}")
    return data


def validate_episode(episode: dict[str, Any], validator: Draft7Validator | None = None) -> list[str]:
    v = validator or make_validator()
    return [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in sorted(v.iter_errors(episode), key=lambda x: list(x.path))]


def iter_episode_paths(*, include_examples: bool = True) -> list[Path]:
    paths: list[Path] = []
    for split in ("attack", "benign"):
        d = EPISODES_DIR / split
        if d.is_dir():
            paths.extend(sorted(d.glob("*.json")))
    if include_examples and EXAMPLES_DIR.is_dir():
        paths.extend(sorted(EXAMPLES_DIR.glob("episode_*.json")))
    return paths


def find_episode_by_id(episode_id: str) -> Path:
    for path in iter_episode_paths(include_examples=True):
        ep = load_episode(path)
        if ep.get("id") == episode_id:
            return path
    raise FileNotFoundError(f"Episode id not found: {episode_id}")


def load_episode_by_id(episode_id: str) -> dict[str, Any]:
    return load_episode(find_episode_by_id(episode_id))
