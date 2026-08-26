"""Shared credential scanner for every configuration production path."""
from __future__ import annotations

import re
from pathlib import Path


TELEGRAM_PLACEHOLDER_ALLOWLIST = {b"1234567890:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
SECRET_PATTERNS = (
    ("OpenAI key", re.compile(rb"(?<![A-Za-z0-9_])sk-[A-Za-z0-9_-]{8,}")),
    ("GitHub token", re.compile(rb"ghp_[A-Za-z0-9]{8,}")),
    ("AWS key", re.compile(rb"AKIA[A-Z0-9]{12,}")),
    ("Slack token", re.compile(rb"xox[a-z]-[A-Za-z0-9-]{8,}")),
    ("Telegram bot token", re.compile(rb"(?P<value>\d{8,10}:[A-Za-z0-9_-]{35})")),
    ("private key", re.compile(rb"PRIVATE KEY")),
)


class CredentialScanRejected(Exception):
    def __init__(self, failures: list[tuple[str, str]]):
        self.failures = failures
        super().__init__("; ".join(f"{path}: {message}" for path, message in failures))


def scan_tree(root: Path) -> None:
    """Reject a credential-shaped value anywhere in a staged member tree."""
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise CredentialScanRejected([(
                f"credential-scan.{relative}", f"cannot scan file: {exc}",
            )]) from exc
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(data):
                if label == "Telegram bot token" and match.group("value") in TELEGRAM_PLACEHOLDER_ALLOWLIST:
                    continue
                line = data.count(b"\n", 0, match.start()) + 1
                raise CredentialScanRejected([(
                    f"credential-scan.{relative}", f"{label} found at line {line}",
                )])
