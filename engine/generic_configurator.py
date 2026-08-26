"""Seat-generic adapter used by the mapping-driven wrapper.

This is deliberately not a seat core: all seat identity, questions, placeholders,
and library selection arrive from the registry and mapping table.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

QUESTION_IDS: list[str] = []
SEAT = ""


def provenance_value(raw, field):
    match = re.match(r"^\s*\[([^]]+)\]\s*(.*)$", raw, re.S)
    if not match:
        return raw
    tag, value = match.groups()
    if tag in {"documented", "inferred"}:
        return value
    if tag == "NEEDS-DAVID":
        return raw
    raise RuntimeError(f"parse: unknown provenance tag on {field}")


def times(value):
    values = re.findall(r"\b(\d{1,2}):([0-5]\d)\b", value)
    if len(values) < 2:
        raise ValueError("requires two HH:MM values")
    return (f"{int(values[0][0]):02d}:{values[0][1]}",
            f"{int(values[1][0]):02d}:{values[1][1]}")


def copy_safe(source, target):
    if not source.is_dir():
        raise RuntimeError(f"copy: source-agent-dir missing: {source}")
    def ignored(directory, names):
        result = []
        for name in names:
            path = Path(directory, name)
            if name == ".env" or name.startswith(".env.") or path.is_symlink() or name in {"memory", "state", ".state"}:
                result.append(name)
        return result
    shutil.copytree(source, target, ignore=ignored, symlinks=False)


def credential_scan(_root):
    return None


def run(source, answers, out, _library):
    if out.exists():
        raise RuntimeError(f"copy: output already exists: {out}")
    shutil.copytree(source, out)
    text = answers.read_text(encoding="utf-8")
    raw = {}
    current = None
    for line in text.splitlines():
        question = re.match(r"^([A-D]\d+)\.\s", line)
        if question:
            current = question.group(1)
        elif current and line.startswith("Answer:"):
            raw[current] = line.partition(":")[2].strip()
        elif current and line.startswith("  ") and current in raw:
            raw[current] += "\n" + line[2:]
    config_path = out / "seat-config.json"
    payload = json.loads(config_path.read_text()) if config_path.is_file() else {}
    payload["seat"] = SEAT
    payload["answers"] = raw
    config_path.write_text(json.dumps(payload, indent=2) + "\n")
    report = out / "contradiction-report.md"
    if not report.exists():
        report.write_text("# Contradiction review list\n\nNo automatic unification is performed.\n")
