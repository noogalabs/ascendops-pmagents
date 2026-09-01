#!/usr/bin/env python3
"""Guided, presentation-only setup for AscendOps PMAgents."""
from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable, NamedTuple, TextIO

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "engine"))
import engine  # noqa: E402


SEAT_LABELS = {
    "accounting": "Accounting",
    "maintenance-coordinator": "Maintenance coordinator",
    "turnover-coordinator": "Turnover coordinator",
}
SEATS = tuple({"id": seat, "label": SEAT_LABELS.get(seat, seat.replace("-", " ").title())}
              for seat in engine.SUPPORTED)
SHIPPED_MAINTENANCE_TEMPLATE = ROOT / "templates" / "maintenance-coordinator"
SCAFFOLD_TOKENS = (
    "agent_name",
    "org",
    "current_timestamp",
    "upstream_update_minute",
)
SKIP_WORDS = {"skip", "unsure", "?"}
REJECTION_RULES = (
    ("mapping.config_keys", "the configuration question named by this row", "the answer cannot be written with the declared type or path", "Example: enter a timezone such as America/Denver"),
    ("config_keys", "the configuration question named by this row", "the answer cannot be written with the declared type or path", "Example: enter a timezone such as America/Denver"),
    ("mapping", "this edition's setup mapping", "the installed edition data is missing or invalid", "Example: reinstall or update this PMAgents checkout, then retry"),
    ("template", "the template agent directory", "the template could not be read or still contains unmanaged setup markers", "Example: choose a clean, unconfigured template directory"),
    ("protected_state", "the existing agent directory", "protected member state could not be preserved", "Example: check directory permissions and retry without deleting memory or tasks"),
    ("structured_answers_file", "the configured-answer artifact", "the edition's declared artifact is absent or conflicts with another file", "Example: restore the edition mapping and rerun setup"),
    ("sealed_core.", "the questionnaire answer named by the sealed configuration stage", "the sealed configurator rejected the supplied content", "Example: remove credentials and use plain operational answers"),
    ("cross_seat", "the connected-seat question named by this row", "a connected seat is missing, incompatible, or contradictory", "Example: configure the named owner seat first, then retry"),
    ("append-plan", "the cross-seat handoff plan", "the appender or owner artifact is missing or incompatible", "Example: rerun setup for both named seats before applying the handoff"),
    ("appender.", "the appending seat's configured answers", "the appender artifact cannot be read safely", "Example: rerun setup for the appending seat"),
    ("owner.", "the owner seat's configured answers", "the owner artifact cannot be read safely", "Example: rerun setup for the owner seat"),
    ("file", "the completed answers file", "the questionnaire file cannot be read", "Example: choose a UTF-8 answers file from this edition"),
    ("output", "the configured agent destination", "the destination is not a usable agent directory", "Example: choose a new directory or the same existing configured agent"),
    ("seat", "the setup edition", "the selected edition is not installed", "Example: choose one of the editions shown by setup"),
)


class PromptField(NamedTuple):
    key: str
    label: str


AUTONOMY_FIELDS = (
    PromptField("cover.Autonomy mode", "Autonomy mode"),
    PromptField("cover.Unlock window", "Unlock window"),
    PromptField("cover.Qualifying accuracy", "Qualifying accuracy"),
    PromptField("cover.Resident messaging autonomy", "Resident messaging autonomy"),
)
AUTONOMY_DEFAULTS = {
    "cover.Autonomy mode": "copilot",
    "cover.Unlock window": "last_10",
    "cover.Qualifying accuracy": "null",
    "cover.Resident messaging autonomy": "no",
}


def questionnaire_fields(template: str, cover_fields=None) -> list[PromptField]:
    active_cover_fields = engine.intake.COVER_FIELDS if cover_fields is None else cover_fields
    fields = [
        PromptField(f"cover.{label}", label)
        for label in active_cover_fields
    ]
    for field in AUTONOMY_FIELDS:
        if field not in fields:
            fields.append(field)
    for match in engine.intake.QUESTION_HEADING.finditer(template):
        fields.append(PromptField(match.group(1), f"{match.group(1)}. {match.group(2)}"))
    return fields


