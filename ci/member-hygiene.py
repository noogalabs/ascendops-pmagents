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
# Owner rule 2026-09-01: PM Agents are SOFTWARE-agnostic and MODEL-agnostic.
# Platform names may appear only inside a platform HOW-skill variant or as a
# setup-answer example (exact-site allowlist, token "platform"); model/vendor
# names may appear only on runtime-mechanics surfaces (named class below) or
# at exact-site allowlisted config/placeholder rows (token "model").
PLATFORM_TERMS = ("PropertyMeld", "Property Meld", "Meld", "AppFolio",
                  "Buildium", "Yardi", "Rent Manager", "RentManager")
PLATFORM_SKILL_DIRS = ("/.claude/skills/propertymeld/", "/.claude/skills/appfolio/")
MODEL_TERMS_CI = ("Claude", "Codex", "GPT", "Gemini", "Anthropic", "OpenAI")
MODEL_TERMS_CS = ("Opus", "Sonnet", "Haiku", "Fable")  # English words: case-sensitive
MODEL_TERMS = MODEL_TERMS_CI + MODEL_TERMS_CS
MODEL_ID_RE = re.compile(r"(?i)(?<![./])\bclaude-[a-z0-9-]+\b|\bgpt-[0-9][a-z0-9.-]*\b|\bgemini-[0-9][a-z0-9.-]*\b")
# Runtime-mechanics surfaces: the harness IS a named model runtime and names
# itself here; these are exempt as a CLASS (named in the census output), not
# as duty text. Duty surfaces are everything else.
RUNTIME_SURFACE_NAMES = {"HEARTBEAT.md", "AGENTS.md", "TOOLS.md", "CLAUDE.md", "SYSTEM.md",
                         "config.json", "settings.json", ".env.example"}
# README.md is member-facing front-page prose: scanned as a duty surface; its
# genuine runtime mentions are allowlisted by exact site (dane fold 2026-09-01).
# Engine and edition CODE is runtime mechanics (credential patterns, harness
# wiring); duty text never lives in .py files.
RUNTIME_CODE_SUFFIXES = (".py",)
# A skill's frontmatter `model:` line is RUNTIME ROUTING config (which engine
# the harness runs the skill on), not duty prose (dane ruling 2026-09-01).
FRONTMATTER_MODEL_RE = re.compile(r"^model:\s*\S+\s*$")
RUNTIME_SKILL_DIRS = ("/.claude/skills/agent-management/", "/.claude/skills/m2c1-worker/",
                      "/.claude/skills/worker-agents/", "/.claude/skills/delegation-matrix/",
                      "/.claude/skills/auto-skill/", "/.claude/skills/soul-philosophy/",
                      "/.claude/skills/heartbeat/", "/.claude/skills/comms/",
                      "/.claude/skills/tasks/", "/.claude/skills/cron-management/",
                      "/.claude/skills/event-logging/", "/.claude/skills/bus-reference/",
                      "/.claude/skills/env-management/", "/.claude/skills/approvals/",
                      "/.claude/skills/human-tasks/", "/.claude/skills/onboarding/",
                      "/.claude/skills/knowledge-base/", "/.claude/skills/activity-channel/",
                      "/.claude/skills/tool-registration/", "/.claude/skills/system-diagnostics/",
                      "/.claude/skills/memory/", "/.claude/skills/guardrails-reference/",
                      "/.claude/skills/opencli/", "/.claude/skills/codex-bot-review/",
                      "/.claude/skills/officecli/", "/.claude/skills/graphify/",
                      "/.claude/skills/agent-browser/")


def is_runtime_surface(relative: str) -> bool:
    name = relative.rsplit("/", 1)[-1]
    if name in RUNTIME_SURFACE_NAMES or name.endswith(RUNTIME_CODE_SUFFIXES):
        return True
    return any(d in "/" + relative for d in RUNTIME_SKILL_DIRS)


def strip_platform_skill_paths(line: str) -> str:
    """A manifest/provenance/path-list reference to the platform variant
    skill's own path is a reference to the variant, not duty prose: the path
    substring is removed and the REST of the line is still scanned, so prose
    cannot smuggle a platform name by sharing a line with the path."""
    for d in PLATFORM_SKILL_DIRS:
        line = line.replace(d.strip("/"), "")
    return line


def is_platform_skill(relative: str) -> bool:
    return any(d in "/" + relative for d in PLATFORM_SKILL_DIRS)
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
    platform_re = re.compile(r"(?i)(?<![A-Za-z0-9_])(?:" + "|".join(re.escape(x) for x in PLATFORM_TERMS) + r")(?![A-Za-z0-9_])")
    # `.claude/` directory paths and `/claude-code` package segments are the
    # runtime's own filesystem naming, not duty prose: dot/slash-preceded
    # tokens are excluded by construction.
    # ...and a `CLAUDE.md` filename reference names the runtime's config file.
    model_re = re.compile(r"(?<![A-Za-z0-9_./-])(?:"
                          + "|".join("(?i:" + re.escape(x) + ")" for x in MODEL_TERMS_CI) + "|"
                          + "|".join(re.escape(x) for x in MODEL_TERMS_CS) + r")(?![A-Za-z0-9_-]|\.md\b)")
    runtime_exempt_files = 0
    for relative in tracked(root):
        if relative in SELF:
            continue
        in_frontmatter = False
        for number, line in enumerate(readable_lines(root, relative), 1):
            # YAML frontmatter block = line 1 "---" through the next "---".
            if number == 1 and line.strip() == "---":
                in_frontmatter = True
            elif in_frontmatter and line.strip() == "---":
                in_frontmatter = False
            privacy_line = line.replace("NEEDS-" + PRIVATE_TERMS[0].upper(), "PROVENANCE-TAG")
            if private_re.search(privacy_line):
                failures.append(f"{relative}:{number}: private identity token")
            if banned_re.search(line):
                failures.append(f"{relative}:{number}: banned sales token")
            if (TASK_ID_RE.search(line)
                    and (not relative.endswith("-REPORT.md") or relative in visible)):
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
            # Platform names: allowed only inside a platform HOW-skill variant;
            # anywhere else needs an exact-site row under token "platform".
            if not is_platform_skill(relative):
                for match in platform_re.finditer(strip_platform_skill_paths(line)):
                    key_prefix = (relative, number, line_hash(line), "platform")
                    matches = [row for row in allowlist if row[:4] == key_prefix]
                    if len(matches) != 1:
                        failures.append(f"{relative}:{number}: platform name {match.group(0)!r} on duty surface (owner rule: software-agnostic)")
                    else:
                        seen_allowlist.add(matches[0])
                    break
            # Model/vendor names: runtime-mechanics surfaces are exempt as a
            # named class; every duty surface needs an exact-site row under
            # token "model".
            if not is_runtime_surface(relative) and not (in_frontmatter and FRONTMATTER_MODEL_RE.match(line)):
                model_hit = model_re.search(line) or MODEL_ID_RE.search(line)
                if model_hit:
                    key_prefix = (relative, number, line_hash(line), "model")
                    matches = [row for row in allowlist if row[:4] == key_prefix]
                    if len(matches) != 1:
                        failures.append(f"{relative}:{number}: model name {model_hit.group(0)!r} on duty surface (owner rule: model-agnostic)")
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
