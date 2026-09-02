"""Mapping-table-driven managed placeholder application and rerun."""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
import json, math, re, value_extractors
from pathlib import Path

TOKEN = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")
PRESERVED_RUNTIME_TOKENS = {"CTX_ROOT"}
UNRESOLVED_MARKER = re.compile(r"\[NEEDS-(?:D[A-Z]{4}|CONFIRM)\]", re.I)
SUPPORTED_EXTRACTORS = {
    "currency", "emergency_minutes", "first_integer", "first_person", "labeled_integer",
    "labeled_text", "identity", "literal", "maintenance_platform", "window_end", "window_start",
}


class PlaceholderRejected(RuntimeError):
    def __init__(self, failures):
        self.failures = failures
        super().__init__("placeholder integrity rejected")


def load_mapping(path: Path):
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise PlaceholderRejected([("mapping", "mapping document must be an object")])
    schema_version = data.get("schema_version", 1)
    if not isinstance(schema_version, int) or schema_version < 1:
        raise PlaceholderRejected([("mapping.schema_version", "schema version must be a positive integer")])
    rows = data.get("placeholders", [])
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise PlaceholderRejected([("mapping.placeholders", "must be a list of row objects")])
    names = [row.get("placeholder") for row in rows]
    if not rows or len(names) != len(set(names)):
        raise PlaceholderRejected([("mapping", "placeholder rows are missing or duplicated")])
    config_rows = data.get("config_keys", [])
    if not isinstance(config_rows, list) or any(not isinstance(row, dict) for row in config_rows):
        raise PlaceholderRejected([("mapping.config_keys", "must be a list of row objects")])
    if data.get("cross_seat") is not None and not isinstance(data["cross_seat"], dict):
        raise PlaceholderRejected([("mapping.cross_seat", "must be an object")])
    config_paths = [row.get("path") for row in config_rows]
    failures = []
    if len(config_paths) != len(set(config_paths)):
        failures.append(("mapping.config_keys", "config-key paths are duplicated"))
    for row in config_rows:
        if not isinstance(row.get("path"), str) or not row["path"].startswith("/"):
            failures.append(("mapping.config_keys", "config-key path must be an RFC6901 pointer"))
        target = row.get("file", "config.json")
        if (not isinstance(target, str) or "/" in target or "\\" in target
                or target in {"", ".", ".."} or not target.endswith(".json")):
            failures.append((f"mapping.config_keys.{row.get('path')}",
                             "file must be a bare .json filename in the seat root"))
        elif "file" in row and row.get("value_from") == "pointer":
            failures.append((f"mapping.config_keys.{row.get('path')}",
                             "file is not supported on pointer rows"))
        if row.get("mode", "replace") not in {"replace", "create"}:
            failures.append((f"mapping.config_keys.{row.get('path')}", "mode must be replace or create"))
        if row.get("value_type", "string") not in {"string", "integer", "number", "boolean"}:
            failures.append((f"mapping.config_keys.{row.get('path')}", "unsupported value_type"))
        kind = row.get("value_type", "string")
        for bound in ("minimum", "maximum"):
            if bound not in row:
                continue
            value = row[bound]
            if kind not in {"integer", "number"}:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 f"{bound} is only valid for numeric value types"))
            elif isinstance(value, bool) or not isinstance(value, (int, float)):
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 f"{bound} must be a number"))
            elif not math.isfinite(value):
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 f"{bound} must be finite"))
        if (isinstance(row.get("minimum"), (int, float))
                and not isinstance(row.get("minimum"), bool)
                and isinstance(row.get("maximum"), (int, float))
                and not isinstance(row.get("maximum"), bool)
                and row["minimum"] > row["maximum"]):
            failures.append((f"mapping.config_keys.{row.get('path')}",
                             "minimum must not exceed maximum"))
        if row.get("value_from") not in {None, "pointer"}:
            failures.append((f"mapping.config_keys.{row.get('path')}", "value_from must be pointer"))
        if row.get("value_from") == "pointer" and not isinstance(row.get("pointer_name"), str):
            failures.append((f"mapping.config_keys.{row.get('path')}", "pointer_name is required"))
        if row.get("value_from") == "pointer":
            extractor = row.get("extractor")
            if extractor is not None and extractor not in {"window_start", "window_end"}:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 "pointer extractor must be window_start or window_end"))
            if "fallback" in row and row.get("fallback_from") == "holding_answer":
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 "literal fallback and holding-answer fallback are mutually exclusive"))
            if row.get("fallback_from") not in {None, "holding_answer"}:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 "fallback_from must be holding_answer"))
        else:
            extractor = row.get("extractor")
            if extractor not in SUPPORTED_EXTRACTORS:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 f"unknown extractor {extractor!r}"))
            if extractor == "literal" and not isinstance(row.get("value"), str):
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 "literal extractor requires a string value"))
            if extractor != "literal" and not isinstance(row.get("source"), str):
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 "row requires a source (only literal rows derive from no answer)"))
            if extractor == "literal" and "source" in row:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 "literal rows derive from no answer and must not carry a source"))
            if (extractor in {"labeled_integer", "labeled_text"}
                    and (not isinstance(row.get("label"), str) or not row["label"].strip())):
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 f"{extractor} requires a string label"))
    if schema_version >= 2:
        timezone_rows = [row for row in config_rows if row.get("path") == "/timezone"]
        if len(timezone_rows) != 1:
            failures.append(("mapping.config_keys./timezone",
                             "schema v2+ requires exactly one timezone config-key row"))
        elif not ((timezone_rows[0].get("source") == "cover.timezone"
                   and timezone_rows[0].get("extractor") == "identity"
                   and timezone_rows[0].get("value_type", "string") == "string")
                  or (timezone_rows[0].get("value_from") == "pointer"
                      and isinstance(timezone_rows[0].get("pointer_name"), str)
                      and timezone_rows[0].get("value_type", "string") == "string")):
            failures.append(("mapping.config_keys./timezone",
                             "timezone row must source cover.timezone or a declared pointer as a string"))
    for row in rows:
        extractor = row.get("extractor")
        if extractor not in SUPPORTED_EXTRACTORS:
            failures.append((f"mapping.{row.get('placeholder')}",
                             f"unknown extractor {extractor!r}"))
        if extractor == "literal" and not isinstance(row.get("value"), str):
            failures.append((f"mapping.{row.get('placeholder')}",
                             "literal extractor requires a string value"))
        if extractor != "literal" and not isinstance(row.get("source"), str):
            failures.append((f"mapping.{row.get('placeholder')}",
                             "row requires a source (only literal rows derive from no answer)"))
        if extractor == "literal" and "source" in row:
            failures.append((f"mapping.{row.get('placeholder')}",
                             "literal rows derive from no answer and must not carry a source"))
        if (extractor in {"labeled_integer", "labeled_text"}
                and (not isinstance(row.get("label"), str) or not row["label"].strip())):
            failures.append((f"mapping.{row.get('placeholder')}",
                             f"{extractor} requires a string label"))
        sites = row.get("sites")
        if sites is None:
            continue
        if not isinstance(sites, list) or not sites:
            failures.append((f"mapping.{row.get('placeholder')}", "sites must be a nonempty list"))
            continue
        seen = set()
        for site in sites:
            identity = (site.get("file"), site.get("count")) if isinstance(site, dict) else None
            if (not isinstance(site, dict) or not isinstance(site.get("file"), str)
                    or site.get("file", "").startswith("/") or ".." in Path(site.get("file", "")).parts
                    or not isinstance(site.get("count"), int) or site.get("count") < 1):
                failures.append((f"mapping.{row.get('placeholder')}", "site requires safe relative file and positive count"))
            elif identity in seen:
                failures.append((f"mapping.{row.get('placeholder')}", "site declarations are duplicated"))
            else:
                seen.add(identity)
    if failures:
        raise PlaceholderRejected(failures)
    return data


