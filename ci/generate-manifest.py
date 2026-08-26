#!/usr/bin/env python3
"""Generate MANIFEST.sha256 from Git's tracked-file census only."""
from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"


def tracked_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / item.decode() for item in output.split(b"\0") if item and item.decode() != "MANIFEST.sha256"]


def render() -> str:
    rows = []
    for path in tracked_files():
        if not path.is_file():
            raise SystemExit(f"tracked manifest input is absent: {path.relative_to(ROOT)}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(ROOT)}")
    return "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if MANIFEST.read_text() != expected:
            print("MANIFEST.sha256 differs from the tracked-file census")
            return 1
        return 0
    MANIFEST.write_text(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