def answer_values(text: str, cover_fields=None) -> dict[str, str]:
    active_cover_fields = engine.intake.COVER_FIELDS if cover_fields is None else cover_fields
    values: dict[str, str] = {}
    lines = text.splitlines()
    for label in active_cover_fields:
        for index, line in enumerate(lines):
            match = re.match(rf"^{re.escape(label)}:\s*(.*)$", line)
            if not match:
                continue
            value = engine.intake.indented_value(lines, index, match.group(1))
            if value.strip(" _\n"):
                values[f"cover.{label}"] = value
    current = None
    lines = text.splitlines()
    for index, line in enumerate(lines):
        question = engine.intake.QUESTION_LINE.match(line)
        if question:
            current = question.group(1)
            continue
        if not current or not line.startswith("Answer:"):
            continue
        answer = engine.intake.indented_value(lines, index, line.partition(":")[2])
        if answer.strip(" _\n"):
            values[current] = answer
    return values


def set_answer(text: str, field: PromptField, value: str) -> str:
    if field.key.startswith("cover."):
        rendered = value.rstrip().replace("\n", "\n  ")
        pattern = rf"^{re.escape(field.label)}:{engine.intake.INTAKE_VALUE_SPAN}"
        if not re.search(pattern, text, flags=re.M):
            anchor = re.search(r"^Timezone:.*$", text, flags=re.M)
            if anchor:
                return text[:anchor.end()] + f"\n{field.label}: {rendered}" + text[anchor.end():]
            return f"{field.label}: {rendered}\n" + text
        return re.sub(pattern, f"{field.label}: {rendered}", text, count=1, flags=re.M)
    pattern = (
        rf"(^({re.escape(field.key)})\..*?^Answer:){engine.intake.INTAKE_VALUE_SPAN}"
    )
    rendered = value.rstrip().replace("\n", "\n  ")
    return re.sub(pattern, lambda match: f"{match.group(1)} {rendered}",
                  text, count=1, flags=re.M | re.S)


def collect_answer(ask: Callable[[str], str], prompt: str) -> str:
    """Collect a blank-line-terminated answer without flattening semantic lines."""
    lines = [ask(prompt)]
    while lines[-1]:
        lines.append(ask("Continue answer (blank line finishes): "))
    return "\n".join(lines[:-1]).strip()


def documented_answer(response: str) -> str:
    if response.lower() in SKIP_WORDS or not response:
        return "[NEEDS-DAVID] Confirm this answer later"
    if not re.match(r"^\[(?:documented|inferred|NEEDS-DAVID)\]", response):
        return f"[documented] {response}"
    return response


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.setup-tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def upstream_update_minute(agent_name: str) -> int:
    """Match cortextOS add-agent's unsigned FNV-1a update-minute assignment."""
    value = 2166136261
    for byte in agent_name.encode("utf-8"):
        value ^= byte
        value = (value * 16777619) & 0xFFFFFFFF
    return value % 60


def scaffold_identity(output: Path) -> tuple[str, str]:
    """Derive add-agent identity inputs from the documented member destination."""
    agent_name = output.name
    org = output.parent.parent.name if output.parent.name == "agents" else output.parent.name
    if not agent_name or not org:
        raise ValueError("configured agent path must identify both organization and agent")
    return agent_name, org