def _number(value, *, integer=False):
    match = re.search(r"\$([0-9][0-9,]*(?:\.\d+)?)(?!\.\d|\d)", value)
    if not match:
        match = re.search(
            r"([0-9][0-9,]*(?:\.\d+)?)(?!\.\d|\d)\s*(?:base\s+)?threshold",
            value,
            re.I,
        )
    if not match: raise ValueError("currency value not found")
    # A comma immediately after the amount may be sentence punctuation; internal
    # commas remain part of the token and must use canonical thousands grouping.
    raw_token = match.group(1).rstrip(",")
    integer_token = raw_token.partition(".")[0]
    if "," in integer_token and not re.fullmatch(r"\d{1,3}(?:,\d{3})*", integer_token):
        raise ValueError("currency value must use standard comma grouping")
    token = raw_token.replace(",", "")
    try:
        number = Decimal(token)
    except InvalidOperation:
        return token
    if number == number.to_integral_value():
        return str(int(number))
    if integer:
        raise ValueError("currency threshold must be stated in whole dollars")
    return token


def _question_id(row):
    """Manifest provenance for a row: its source, or "literal" for a row that derives from no answer."""
    return row["source"] if "source" in row else "literal"


def extract(row, cover, answers, core):
    kind = row["extractor"]
    if kind == "literal":
        return row["value"]
    source = row["source"]
    raw = cover[source.split(".", 1)[1]] if source.startswith("cover.") else answers[source]
    value = core.provenance_value(raw, source)
    return extract_value(row, value, core)


