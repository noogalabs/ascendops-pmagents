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
    rows = data.get("placeholders", [])
    names = [row.get("placeholder") for row in rows]
    if not rows or len(names) != len(set(names)):
        raise PlaceholderRejected([("mapping", "placeholder rows are missing or duplicated")])
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
    if failures: raise PlaceholderRejected(failures)
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
