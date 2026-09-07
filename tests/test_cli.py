from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_validate_episodes_cli():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_episodes.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    report = json.loads(proc.stdout)
    assert report["ok"] is True
    assert report["n"] == 42
    assert report["errors"] == 0


def test_score_asr_empty_traces():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score_asr.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    report = json.loads(proc.stdout)
    # Fresh checkout: no traces → rate null (not an eval result)
    if report["n"] == 0:
        assert report["rate"] is None
        assert report["successes"] == 0