def extract_value(row, value, core):
    """Apply a declared extractor to an already-resolved scalar value."""
    kind = row["extractor"]
    if kind == "identity": return value
    if kind == "currency": return _number(value, integer=row.get("value_type") == "integer")
    if kind == "first_integer":
        match = re.search(r"[-+]?\d[\d,]*", value)
        if not match: raise ValueError("integer value not found")
        return match.group(0).replace(",", "")
    if kind == "labeled_integer":
        label = row["label"]
        matches = list(re.finditer(
            rf"^\s*{re.escape(label)}\s*:\s*([-+]?\d[\d,]*)\s*$",
            value,
            re.I | re.M,
        ))
        if not matches:
            raise ValueError(f"labeled integer line {label!r}: NN not found")
        if len(matches) > 1:
            raise ValueError(f"labeled integer line {label!r}: NN appears more than once")
        return matches[0].group(1).replace(",", "")
    if kind == "emergency_minutes":
        match = re.search(r"Emergency\s+dispatch(?:\s+within)?\s+(\d+)\s+minutes?", value, re.I)
        if not match: raise ValueError("Emergency dispatch minutes not found")
        return match.group(1)
    if kind == "labeled_text":
        # Mirrors labeled_integer for prose values: exactly one line of the form
        # "<label>: <text>" in the answer, text taken verbatim to end of line.
        # Missing or duplicated label rejects BY NAME (fail-closed) rather than
        # letting a whole multi-paragraph answer flow into a single-value slot.
        label = row["label"]
        pattern = re.compile(rf"^\s*{re.escape(label)}\s*:\s*(.+?)\s*$", re.M)
        matches = list(pattern.finditer(value))
        if not matches:
            raise ValueError(f"labeled text line {label!r}: not found")
        if len(matches) > 1:
            raise ValueError(f"labeled text line {label!r}: appears more than once")
        return matches[0].group(1)
    if kind == "first_person": return re.split(r"[,;]", value, maxsplit=1)[0].strip()
    if kind == "maintenance_platform":
        return value_extractors.maintenance_platform(value)
    if kind in {"window_start", "window_end"}:
        start, end = core.times(value)
        return start if kind.endswith("start") else end
    raise ValueError(f"unknown extractor {kind}")


def _text_files(root):
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.name != "seat-config.json":
            try: path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError): continue
            yield path


def _pointer_parts(pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("JSON pointer must start with /")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]


def _pointer_parent(data, pointer, *, create=False):
    parts = _pointer_parts(pointer)
    if not parts:
        raise ValueError("JSON pointer cannot target the document root")
    node = data
    for part in parts[:-1]:
        if isinstance(node, list):
            node = node[int(part)]
        elif isinstance(node, dict):
            if part not in node:
                if not create:
                    raise KeyError(part)
                node[part] = {}
            node = node[part]
        else:
            raise TypeError("JSON pointer traverses a scalar")
    leaf = int(parts[-1]) if isinstance(node, list) else parts[-1]
    return node, leaf


def _typed_value(row, value):
    if UNRESOLVED_MARKER.search(str(value)):
        raise ValueError("unresolved answer must be confirmed before configuration")
    kind = row.get("value_type", "string")
    try:
        if kind == "string":
            return str(value)
        if kind == "integer":
            if not re.fullmatch(r"[-+]?\d+", str(value).strip()):
                raise ValueError("not an integer")
            typed = int(value)
            return _validate_numeric_domain(row, typed)
        if kind == "number":
            typed = float(value)
            return _validate_numeric_domain(row, typed)
        if kind == "boolean":
            if str(value).strip().lower() not in {"true", "false"}:
                raise ValueError("not true or false")
            return str(value).strip().lower() == "true"
    except (TypeError, ValueError) as exc:
        raise ValueError(f"cannot coerce {value!r} to {kind}: {exc}") from exc
    raise ValueError(f"unsupported value_type {kind}")


