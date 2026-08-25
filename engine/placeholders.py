"""Mapping-table-driven managed placeholder application and rerun."""
from __future__ import annotations
import json, re
from pathlib import Path

TOKEN = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")
PRESERVED_RUNTIME_TOKENS = {"CTX_ROOT"}


class PlaceholderRejected(RuntimeError):
    def __init__(self, failures):
        self.failures = failures
        super().__init__("placeholder integrity rejected")


def load_mapping(path: Path):
    data = json.loads(path.read_text())
    schema_version = data.get("schema_version", 1)
    if not isinstance(schema_version, int) or schema_version < 1:
        raise PlaceholderRejected([("mapping.schema_version", "schema version must be a positive integer")])
    rows = data.get("placeholders", [])
    names = [row.get("placeholder") for row in rows]
    if not rows or len(names) != len(set(names)):
        raise PlaceholderRejected([("mapping", "placeholder rows are missing or duplicated")])
    config_rows = data.get("config_keys", [])
    config_paths = [row.get("path") for row in config_rows]
    failures = []
    if len(config_paths) != len(set(config_paths)):
        failures.append(("mapping.config_keys", "config-key paths are duplicated"))
    for row in config_rows:
        if not isinstance(row.get("path"), str) or not row["path"].startswith("/"):
            failures.append(("mapping.config_keys", "config-key path must be an RFC6901 pointer"))
        if row.get("mode", "replace") not in {"replace", "create"}:
            failures.append((f"mapping.config_keys.{row.get('path')}", "mode must be replace or create"))
        if row.get("value_type", "string") not in {"string", "integer", "number", "boolean"}:
            failures.append((f"mapping.config_keys.{row.get('path')}", "unsupported value_type"))
    if schema_version >= 2:
        timezone_rows = [row for row in config_rows if row.get("path") == "/timezone"]
        if len(timezone_rows) != 1:
            failures.append(("mapping.config_keys./timezone",
                             "schema v2+ requires exactly one timezone config-key row"))
        elif not (timezone_rows[0].get("source") == "cover.timezone"
                  and timezone_rows[0].get("extractor") == "identity"
                  and timezone_rows[0].get("value_type", "string") == "string"):
            failures.append(("mapping.config_keys./timezone",
                             "timezone row must source cover.timezone as an identity string"))
    for row in rows:
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


def _number(value):
    match = re.search(r"\$([0-9][0-9,]*(?:\.\d+)?)", value)
    if not match:
        match = re.search(r"([0-9][0-9,]*(?:\.\d+)?)\s*(?:base\s+)?threshold", value, re.I)
    if not match: raise ValueError("currency value not found")
    return match.group(1).replace(",", "")


def extract(row, cover, answers, core):
    source = row["source"]
    raw = cover[source.split(".", 1)[1]] if source.startswith("cover.") else answers[source]
    value = core.provenance_value(raw, source)
    kind = row["extractor"]
    if kind == "identity": return value
    if kind == "currency": return _number(value)
    if kind == "emergency_minutes":
        match = re.search(r"Emergency\s+dispatch(?:\s+within)?\s+(\d+)\s+minutes?", value, re.I)
        if not match: raise ValueError("Emergency dispatch minutes not found")
        return match.group(1)
    if kind == "first_person": return re.split(r"[,;]", value, maxsplit=1)[0].strip()
    if kind == "maintenance_platform":
        match = re.search(r"(?:platform\s+)?([A-Za-z][A-Za-z0-9_-]+)\s+for\s+maintenance", value, re.I)
        if not match: raise ValueError("maintenance platform not found")
        return match.group(1)
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
    kind = row.get("value_type", "string")
    try:
        if kind == "string":
            return str(value)
        if kind == "integer":
            if not re.fullmatch(r"[-+]?\d+", str(value).strip()):
                raise ValueError("not an integer")
            return int(value)
        if kind == "number":
            return float(value)
        if kind == "boolean":
            if str(value).strip().lower() not in {"true", "false"}:
                raise ValueError("not true or false")
            return str(value).strip().lower() == "true"
    except (TypeError, ValueError) as exc:
        raise ValueError(f"cannot coerce {value!r} to {kind}: {exc}") from exc
    raise ValueError(f"unsupported value_type {kind}")


def _plan_config_keys_initial(root, mapping, cover, answers, core):
    rows = mapping.get("config_keys", [])
    if not rows:
        return None, []
    path = root / "config.json"
    if not path.is_file():
        raise PlaceholderRejected([("mapping.config_keys", "config.json is missing")])
    data = json.loads(path.read_text())
    manifest = []
    failures = []
    for row in rows:
        pointer = row["path"]
        try:
            node, leaf = _pointer_parent(data, pointer, create=row.get("mode", "replace") == "create")
            exists = ((isinstance(node, list) and isinstance(leaf, int) and 0 <= leaf < len(node))
                      or (isinstance(node, dict) and leaf in node))
            if not exists and row.get("mode", "replace") != "create":
                raise KeyError("declared replace target is absent")
            value = _typed_value(row, extract(row, cover, answers, core))
            if isinstance(node, list) and not exists:
                raise IndexError("create mode cannot extend arrays")
            manifest.append({
                "row_type": "config_key",
                "config_path": pointer,
                "question_id": row["source"],
                "file": "config.json#" + pointer,
                "count": 1,
                "value": value,
            })
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            failures.append((f"mapping.config_keys.{pointer}", str(exc)))
    if failures:
        raise PlaceholderRejected(failures)
    return path, manifest


def _commit_config_keys(path, manifest):
    if path is None:
        return
    data = json.loads(path.read_text())
    for item in manifest:
        node, leaf = _pointer_parent(data, item["config_path"], create=True)
        if isinstance(node, list):
            node[leaf] = item["value"]
        else:
            node[leaf] = item["value"]
    path.write_text(json.dumps(data, indent=2) + "\n")


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
    if failures: raise PlaceholderRejected(failures)
    config_path, config_manifest = _plan_config_keys_initial(
        root, mapping, cover, answers, core
    )
    manifest = []
    for name, row in rows.items():
        value = extract(row, cover, answers, core)
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
                    manifest.append({"placeholder": name, "question_id": row["source"], "file": relative + "#" + pointer, "count": 1, "value": value})
            else:
                text = path.read_text(); count = text.count(token)
                marker = f"<!-- BETTY-PH:{name} -->{value}<!-- /BETTY-PH:{name} -->"
                path.write_text(text.replace(token, marker))
                manifest.append({"placeholder": name, "question_id": row["source"], "file": relative, "count": count, "value": value})
    if config_path is not None:
        _commit_config_keys(config_path, config_manifest)
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
            row = next((candidate for candidate in mapping.get("config_keys", [])
                        if candidate.get("path") == pointer), None)
            if row is None:
                failures.append((f"manifest.config_key.{pointer}", "managed config key no longer has a mapping row")); continue
            path = root / "config.json"
            try:
                data = json.loads(path.read_text())
                node, leaf = _pointer_parent(data, pointer)
                current = node[leaf]
                if current != item.get("value"):
                    raise ValueError("managed config value changed outside the engine")
                value = _typed_value(row, extract(row, cover, answers, core))
                node[leaf] = value
                path.write_text(json.dumps(data, indent=2) + "\n")
                new_manifest.append({**item, "question_id": row["source"], "value": value})
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
        value = extract(row, cover, answers, core)
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
        new_manifest.append({**item, "question_id": row["source"], "value": value})
    if failures: raise PlaceholderRejected(failures)
    return new_manifest
