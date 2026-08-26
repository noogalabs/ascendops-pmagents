"""Shared pure-value extractors used across mapping and cross-seat paths."""
from __future__ import annotations

import re


def maintenance_platform(value):
    match = re.search(
        r"(?:platform\s+)?([A-Za-z][A-Za-z0-9_-]+)\s+for\s+maintenance",
        str(value),
        re.I,
    )
    if not match:
        raise ValueError("maintenance platform not found")
    return match.group(1)