def _validate_numeric_domain(row, value):
    if not math.isfinite(value):
        raise ValueError(f"value {value!r} must be finite")
    if "minimum" in row and value < row["minimum"]:
        raise ValueError(f"value {value!r} is below minimum {row['minimum']!r}")
    if "maximum" in row and value > row["maximum"]:
        raise ValueError(f"value {value!r} is above maximum {row['maximum']!r}")
    return value


def validate_consumed_values(mapping, raw_cover, raw_answers):
    """Reject unresolved intake values consumed by mapping activation surfaces."""
    failures = []
    seen = set()
    rows = list(mapping.get("placeholders", [])) + [
        row for row in mapping.get("config_keys", []) if row.get("value_from") != "pointer"
    ]
    for row in rows:
        if row.get("extractor") == "literal":
            continue
        source = row.get("source")
        if not isinstance(source, str) or source in seen:
            continue
        seen.add(source)
        value = (raw_cover.get(source.split(".", 1)[1])
                 if source.startswith("cover.") else raw_answers.get(source))
        if value is not None and UNRESOLVED_MARKER.search(value):
            failures.append((
                source,
                "configuration incomplete: replace the unresolved marker with a confirmed answer and rerun setup",
            ))
    if failures:
        raise PlaceholderRejected(failures)


def _row_target(row):
    """Target JSON file of a mapping config row (bare filename in the seat root)."""
    return row.get("file", "config.json")


def _item_target(item):
    """Target JSON file of a managed config_key manifest item.

    Items without "config_file" (pointer rows, manifests written before file
    targeting existed) commit to config.json; the display "file" field is
    "<filename>#<pointer>" and is never parsed.
    """
    return item.get("config_file", "config.json")


def _plan_config_keys_initial(root, mapping, cover, answers, core):
    rows = [row for row in mapping.get("config_keys", []) if row.get("value_from") != "pointer"]
    if not rows:
        return []
    data_by_file = {}
    for row in rows:
        filename = _row_target(row)
        if filename in data_by_file:
            continue
        path = root / filename
        if not path.is_file():
            raise PlaceholderRejected([("mapping.config_keys", f"{filename} is missing")])
        data_by_file[filename] = json.loads(path.read_text())
    manifest = []
    failures = []
    for row in rows:
        pointer = row["path"]
        filename = _row_target(row)
        data = data_by_file[filename]
        try:
            node, leaf = _pointer_parent(data, pointer, create=row.get("mode", "replace") == "create")
            exists = ((isinstance(node, list) and isinstance(leaf, int) and 0 <= leaf < len(node))
                      or (isinstance(node, dict) and leaf in node))
            if not exists and row.get("mode", "replace") != "create":
                raise KeyError("declared replace target is absent")
            value = _typed_value(row, extract(row, cover, answers, core))
            if isinstance(node, list) and not exists:
                raise IndexError("create mode cannot extend arrays")
            item = {
                "row_type": "config_key",
                "config_path": pointer,
                "question_id": _question_id(row),
                "file": filename + "#" + pointer,
                "count": 1,
                "value": value,
            }
            if filename != "config.json":
                # Only non-default targets are recorded, so seats that never
                # leave config.json keep byte-identical manifests and goldens.
                item["config_file"] = filename
            manifest.append(item)
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            failures.append((f"mapping.config_keys.{pointer}", str(exc)))
    if failures:
        raise PlaceholderRejected(failures)
    return manifest


