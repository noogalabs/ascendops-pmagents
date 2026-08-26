#!/usr/bin/env python3
"""Fail-closed member-repository hygiene census with no birth baseline."""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from pathlib import Path

PRIVATE_TERMS = (
    "Da" + "vid", "Di" + "ego", "Car" + "los", "Sil" + "vano",
    "Ca" + "sey", "B" + "ud", "Pa" + "ul", "Ka" + "den", "Brit" + "tany",
    "Ascend Property Management", "PB" + "GS", "Kapo Mechanical",
    "Legacy Heat and Air", "River City Repairs", "ZJB Construction LLC",
    "CT Flooring Supply House", "Stanley Steemer", "Trust Exterminating",
)
BANNED_TOKEN = "NE" + "PQ"
CODENAME = "Bet" + "ty"
TASK_ID_RE = re.compile(r"(?i)(?<![A-Za-z0-9_])task_\d+(?:_\d+)*(?![A-Za-z0-9_])")
SELF = {
    "ci/member-hygiene.py",
    "ci/test-member-hygiene.py",
    "ci/internal-codename-allowlist.tsv",
    ".github/scripts/leak-guard.sh",
    ".github/workflows/leak-guard.yml",
    "tests/leak-guard.test.sh",
}


def line_hash(line: str) -> str:
    return hashlib.sha256(line.encode()).hexdigest()


def tracked(root: Path) -> list[str]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=root)
    return [item.decode() for item in output.split(b"\0") if item]


def readable_lines(root: Path, relative: str):
    try:
        return (root / relative).read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return []


def load_visible(root: Path) -> set[str]:
    rows = {
        line.strip() for line in (root / "ci/member-visible-paths.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }
    missing = sorted(path for path in rows if not (root / path).is_file())
    if missing:
        raise SystemExit("member-visible manifest names missing files: " + ", ".join(missing))
    return rows


def load_allowlist(root: Path):
    rows = set()
    path = root / "ci/internal-codename-allowlist.tsv"
    for raw in path.read_text().splitlines():
        if not raw or raw.startswith("#"):
            continue
        relative, number, digest, token, reason = raw.split("\t", 4)
        rows.add((relative, int(number), digest, token.lower(), reason))
    return rows


def scan(root: Path) -> list[str]:
    visible = load_visible(root)
    allowlist = load_allowlist(root)
    seen_allowlist = set()
    failures = []
    private_re = re.compile(r"(?i)(?<![A-Za-z0-9_-])(?:" + "|".join(re.escape(x) for x in PRIVATE_TERMS) + r")(?![A-Za-z0-9_-])")
    banned_re = re.compile(r"(?i)(?<![A-Za-z0-9_-])" + re.escape(BANNED_TOKEN) + r"(?![A-Za-z0-9_-])")
    # A hyphen delimits a word here so protocol identifiers such as
    # ``BETTY-CONFIG`` cannot bypass the codename census.
    codename_re = re.compile(r"(?i)(?<![A-Za-z0-9_])" + re.escape(CODENAME) + r"(?![A-Za-z0-9_])")
    for relative in tracked(root):
        if relative in SELF:
            continue
        for number, line in enumerate(readable_lines(root, relative), 1):
            privacy_line = line.replace("NEEDS-" + PRIVATE_TERMS[0].upper(), "PROVENANCE-TAG")
            if private_re.search(privacy_line):
                failures.append(f"{relative}:{number}: private identity token")
            if banned_re.search(line):
                failures.append(f"{relative}:{number}: banned sales token")
            if TASK_ID_RE.search(line) and not relative.endswith("-REPORT.md"):
                failures.append(f"{relative}:{number}: internal task id on shipped member surface")
            for match in codename_re.finditer(line):
                if relative in visible:
                    failures.append(f"{relative}:{number}: internal codename on member-visible surface")
                    continue
                key_prefix = (relative, number, line_hash(line), match.group(0).lower())
                matches = [row for row in allowlist if row[:4] == key_prefix]
                if len(matches) != 1:
                    failures.append(f"{relative}:{number}: internal codename lacks exact-site allowlist")
                else:
                    seen_allowlist.add(matches[0])
    stale = allowlist - seen_allowlist
    failures.extend(f"{row[0]}:{row[1]}: stale internal-codename allowlist row" for row in sorted(stale))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    failures = scan(args.root.resolve())
    if failures:
        print("\n".join(failures))
        return 1
    print("PMAgents member hygiene: CLEAN (zero baseline)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