def materialize_template(
    source: Path,
    destination: Path,
    output: Path,
    *,
    now: Callable[[], datetime.datetime],
) -> Path:
    """Copy and resolve scaffold-time tokens before the fail-closed engine runs."""
    agent_name, org = scaffold_identity(output)
    timestamp = (
        now().astimezone(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    replacements = {
        "agent_name": agent_name,
        "org": org,
        "current_timestamp": timestamp,
        "upstream_update_minute": str(upstream_update_minute(agent_name)),
    }
    shutil.copytree(source, destination, symlinks=True)
    for path in destination.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in SCAFFOLD_TOKENS:
            text = text.replace("{{" + token + "}}", replacements[token])
        path.write_text(text, encoding="utf-8")
    return destination


def rejection_rule(row: str, fields: dict[str, PromptField] | None = None):
    if engine.intake.QUESTION_ID.fullmatch(row):
        question = fields[row].label if fields and row in fields else row
        return (question, "the answer did not meet the question's required format", "Example: enter a confirmed answer, or use 'unsure' to confirm it later")
    if row.startswith("cover."):
        return (row.removeprefix("cover."), "this cover-sheet answer is missing or invalid", "Example: enter the company value requested by this field")
    for prefix, question, problem, example in REJECTION_RULES:
        if row.startswith(prefix):
            return question, problem, example
    return None


def render_rejection(
    exc: engine.IntakeRejected,
    err: TextIO,
    fields: dict[str, PromptField] | None = None,
) -> None:
    print("Setup needs a correction. No configured agent files were written.", file=err)
    for row, reason in exc.failures:
        print(f"Issue: {row}: {reason}", file=err)
        rule = rejection_rule(row, fields)
        if rule is None:
            print("Question to fix: this setup row is not recognized by this wrapper.", file=err)
            print("Share the raw issue above with support; it has not been hidden or replaced.", file=err)
            continue
        question, problem, example = rule
        print(f"Question to fix: {question}", file=err)
        print(f"What was wrong: {problem}", file=err)
        print(example, file=err)


def answer_field_map(answers: Path, cover_fields=None) -> dict[str, PromptField]:
    try:
        return {
            field.key: field
            for field in questionnaire_fields(answers.read_text(encoding="utf-8"), cover_fields)
        }
    except (OSError, UnicodeError):
        return {}


def fix_named_answer(
    answers: Path,
    failures,
    ask: Callable[[str], str],
    editable: dict[str, PromptField] | None = None,
) -> bool:
    editable = answer_field_map(answers) if editable is None else editable
    row = next((name for name, _reason in failures if name in editable), None)
    if row is None:
        return ask("Correct the named file or setup input, then type 'retry' (Enter exits): ").strip().lower() == "retry"
    response = collect_answer(
        ask, f"New answer for {editable[row].label} (blank line finishes; blank first line exits): "
    )
    if not response:
        return False
    response = documented_answer(response)
    text = set_answer(answers.read_text(encoding="utf-8"), editable[row], response)
    atomic_text(answers, text)
    return True


def guided_answers(path: Path, ask: Callable[[str], str], out: TextIO, seat: str = "maintenance-coordinator") -> Path:
    cover_fields = engine.cover_fields_for_seat(seat)
    if path.exists():
        text = path.read_text(encoding="utf-8")
        print(f"Resuming {path}", file=out)
    else:
        text = engine.SUPPORTED[seat]["answers"].read_text(encoding="utf-8")
        atomic_text(path, text)
    complete = answer_values(text, cover_fields)
    fields = questionnaire_fields(text, cover_fields)
    for field in fields:
        if field.key in complete:
            continue
        response = collect_answer(
            ask,
            f"{field.label}\nAnswer (blank line finishes; 'unsure' confirms later): ",
        )
        if not response and field.key in AUTONOMY_DEFAULTS:
            response = AUTONOMY_DEFAULTS[field.key]
        response = documented_answer(response)
        text = set_answer(text, field, response)
        atomic_text(path, text)
    return path


def choose_seat(ask: Callable[[str], str], out: TextIO) -> str:
    print("Available setup editions:", file=out)
    for number, seat in enumerate(SEATS, 1):
        print(f"  {number}. {seat['label']}", file=out)
    raw = ask("Choose an edition [1]: ").strip() or "1"
    if not raw.isdigit() or not 1 <= int(raw) <= len(SEATS):
        raise ValueError("choose one of the listed edition numbers")
    return SEATS[int(raw) - 1]["id"]


def cleanup_interrupted_candidates(output: Path | None) -> None:
    if output is None:
        return
    for pattern in (
        f".{output.name}.glue-scratch-*",
        f".{output.name}.glue-candidate-*",
    ):
        for path in output.parent.glob(pattern):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)


def discover_seat_registry(
    output: Path,
    current_seat: str,
    *,
    out: TextIO = sys.stdout,
) -> dict[str, dict]:
    """Discover complete sibling installations without writing to peer trees."""
    registry: dict[str, dict] = {}
    if not output.parent.is_dir():
        return registry
    for candidate in sorted(output.parent.iterdir()):
        if candidate == output or not candidate.is_dir() or not (candidate / "config.json").is_file():
            continue
        for seat in engine.SUPPORTED:
            if seat == current_seat:
                continue
            mapping = engine.load_seat_mapping(seat)
            filename = engine.cross_seat.structured_answers_filename(mapping)
            artifact = candidate / filename
            if not artifact.is_file():
                continue
            try:
                payload = json.loads(artifact.read_text(encoding="utf-8"))
                if not isinstance(payload, dict) or payload.get("seat") != seat:
                    continue
                engine.cross_seat._validate_peer_version(
                    seat, payload, engine.ENGINE_VERSION,
                )
            except engine.cross_seat.CrossSeatRejected as exc:
                detail = "; ".join(f"{row}: {reason}" for row, reason in exc.failures)
                print(f"Excluded connected seat {seat} at {candidate}: {detail}", file=out)
                continue
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                print(f"Excluded connected seat {seat} at {candidate}: {exc}", file=out)
                continue
            if seat in registry:
                first = Path(registry[seat]["path"])
                raise ValueError(
                    f"duplicate connected seat {seat}: both {first} and {candidate} "
                    "claim this seat; remove or relocate one before setup"
                )
            registry[seat] = {"path": candidate, "mapping": mapping}
    return registry


def render_cross_seat_completion(output: Path, seat: str, out: TextIO) -> None:
    mapping = engine.load_seat_mapping(seat)
    artifact = output / engine.cross_seat.structured_answers_filename(mapping)
    try:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return
    cross = payload.get("cross_seat", {})
    if not isinstance(cross, dict):
        return
    pointers = cross.get("pointers", {})
    held = cross.get("held", {})
    if not isinstance(pointers, dict) or not isinstance(held, dict):
        return
    for name, row in sorted(pointers.items()):
        if isinstance(row, dict) and row.get("state") == "resolved":
            print(f"Connected pointer {name}: resolved from {row.get('owner_seat')}", file=out)
    for name, row in sorted(held.items()):
        if isinstance(row, dict):
            print(f"Connected pointer {name}: held pending {row.get('held_pending_seat')}", file=out)


def run_setup(
    *,
    ask: Callable[[str], str] = input,
    out: TextIO = sys.stdout,
    err: TextIO = sys.stderr,
    clock: Callable[[], datetime.date] = datetime.date.today,
    now: Callable[[], datetime.datetime] = lambda: datetime.datetime.now(datetime.timezone.utc),
    configure_fn=engine.configure,
) -> int:
    output = None
    materialized_root = None
    try:
        seat = choose_seat(ask, out)
        default_source = (SHIPPED_MAINTENANCE_TEMPLATE
                          if seat == "maintenance-coordinator"
                          else engine.SUPPORTED[seat]["library"])
        selected_source = ask(f"Template agent directory [{default_source}]: ").strip()
        source = Path(selected_source).expanduser().resolve() if selected_source else default_source
        output = Path(ask("Configured agent directory: ").strip()).expanduser().resolve()
        mode = ask("Answers: [1] guide me  [2] use a completed file [1]: ").strip() or "1"
        if mode == "1":
            default_answers = Path.cwd() / "pmagents-setup-answers.md"
            selected = ask(f"Answers file [{default_answers}]: ").strip()
            answers = guided_answers(
                Path(selected).expanduser().resolve() if selected else default_answers,
                ask,
                out,
                seat,
            )
        elif mode == "2":
            answers = Path(ask("Completed answers file: ").strip()).expanduser().resolve()
        else:
            raise ValueError("answers choice must be 1 or 2")

        if output.exists():
            actual_source = output
        elif seat == "maintenance-coordinator":
            materialized_root = Path(tempfile.mkdtemp(prefix="pmagents-materialized-"))
            actual_source = materialize_template(
                source, materialized_root / "source", output, now=now,
            )
        else:
            actual_source = source
        seat_registry = discover_seat_registry(output, seat, out=out)
        while True:
            try:
                configure_fn(
                    actual_source, answers, output, seat, clock=clock,
                    seat_registry=seat_registry,
                )
                break
            except engine.IntakeRejected as exc:
                editable = answer_field_map(answers, engine.cover_fields_for_seat(seat))
                render_rejection(exc, err, editable)
                if not fix_named_answer(answers, exc.failures, ask, editable):
                    return 2
                if output.exists():
                    actual_source = output
                elif seat == "maintenance-coordinator":
                    # A retry means the member may have corrected the selected source.
                    # Never retry the one-time materialized snapshot.
                    shutil.rmtree(actual_source, ignore_errors=True)
                    actual_source = materialize_template(
                        source, materialized_root / "source", output, now=now,
                    )
        print(f"Configured agent: {output}", file=out)
        render_cross_seat_completion(output, seat, out)
        print("Next: review the generated agent with your implementation contact before activation.", file=out)
        return 0
    except KeyboardInterrupt:
        cleanup_interrupted_candidates(output)
        print("Setup stopped. No partial configured agent was written; rerun the same command to resume answers.", file=err)
        return 130
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"SETUP ERROR: {exc}", file=err)
        return 2
    except Exception as exc:
        print(f"ERROR {exc}", file=err)
        return 1
    finally:
        if materialized_root is not None:
            shutil.rmtree(materialized_root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Guided AscendOps PMAgents setup")
    parser.parse_args()
    return run_setup()


if __name__ == "__main__":
    raise SystemExit(main())