def _commit_config_keys(root, manifest, *, mode_by_path=None):
    """Write resolved config rows into their target files (one load and one write per file).

    Items name their target with "config_file"; items without one (pointer rows,
    manifests written before file targeting existed) commit to config.json.
    """
    if not manifest:
        return
    mode_by_path = mode_by_path or {}
    groups = {}
    for item in manifest:
        groups.setdefault(_item_target(item), []).append(item)
    for filename, items in groups.items():
        path = root / filename
        if not path.is_file():
            raise PlaceholderRejected([("mapping.config_keys", f"{filename} is missing")])
        data = json.loads(path.read_text())
        for item in items:
            pointer = item["config_path"]
            mode = mode_by_path.get((filename, pointer), item.get("mode", "replace"))
            try:
                node, leaf = _pointer_parent(data, pointer, create=mode == "create")
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                if isinstance(exc, KeyError) and exc.args:
                    detail = f"missing parent segment {exc.args[0]!r}"
                else:
                    detail = f"parent traversal failed: {exc}"
                raise PlaceholderRejected([
                    (f"mapping.config_keys.{pointer}", detail)
                ]) from exc
            exists = ((isinstance(node, list) and isinstance(leaf, int) and 0 <= leaf < len(node))
                      or (isinstance(node, dict) and leaf in node))
            if not exists and mode != "create":
                raise PlaceholderRejected([
                    (f"mapping.config_keys.{pointer}", "declared replace target is absent")
                ])
            if isinstance(node, list):
                if not exists:
                    raise PlaceholderRejected([
                        (f"mapping.config_keys.{pointer}", "create mode cannot extend arrays")
                    ])
                node[leaf] = item["value"]
            else:
                node[leaf] = item["value"]
        path.write_text(json.dumps(data, indent=2) + "\n")


def commit_config_manifest(root: Path, manifest):
    """Commit pre-resolved config rows to their staged target files."""
    _commit_config_keys(root, manifest)


def apply_initial(root: Path, mapping, cover, answers, core):
    rows = {row["placeholder"]: row for row in mapping["placeholders"]}
    occurrences = {name: [] for name in rows}
    unknown = []
    for path in _text_files(root):
        text = path.read_text()
        for name in TOKEN.findall(text):
            if name in rows: occurrences[name].append(path)
            elif name in PRESERVED_RUNTIME_TOKENS: continue
            else: unknown.append((str(path.relative_to(root)), name))
    failures = [(f"template.{path}", f"unknown placeholder {{{{{name}}}}} has no mapping row") for path, name in unknown]
    for name, paths in occurrences.items():
        if not paths: failures.append((f"mapping.{name}", f"P-row placeholder {{{{{name}}}}} is absent from template"))
    for name, row in rows.items():
        for site in row.get("sites", []):
            path = root / site["file"]
            count = path.read_text().count("{{" + name + "}}") if path.is_file() else 0
            if count != site["count"]:
                failures.append((f"mapping.{name}.site.{site['file']}",
                                 f"expected {site['count']} occurrence(s), found {count}"))
    values = {}
    for name, row in rows.items():
        try:
            values[name] = extract(row, cover, answers, core)
        except (KeyError, TypeError, ValueError) as exc:
            failures.append((f"mapping.{name}", f"value extraction failed: {exc}"))
    if failures: raise PlaceholderRejected(failures)
    config_manifest = _plan_config_keys_initial(root, mapping, cover, answers, core)
    manifest = []
    for name, row in rows.items():
        value = values[name]
        for path in sorted(set(occurrences[name])):
            relative = str(path.relative_to(root)); token = "{{" + name + "}}"
            if path.suffix == ".json":
                data = json.loads(path.read_text())
                pointers = []
                def walk(node, pointer=""):
                    if isinstance(node, dict):
                        for key, child in node.items(): node[key] = walk(child, pointer + "/" + key.replace("~", "~0").replace("/", "~1"))
                    elif isinstance(node, list):
                        for index, child in enumerate(node): node[index] = walk(child, pointer + f"/{index}")
                    elif isinstance(node, str) and token in node:
                        count = node.count(token); pointers.extend([pointer] * count); return node.replace(token, value)
                    return node
                data = walk(data); path.write_text(json.dumps(data, indent=2) + "\n")
                for pointer in pointers:
                    manifest.append({"placeholder": name, "question_id": _question_id(row), "file": relative + "#" + pointer, "count": 1, "value": value})
            else:
                text = path.read_text(); count = text.count(token)
                marker = f"<!-- BETTY-PH:{name} -->{value}<!-- /BETTY-PH:{name} -->"
                path.write_text(text.replace(token, marker))
                manifest.append({"placeholder": name, "question_id": _question_id(row), "file": relative, "count": count, "value": value})
    _commit_config_keys(
        root,
        config_manifest,
        mode_by_path={(_row_target(row), row["path"]): row.get("mode", "replace")
                      for row in mapping.get("config_keys", [])},
    )
    manifest.extend(config_manifest)
    return manifest


