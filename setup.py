#!/usr/bin/env python3
"""Guided, presentation-only setup for AscendOps PMAgents."""
from __future__ import annotations

import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path
from typing import Callable, NamedTuple, TextIO

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "engine"))
import engine  # noqa: E402


SEATS = (
    {"id": "maintenance-coordinator", "label": "Maintenance coordinator"},
    {"id": "business-development", "label": "Business development"},
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
    marker: str


def questionnaire_fields(template: str) -> list[PromptField]:
    fields = [
        PromptField(f"cover.{label}", label, rf"^{re.escape(label)}:\s*.*$" )
        for label in engine.intake.COVER_FIELDS
    ]
    for match in re.finditer(r"^([A-D]\d+)\.\s+(.+)$", template, re.M):
        fields.append(PromptField(match.group(1), f"{match.group(1)}. {match.group(2)}", ""))
    return fields


def answer_values(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for label in engine.intake.COVER_FIELDS:
        match = re.search(rf"^{re.escape(label)}:\s*(.*)$", text, re.M)
        if match and match.group(1).strip(" _"):
            values[f"cover.{label}"] = match.group(1).strip()
    current = None
    for line in text.splitlines():
        question = re.match(r"^([A-D]\d+)\.\s", line)
        if question:
            current = question.group(1)
        elif current and line.startswith("Answer:") and line.partition(":")[2].strip(" _"):
            values[current] = line.partition(":")[2].strip()
    return values


def set_answer(text: str, field: PromptField, value: str) -> str:
    if field.key.startswith("cover."):
        return re.sub(field.marker, f"{field.label}: {value}", text, count=1, flags=re.M)
    pattern = rf"(^({re.escape(field.key)})\..*?^Answer:)\s*[^\n]*"
    return re.sub(pattern, rf"\1 {value}", text, count=1, flags=re.M | re.S)


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.setup-tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def rejection_rule(row: str, fields: dict[str, PromptField] | None = None):
    if re.fullmatch(r"[A-D]\d+", row):
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


def answer_field_map(answers: Path) -> dict[str, PromptField]:
    try:
        return {
            field.key: field
            for field in questionnaire_fields(answers.read_text(encoding="utf-8"))
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
    response = ask(f"New answer for {editable[row].label} (Enter exits setup): ").strip()
    if not response:
        return False
    if response.lower() in SKIP_WORDS:
        response = "[NEEDS-DAVID] Confirm this answer later"
    elif not re.match(r"^\[(?:documented|inferred|NEEDS-DAVID)\]", response):
        response = f"[documented] {response}"
    text = set_answer(answers.read_text(encoding="utf-8"), editable[row], response)
    atomic_text(answers, text)
    return True


def guided_answers(path: Path, ask: Callable[[str], str], out: TextIO, seat: str) -> Path:
    if path.exists():
        text = path.read_text(encoding="utf-8")
        print(f"Resuming {path}", file=out)
    else:
        text = engine.SUPPORTED[seat]["answers"].read_text(encoding="utf-8")
        atomic_text(path, text)
    complete = answer_values(text)
    fields = questionnaire_fields(text)
    for field in fields:
        if field.key in complete:
            continue
        response = ask(f"{field.label}\nAnswer (or 'unsure' to confirm later): ").strip()
        if response.lower() in SKIP_WORDS or not response:
            response = "[NEEDS-DAVID] Confirm this answer later"
        elif not re.match(r"^\[(?:documented|inferred|NEEDS-DAVID)\]", response):
            response = f"[documented] {response}"
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


def run_setup(
    *,
    ask: Callable[[str], str] = input,
    out: TextIO = sys.stdout,
    err: TextIO = sys.stderr,
    clock: Callable[[], datetime.date] = datetime.date.today,
    configure_fn=engine.configure,
) -> int:
    output = None
    try:
        seat = choose_seat(ask, out)
        source = Path(ask("Template agent directory: ").strip()).expanduser().resolve()
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

        actual_source = output if output.exists() else source
        while True:
            try:
                configure_fn(actual_source, answers, output, seat, clock=clock, seat_registry={})
                break
            except engine.IntakeRejected as exc:
                editable = answer_field_map(answers)
                render_rejection(exc, err, editable)
                if not fix_named_answer(answers, exc.failures, ask, editable):
                    return 2
                actual_source = output if output.exists() else source
        print(f"Configured agent: {output}", file=out)
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Guided AscendOps PMAgents setup")
    parser.parse_args()
    return run_setup()


if __name__ == "__main__":
    raise SystemExit(main())
