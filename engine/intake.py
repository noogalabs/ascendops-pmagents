"""Complete, write-free questionnaire intake validation for the Betty glue wrapper."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


PROVENANCE = {"documented", "inferred", "NEEDS-DAVID"}
COVER_FIELDS = {
    "Company name": "company_name",
    "Org short-name": "org_short_name",
    "Forward email": "forward_email",
    "Timezone": "timezone",
    "Autonomy mode": "autonomy_mode",
    "Unlock window": "unlock_window",
    "Qualifying accuracy": "qualifying_accuracy",
}
QUESTION_ID_PATTERN = r"[A-Z]\d+"
QUESTION_ID = re.compile(rf"^{QUESTION_ID_PATTERN}$")
QUESTION_LINE = re.compile(rf"^({QUESTION_ID_PATTERN})\.\s")
QUESTION_HEADING = re.compile(rf"^({QUESTION_ID_PATTERN})\.\s+(.+)$", re.M)
CONTINUATION_LINE = re.compile(r"^[ \t]+(?:\S[^\n]*)?$")
INTAKE_VALUE_SPAN = r"[^\n]*(?:\n[ \t]+[^\n]*)*"
TERMINAL_PUNCTUATION_RUN = r"[.,;:!?)\]}\"'’”…]*"
STRUCTURED_DAY_COUNT_LINE = re.compile(
    r"\s*[^:\n]+?\s*(?::|[-–—])\s*\d+\s+(?:(?:calendar|business)\s+)?days?"
    r"\s*",
    re.I,
)
US_JURISDICTION_NAMES = (
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming", "District of Columbia",
    "Puerto Rico", "American Samoa", "Guam", "Northern Mariana Islands",
    "United States Virgin Islands", "US Virgin Islands", "U.S. Virgin Islands",
    "United States Minor Outlying Islands",
)
US_JURISDICTION_NAME = re.compile(
    rf"(?<!\w)(?:{'|'.join(re.escape(name) for name in US_JURISDICTION_NAMES)}|D\.?C\.?)(?!\w)",
    re.I,
)
def _normalize_accounting_clock_answer(answer: str) -> str:
    return "\n".join(
        re.sub(rf"\s*{TERMINAL_PUNCTUATION_RUN}\s*$", "", line)
        for line in answer.splitlines()
    )


def _is_closed_vocabulary_grace_clock(line: str) -> bool:
    has_jurisdiction_subject = bool(
        US_JURISDICTION_NAME.search(line)
        or re.search(r"\b(?:county|parish|city|state|jurisdiction)\b", line, re.I)
    )
    has_grace_concept = bool(re.search(r"\bgrace\b", line, re.I))
    has_integer_duration = bool(
        re.search(r"\b\d+\s+(?:(?:calendar|business)\s+)?days?\b", line, re.I)
    )
    return has_jurisdiction_subject and has_grace_concept and has_integer_duration

class IntakeRejected(RuntimeError):
    def __init__(self, failures: list[tuple[str, str]]):
        self.failures = failures
        super().__init__("questionnaire rejected")

    def render(self) -> str:
        return "\n".join(
            ["REJECT LIST — no agent files were written"]
            + [f"- {field}: {reason}" for field, reason in self.failures]
        )


@dataclass(frozen=True)
class IntakeResult:
    text: str
    cover: dict[str, str]
    answers: dict[str, str]
    raw_cover: dict[str, str]
    raw_answers: dict[str, str]
    provenance: dict[str, str]


def indented_value(lines: list[str], index: int, initial: str) -> str:
    """Read one intake value plus its canonical indented continuation lines."""
    value_lines = [initial.strip()]
    cursor = index + 1
    while cursor < len(lines) and CONTINUATION_LINE.match(lines[cursor]):
        value_lines.append(lines[cursor].strip())
        cursor += 1
    return "\n".join(value_lines).strip()


def _tagged(raw: str, field: str, failures: list[tuple[str, str]]):
    match = re.match(r"^\s*\[([^]]+)\]\s*(.*)$", raw, re.S)
    if not match:
        return raw, "untagged"
    tag, value = match.groups()
    if tag not in PROVENANCE:
        failures.append((field, f"unknown provenance tag [{tag}]; human confirmation is required"))
        return value, f"unknown:{tag}"
    return (raw if tag == "NEEDS-DAVID" else value), tag


def _number(pattern: str, value: str):
    match = re.search(pattern, value, re.I)
    if not match:
        return None
    token = next((item for item in match.groupdict().values() if item is not None), None)
    return float(token.replace(",", "")) if token is not None else None


def _bounded(field: str, value: str, pattern: str, low: float, high: float, label: str,
             failures: list[tuple[str, str]]):
    number = _number(pattern, value)
    if number is None or not low <= number <= high:
        failures.append((field, f"{label} must be explicit and from {low:g} through {high:g}"))


def _validate_semantics(answers: dict[str, str], raw: dict[str, str], failures: list[tuple[str, str]]):
    confirmed = {q: v for q, v in answers.items() if "NEEDS-DAVID" not in raw.get(q, "")}
    if "B1" in confirmed:
        _bounded("B1", confirmed["B1"], r"(?:\$(?P<n>[\d,]+(?:\.\d+)?)\s*(?:base|owner)|(?:base|owner)[^\n;$]{0,40}\$(?P<n2>[\d,]+(?:\.\d+)?))", 0, 1_000_000, "base currency threshold", failures)
        # The alternate named group is normalized here without falling back to an unrelated numeral.
        if failures and failures[-1][0] == "B1":
            alt = re.search(r"(?:base|owner)[^\n;$]{0,40}\$([\d,]+(?:\.\d+)?)", confirmed["B1"], re.I)
            if alt and 0 <= float(alt.group(1).replace(",", "")) <= 1_000_000:
                failures.pop()
    for q, high in (("B2", 1_000_000), ("B3", 100_000)):
        if q in confirmed:
            _bounded(q, confirmed[q], r"\$(?P<n>[\d,]+(?:\.\d+)?)", 0, high, "currency value", failures)
    if "B4" in confirmed:
        _bounded("B4", confirmed["B4"], r"(?P<n>[\d,]+(?:\.\d+)?)\s*(?:%|percent\b)", 0, 100, "percentage", failures)
    if "B11" in confirmed:
        low = _number(r"(?:below|under|low(?:\s+score)?(?:\s+is)?)\s*(?P<n>\d+(?:\.\d+)?)", confirmed["B11"])
        target = _number(r"(?:target|average(?:\s+is)?)\D{0,20}(?P<n>\d+(?:\.\d+)?)", confirmed["B11"])
        if low is None or target is None or not (0 <= low <= 5 and 0 <= target <= 5):
            failures.append(("B11", "low-score and target values must both be explicit and from 0 through 5"))

    for question, flag in (("A4", "CERTIFIED-MAIL-CONFIRMED"), ("B3", "LEASE-CLAUSE-CONFIRMED"), ("B6", "SILENCE-CLAUSE-CONFIRMED")):
        if question not in confirmed:
            continue
        mentions = re.findall(rf"\b{flag}\s*=\s*([^\s;,.]+)", confirmed[question], re.I)
        valid = [v.lower() for v in mentions if v.lower() in {"true", "false"}]
        if len(mentions) != 1 or len(valid) != 1:
            failures.append((question, f"requires exactly one {flag}=true|false value"))
            continue
        if question == "A4":
            answer = re.match(r"\s*(yes|no)\b", confirmed[question], re.I)
            if answer is None:
                failures.append((question, "enum must begin with yes or no"))
            elif (answer.group(1).lower() == "yes") != (valid[0] == "true"):
                failures.append((question, f"yes/no answer contradicts {flag}={valid[0]}"))

    if "B8" in confirmed and not re.search(r"\d{1,2}:\d{2}\s*(?:[-–]|to)\s*\d{1,2}:\d{2}", confirmed["B8"], re.I):
        failures.append(("B8", "requires an HH:MM-HH:MM communications window"))
    if "D9" in confirmed:
        match = re.fullmatch(r"\s*Friday\s+(\d{2}):(\d{2})\s+destination:\s*(.+?)\s*;\s*Monday\s+(\d{2}):(\d{2})\s+destination:\s*(.+?)\s*", confirmed["D9"], re.I)
        if not match:
            failures.append(("D9", "requires Friday HH:MM destination: ...; Monday HH:MM destination: ..."))
        elif any(int(v) > limit for v, limit in zip((match.group(1), match.group(2), match.group(4), match.group(5)), (23, 59, 23, 59))):
            failures.append(("D9", "report time is outside 00:00-23:59"))


def _validate_accounting_scope(answers: dict[str, str], failures: list[tuple[str, str]]):
    answer = answers.get("A1", "")
    lines = _normalize_accounting_clock_answer(answer).splitlines()
    canonical_pattern = re.compile(r"\s*Late fee grace days\s*:\s*\d+\s*", re.I)
    canonical = [line for line in lines if canonical_pattern.fullmatch(line)]
    scoped = [line for line in lines if (
        (re.search(r"\blate fee grace days\b", line, re.I)
         and re.search(r":\s*\d+\s*$", line)
         and not canonical_pattern.fullmatch(line))
        or (re.search(r"\blate fee grace\b", line, re.I)
            and re.search(r"\b\d+\b", line)
            and re.search(r"\bdays?\b", line, re.I)
            and not canonical_pattern.fullmatch(line))
        or _is_closed_vocabulary_grace_clock(line)
        or STRUCTURED_DAY_COUNT_LINE.fullmatch(line)
        or re.fullmatch(
            r"\s*.+\b(?:county|parish|city|state|jurisdiction)\s*:\s*\d+\s+days\s*",
            line,
            re.I,
        )
    )]
    if len(canonical) != 1 or scoped:
        failures.append((
            "A1",
            "A1 accepts exactly one structured day-count line (Late fee grace days: NN). "
            "Additional label: N day(s) lines, including calendar/business qualifiers, "
            "are ambiguous—state other timing details as "
            "plain prose, or wait for the tracked per-jurisdiction capability.",
        ))


def preflight(path: Path, question_ids: list[str], *, cover_fields=None,
              semantic_profile: str = "maintenance") -> IntakeResult:
    failures: list[tuple[str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise IntakeRejected([("file", f"cannot read questionnaire as UTF-8: {exc}")]) from exc

    raw_cover: dict[str, str] = {}
    active_cover_fields = COVER_FIELDS if cover_fields is None else cover_fields
    for label, key in active_cover_fields.items():
        hits = []
        lines = text.splitlines()
        for index, line in enumerate(lines):
            match = re.match(rf"^{re.escape(label)}:\s*(.*)$", line)
            if not match:
                continue
            hits.append(indented_value(lines, index, match.group(1)))
        if len(hits) != 1 or not (hits[0].strip(" _") if hits else ""):
            failures.append((f"cover.{label}", "required exactly once with a nonblank value"))
        elif hits:
            raw_cover[key] = hits[0].strip()

    raw_answers: dict[str, str] = {}
    counts: dict[str, int] = {}
    current = None
    lines = text.splitlines()
    for index, line in enumerate(lines):
        question = QUESTION_LINE.match(line)
        if question:
            current = question.group(1)
        elif current and line.startswith("Answer:"):
            counts[current] = counts.get(current, 0) + 1
            raw_answers.setdefault(
                current,
                indented_value(lines, index, line.partition(":")[2]),
            )
    declared_questions = set(question_ids)
    for question in sorted(set(counts) - declared_questions):
        failures.append((question, "question id is not declared for this edition"))
    for question in question_ids:
        if counts.get(question) != 1:
            failures.append((question, "requires exactly one Answer line"))
        elif not raw_answers.get(question, "").strip(" _"):
            failures.append((question, "required answer is blank"))

    provenance: dict[str, str] = {}
    cover: dict[str, str] = {}
    answers: dict[str, str] = {}
    for key, value in raw_cover.items():
        cover[key], provenance[f"cover.{key}"] = _tagged(value, f"cover.{key}", failures)
    for question, value in raw_answers.items():
        answers[question], provenance[question] = _tagged(value, question, failures)
    if semantic_profile == "maintenance":
        _validate_semantics(answers, raw_answers, failures)
    elif semantic_profile == "accounting":
        _validate_accounting_scope(answers, failures)
    if failures:
        raise IntakeRejected(failures)
    return IntakeResult(text, cover, answers, raw_cover, raw_answers, provenance)