def preserved_runtime_manifest(root: Path):
    records = []
    for path in _text_files(root):
        text = path.read_text()
        for name in sorted(PRESERVED_RUNTIME_TOKENS):
            token = "{{" + name + "}}"; count = text.count(token)
            if count:
                records.append({"token": token, "file": str(path.relative_to(root)), "count": count})
    return records


def verify_preserved_runtime_tokens(root: Path, records):
    failures = []
    for item in records:
        if item.get("token") != "{{CTX_ROOT}}":
            failures.append(("preserved-token", f"unclassified preserved token in manifest: {item.get('token')!r}")); continue
        path = root / item["file"]
        if not path.is_file() or path.read_text().count(item["token"]) != item["count"]:
            failures.append(("preserved-token", f"preserved runtime token changed in {item['file']}"))
    if failures: raise PlaceholderRejected(failures)
    return records


def apply_rerun(root: Path, mapping, cover, answers, core, old_manifest):
    rows = {row["placeholder"]: row for row in mapping["placeholders"]}
    failures = []
    new_manifest = []
    for item in old_manifest:
        if item.get("row_type") == "compatibility_guard":
            new_manifest.append(item)
            continue
        if item.get("row_type") == "config_key":
            pointer = item.get("config_path")
            filename = _item_target(item)
            row = next((candidate for candidate in mapping.get("config_keys", [])
                        if candidate.get("path") == pointer and _row_target(candidate) == filename), None)
            if row is None:
                failures.append((f"manifest.config_key.{pointer}", "managed config key no longer has a mapping row")); continue
            path = root / filename
            try:
                data = json.loads(path.read_text())
                node, leaf = _pointer_parent(data, pointer)
                current = node[leaf]
                if current != item.get("value"):
                    raise ValueError("managed config value changed outside the engine")
                if row.get("value_from") == "pointer":
                    # Cross-seat state must be rebuilt before resolving this row.
                    # The initial and rerun paths therefore share one resolver.
                    continue
                value = _typed_value(row, extract(row, cover, answers, core))
                node[leaf] = value
                path.write_text(json.dumps(data, indent=2) + "\n")
                new_manifest.append({**item, "question_id": _question_id(row), "value": value})
            except (OSError, json.JSONDecodeError, KeyError, IndexError, TypeError, ValueError) as exc:
                failures.append((f"manifest.config_key.{pointer}", f"managed JSON pointer changed: {exc}"))
            continue
        name = item.get("placeholder"); row = rows.get(name)
        if row is None:
            failures.append((f"manifest.{name}", "managed placeholder no longer has a mapping row")); continue
        file_name, separator, pointer = item["file"].partition("#")
        path = root / file_name
        if not path.is_file():
            failures.append((f"manifest.{name}", f"managed file is missing: {item['file']}")); continue
        try:
            value = extract(row, cover, answers, core)
        except (KeyError, TypeError, ValueError) as exc:
            failures.append((f"manifest.{name}", f"value extraction failed: {exc}"))
            continue
        if separator:
            data = json.loads(path.read_text()); node = data
            parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
            try:
                for part in parts[:-1]: node = node[int(part)] if isinstance(node, list) else node[part]
                leaf = int(parts[-1]) if isinstance(node, list) else parts[-1]
                current = node[leaf]
                if not isinstance(current, str) or item["value"] not in current: raise ValueError("prior value missing")
                node[leaf] = current.replace(item["value"], value, 1)
                path.write_text(json.dumps(data, indent=2) + "\n")
            except (KeyError, IndexError, ValueError, TypeError) as exc:
                failures.append((f"manifest.{name}", f"managed JSON pointer changed in {item['file']}: {exc}")); continue
        else:
            text = path.read_text(); old = re.escape(item["value"])
            pattern = re.compile(rf"<!-- BETTY-PH:{re.escape(name)} -->{old}<!-- /BETTY-PH:{re.escape(name)} -->")
            if len(pattern.findall(text)) != item["count"]:
                failures.append((f"manifest.{name}", f"managed delimiter count changed in {item['file']}")); continue
            replacement = f"<!-- BETTY-PH:{name} -->{value}<!-- /BETTY-PH:{name} -->"
            path.write_text(pattern.sub(lambda _: replacement, text))
        new_manifest.append({**item, "question_id": _question_id(row), "value": value})
    if failures: raise PlaceholderRejected(failures)
    return new_manifest
