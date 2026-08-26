"""Graduated cross-seat schema, pointer resolution, and contradiction surfacing."""
from __future__ import annotations

import copy
import hashlib
import json
import re, value_extractors
from pathlib import Path
from typing import NamedTuple


SCHEMA_NAME = "betty-seat-config"
SCHEMA_VERSION = 2
CROSS_SEAT_SCHEMA_VERSION = 1
COMPATIBILITY_PLACEHOLDER = "__BETTY_SCHEMA_V2_REQUIRES_ENGINE_1_1__"


class CrossSeatRejected(RuntimeError):
    def __init__(self, failures):
        self.failures = failures
        super().__init__("cross-seat doctrine rejected")


class CrossSeatResult(NamedTuple):
    current: dict
    owner_updates: dict[str, dict]
    report_items: list[dict]


def compatibility_guard(minimum_engine_version):
    _version(minimum_engine_version)
    return {
        "row_type": "compatibility_guard",
        "placeholder": COMPATIBILITY_PLACEHOLDER,
        "minimum_engine_version": minimum_engine_version,
        "file": "seat-config.json",
        "count": 0,
        "value": "",
    }


def validate_compatibility_guards(manifest, reader_version):
    reader = _version(reader_version)
    failures = []
    for item in manifest:
        if item.get("row_type") != "compatibility_guard":
            continue
        try:
            minimum = _version(item.get("minimum_engine_version"))
        except ValueError as exc:
            failures.append(("compatibility_guard", str(exc))); continue
        if minimum > reader:
            failures.append(("compatibility_guard",
                             f"seat requires engine {item['minimum_engine_version']}; reader is {reader_version}"))
    if failures:
        raise CrossSeatRejected(failures)


def _version(value):
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", str(value or ""))
    if not match:
        raise ValueError(f"invalid semantic version {value!r}")
    return tuple(int(part) for part in match.groups())


def _schema_version(config):
    schema = config.get("seat_config_schema")
    if schema is None:
        return 1
    if schema.get("name") != SCHEMA_NAME or not isinstance(schema.get("version"), int):
        raise ValueError("seat_config_schema is invalid")
    return schema["version"]


def _measured_value(measure, value):
    """Normalize a FACT_MATCH value using the declared shared measure."""
    if measure in {None, "identity", "days", "currency"}:
        return value
    if measure == "maintenance_platform":
        return value_extractors.maintenance_platform(value).casefold()
    raise ValueError(f"unsupported FACT_MATCH measure {measure!r}")


def _pointer_parts(pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("value path must be an RFC6901 pointer")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]


def _read_pointer(payload, pointer):
    node = payload
    for part in _pointer_parts(pointer):
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def _digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _plan_id(row, appender_seat, value):
    identity = {
        "owner_seat": row["owner_seat"],
        "owner_question_id": row["owner_question_id"],
        "appender_seat": appender_seat,
        "appender_question_id": row["appender_question_id"],
        "value_name": row["value_name"],
        "value": value,
    }
    return hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def structured_answers_filename(mapping):
    """Resolve the declared structured artifact without guessing from the tree."""
    filename = mapping.get("structured_answers_file", "seat-config.json")
    if (not isinstance(filename, str) or not filename or Path(filename).name != filename
            or not filename.endswith(".json")):
        raise CrossSeatRejected([("mapping.structured_answers_file",
                                  "must be a safe JSON filename")])
    return filename


def undeclared_structured_artifacts(root, mapping):
    declared = structured_answers_filename(mapping)
    return sorted(path.name for path in Path(root).glob("*-config.json")
                  if path.name != declared)


def _load_registry(registry):
    if not isinstance(registry, dict):
        raise CrossSeatRejected([("registry", "seat registry must be an object")])
    result = {}
    for seat, entry in registry.items():
        if isinstance(entry, dict):
            path = entry.get("path")
            mapping = entry.get("mapping", {})
            if not isinstance(mapping, dict):
                raise CrossSeatRejected([(f"registry.{seat}", "mapping declaration must be an object")])
            filename = structured_answers_filename(mapping)
        else:
            path = entry
            filename = "seat-config.json"
        if not isinstance(path, (str, Path)):
            raise CrossSeatRejected([(f"registry.{seat}", "registry path is invalid")])
        candidate = Path(path) / filename if Path(path).is_dir() else Path(path)
        if not candidate.is_file():
            raise CrossSeatRejected([(f"registry.{seat}",
                                      f"declared structured artifact {filename} is absent")])
        try:
            payload = json.loads(candidate.read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise CrossSeatRejected([(f"registry.{seat}",
                                      f"cannot read valid peer JSON: {exc}")]) from exc
        if not isinstance(payload, dict):
            raise CrossSeatRejected([(f"registry.{seat}", "peer payload must be an object")])
        if payload.get("seat") != seat:
            raise CrossSeatRejected([(f"registry.{seat}", "seat-config identity mismatch")])
        result[seat] = payload
    return result


def _check_kind(row):
    kind = row.get("type", row.get("assertion_type", row.get("doctrine")))
    return {"POLICY": "POLICY_DIVERGE", "SPLIT": "POLICY_DIVERGE"}.get(kind, kind)


def _ordering_passes(left, right, operator):
    operations = {
        "gte": lambda a, b: a >= b, ">=": lambda a, b: a >= b,
        "gt": lambda a, b: a > b, ">": lambda a, b: a > b,
        "lte": lambda a, b: a <= b, "<=": lambda a, b: a <= b,
        "lt": lambda a, b: a < b, "<": lambda a, b: a < b,
    }
    if operator not in operations:
        raise ValueError(f"unknown ordering operator {operator!r}")
    def comparable(value):
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
        if isinstance(value, str) and re.fullmatch(r"\s*\$?[-+]?\d[\d,]*(?:\.\d+)?\s*", value):
            return float(value.strip().replace("$", "").replace(",", ""))
        raise TypeError(f"ordering value {value!r} is not numeric")
    return operations[operator](comparable(left), comparable(right))


def _validate_peer_version(seat, payload, reader_version):
    if not isinstance(payload, dict):
        raise CrossSeatRejected([(f"cross_seat.{seat}", "peer payload must be an object")])
    seat_schema = payload.get("seat_config_schema")
    if seat_schema is not None and not isinstance(seat_schema, dict):
        raise CrossSeatRejected([(f"cross_seat.{seat}",
                                  "seat_config_schema must be an object")])
    engine_metadata = payload.get("configuration_engine", {})
    if not isinstance(engine_metadata, dict):
        raise CrossSeatRejected([(f"cross_seat.{seat}",
                                  "configuration_engine must be an object")])
    try:
        schema = _schema_version(payload)
    except (TypeError, ValueError) as exc:
        raise CrossSeatRejected([(f"cross_seat.{seat}", f"invalid seat schema: {exc}")]) from exc
    if schema > SCHEMA_VERSION:
        raise CrossSeatRejected([(f"cross_seat.{seat}",
                                  f"seat schema {schema} is newer than supported {SCHEMA_VERSION}")])
    producer = engine_metadata.get("version")
    if producer is not None:
        try:
            producer_version = _version(producer)
        except (TypeError, ValueError) as exc:
            raise CrossSeatRejected([(f"cross_seat.{seat}",
                                      f"invalid producer engine version: {exc}")]) from exc
        if producer_version > _version(reader_version):
            raise CrossSeatRejected([(f"cross_seat.{seat}",
                                      f"owner engine {producer} is newer than reader {reader_version}")])
    return schema


def apply(current, mapping, registry, *, engine_version):
    """Apply seam metadata in memory; callers commit returned trees transactionally."""
    doctrine = mapping.get("cross_seat")
    if doctrine is None:
        return CrossSeatResult(copy.deepcopy(current), {}, [])
    peers = _load_registry(registry)
    result = copy.deepcopy(current)
    result["seat_config_schema"] = {"name": SCHEMA_NAME, "version": SCHEMA_VERSION}
    cross = result.setdefault("cross_seat", {})
    cross["schema_version"] = CROSS_SEAT_SCHEMA_VERSION
    cross.setdefault("pointers", {})
    cross.setdefault("held", {})
    cross.setdefault("appends", {})
    cross.setdefault("append_plans", {})
    result["cross_seat_checks"] = []
    result["never_graduate"] = copy.deepcopy(doctrine.get("never_graduate", []))
    fill_exempt = doctrine.get("fill_exempt", [])
    if (not isinstance(fill_exempt, list) or any(not isinstance(item, str) or not item
                                                for item in fill_exempt)
            or len(fill_exempt) != len(set(fill_exempt))):
        raise CrossSeatRejected([("cross_seat.fill_exempt", "must be a unique string set")])
    result["fill_exempt"] = copy.deepcopy(fill_exempt)
    lanes = doctrine.get("cross_seat_lane", [])
    if not isinstance(lanes, list):
        raise CrossSeatRejected([("cross_seat.cross_seat_lane", "must be a list")])
    for lane in lanes:
        if (not isinstance(lane, dict)
                or not all(isinstance(lane.get(key), str) and lane[key]
                           for key in ("lane_id", "from_seat", "to_seat"))):
            raise CrossSeatRejected([("cross_seat.cross_seat_lane", "lane definition is invalid")])
    result["cross_seat_lanes"] = copy.deepcopy(lanes)
    failures = []
    report_items = []

    seen = set()
    for row in doctrine.get("pointers", []):
        name = row.get("value_name")
        if not name or name in seen:
            failures.append(("cross_seat.pointers", "value_name is missing or duplicated")); continue
        seen.add(name)
        owner = row.get("owner_seat")
        owner_question = row.get("owner_question_id")
        local_question = row.get("holding_question_id")
        owner_path = row.get("owner_value_path")
        if owner == result.get("seat") or not all(isinstance(item, str) and item for item in
                                                  (owner, owner_question, local_question, owner_path)):
            failures.append((f"cross_seat.pointers.{name}", "pointer identity/path is invalid")); continue
        if owner in peers:
            try:
                owner_schema = _validate_peer_version(owner, peers[owner], engine_version)
                owner_value = _read_pointer(peers[owner], owner_path)
            except (KeyError, IndexError, TypeError, ValueError, CrossSeatRejected) as exc:
                detail = exc.failures if isinstance(exc, CrossSeatRejected) else str(exc)
                failures.append((f"cross_seat.pointers.{name}", f"owner value unresolvable: {detail}")); continue
            cross["held"].pop(name, None)
            cross["pointers"][name] = {
                "owner_seat": owner,
                "owner_question_id": owner_question,
                "state": "resolved",
                "resolved_owner_schema": owner_schema,
                "value_sha256": _digest(owner_value),
            }
        else:
            try:
                value = _read_pointer(result, row.get("holding_value_path", f"/answers/{local_question}"))
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                failures.append((f"cross_seat.pointers.{name}", f"holding value unresolvable: {exc}")); continue
            cross["pointers"].pop(name, None)
            cross["held"][name] = {
                "owner_seat": owner,
                "owner_question_id": owner_question,
                "held_pending_seat": owner,
                "holding_question_id": local_question,
                "value": value,
                "value_sha256": _digest(value),
            }
        if row.get("migration_pending"):
            trigger = row.get("migration_trigger")
            target = row.get("migrates_to")
            if not all(isinstance(item, str) and item for item in (trigger, target)):
                failures.append((f"cross_seat.pointers.{name}",
                                 "migration_pending requires migration_trigger and migrates_to")); continue
            migration = {
                "migration_pending": True,
                "migration_trigger": trigger,
                "migrates_to": target,
                "trigger_present": trigger in peers,
            }
            cross.setdefault("migrations", {})[name] = migration
            if trigger in peers:
                report_items.append({
                    "check_id": f"migration-{name}", "doctrine": "MIGRATION",
                    "status": "PENDING", "migration_trigger": trigger,
                    "migrates_to": target, "value_name": name,
                })

    for row in doctrine.get("checks", []):
        check_id = row.get("check_id")
        kind = _check_kind(row)
        peer = row.get("peer_seat")
        if kind not in {"FACT_MATCH", "POLICY_DIVERGE", "ORDERING"} or not all(
                isinstance(item, str) and item for item in
                (check_id, peer, row.get("local_ref"), row.get("peer_ref"))):
            failures.append((f"cross_seat_checks.{check_id}", "check definition is invalid")); continue
        if kind == "FACT_MATCH":
            local_measure = row.get("local_measure", row.get("measure"))
            peer_measure = row.get("peer_measure", row.get("measure"))
            if local_measure is not None or peer_measure is not None:
                if (not isinstance(local_measure, str) or not local_measure
                        or not isinstance(peer_measure, str) or not peer_measure
                        or local_measure != peer_measure):
                    failures.append((f"cross_seat_checks.{check_id}",
                                     "FACT_MATCH requires one declared common measure")); continue
        if row.get("severity", "report") not in {"report", "error"}:
            failures.append((f"cross_seat_checks.{check_id}", "severity must be report or error")); continue
        try:
            local_value = _read_pointer(result, row["local_ref"])
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            failures.append((f"cross_seat_checks.{check_id}", f"local value unresolvable: {exc}")); continue
        record = {
            "check_id": check_id,
            "doctrine": kind,
            "local_ref": row["local_ref"],
            "peer_ref": {"seat": peer, "path": row["peer_ref"]},
            "local_sha256": _digest(local_value),
        }
        if peer not in peers:
            record["status"] = "peer_absent"
            record["peer_sha256"] = None
            if kind == "FACT_MATCH" and row.get("promise"):
                report_items.append({
                    "check_id": check_id, "doctrine": kind, "status": "UNBACKED",
                    "local": {"seat": result.get("seat"), "path": row["local_ref"], "value": local_value},
                    "peer": {"seat": peer, "path": row["peer_ref"], "value": None},
                })
        else:
            try:
                _validate_peer_version(peer, peers[peer], engine_version)
                peer_value = _read_pointer(peers[peer], row["peer_ref"])
            except (KeyError, IndexError, TypeError, ValueError, CrossSeatRejected) as exc:
                detail = exc.failures if isinstance(exc, CrossSeatRejected) else str(exc)
                failures.append((f"cross_seat_checks.{check_id}", f"peer value unresolvable: {detail}")); continue
            record["peer_sha256"] = _digest(peer_value)
            if kind == "FACT_MATCH":
                try:
                    compared_local = _measured_value(local_measure, local_value)
                    compared_peer = _measured_value(peer_measure, peer_value)
                except ValueError as exc:
                    failures.append((f"cross_seat_checks.{check_id}", str(exc))); continue
                passed = compared_local == compared_peer
            elif kind == "POLICY_DIVERGE":
                passed = True
            else:
                try:
                    passed = _ordering_passes(local_value, peer_value, row.get("operator"))
                except (TypeError, ValueError) as exc:
                    failures.append((f"cross_seat_checks.{check_id}", str(exc))); continue
            record["status"] = "pass" if passed else "fail"
            should_report = (kind == "POLICY_DIVERGE" and local_value != peer_value) or not passed
            if should_report:
                if row.get("severity", "report") == "error":
                    failures.append((f"cross_seat_checks.{check_id}",
                                     f"{kind} assertion failed")); continue
                report_items.append({
                    "check_id": check_id,
                    "doctrine": kind,
                    "local": {"seat": result.get("seat"), "path": row["local_ref"], "value": local_value},
                    "peer": {"seat": peer, "path": row["peer_ref"], "value": peer_value},
                    "status": "EYEBALL",
                })
        result["cross_seat_checks"].append(record)

    for row in doctrine.get("all_pairs", []):
        check_id = row.get("check_id")
        participants = row.get("participants")
        if (not isinstance(check_id, str) or not check_id or not isinstance(participants, list)
                or len(participants) < 2):
            failures.append(("cross_seat.all_pairs", "all-pairs definition is invalid")); continue
        values = []
        try:
            for participant in participants:
                seat = participant["seat"]
                payload = result if seat == result.get("seat") else peers[seat]
                if seat != result.get("seat"):
                    _validate_peer_version(seat, payload, engine_version)
                values.append((seat, participant["path"], _read_pointer(payload, participant["path"])))
        except CrossSeatRejected as exc:
            failures.extend(exc.failures); continue
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            failures.append((f"cross_seat.all_pairs.{check_id}", f"participant unresolvable: {exc}")); continue
        failing = []
        for index, left in enumerate(values):
            for right in values[index + 1:]:
                if left[2] != right[2]:
                    failing.append((left, right))
                    report_items.append({
                        "check_id": f"{check_id}:{left[0]}:{right[0]}",
                        "doctrine": "POLICY_DIVERGE", "status": "EYEBALL",
                        "local": {"seat": left[0], "path": left[1], "value": left[2]},
                        "peer": {"seat": right[0], "path": right[1], "value": right[2]},
                    })
        result["cross_seat_checks"].append({
            "check_id": check_id, "doctrine": "ALL_PAIRS", "pair_count": len(values) * (len(values) - 1) // 2,
            "failing_pair_count": len(failing), "status": "pass" if not failing else "fail",
        })

    fill_hints = doctrine.get("fill_hints", {})
    if not isinstance(fill_hints, dict):
        failures.append(("cross_seat.fill_hints", "must be an object"))
        fill_hints = {}
    derived = result.setdefault("derived", {})
    for field, hint in fill_hints.items():
        if field not in fill_exempt and field not in derived:
            derived[field] = copy.deepcopy(hint)
    for field in fill_exempt:
        if field not in derived:
            report_items.append({
                "check_id": f"fill-exempt-{field}", "doctrine": "FILL_EXEMPT",
                "status": "ABSENT", "value_name": field,
            })

    for row in doctrine.get("appends", []):
        required = ("value_name", "owner_seat", "owner_question_id", "appender_question_id",
                    "value_path", "owner_target_path")
        if not all(isinstance(row.get(key), str) and row[key] for key in required):
            failures.append(("cross_seat.appends", "append definition is incomplete")); continue
        try:
            value = _read_pointer(result, row["value_path"])
            _pointer_parts(row["owner_target_path"])
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            failures.append((f"cross_seat.appends.{row.get('value_name')}", str(exc))); continue
        plan_id = _plan_id(row, result.get("seat"), value)
        plan = {
            "plan_id": plan_id,
            "status": "planned",
            "owner_seat": row["owner_seat"],
            "owner_question_id": row["owner_question_id"],
            "appender_seat": result.get("seat"),
            "appender_question_id": row["appender_question_id"],
            "value_name": row["value_name"],
            "value": value,
            "value_sha256": _digest(value),
            "owner_target_path": row["owner_target_path"],
        }
        existing = cross["append_plans"].get(plan_id)
        if existing is not None and existing != plan:
            failures.append((f"cross_seat.appends.{row['value_name']}", "plan id collision")); continue
        cross["append_plans"][plan_id] = plan
        owner_receipts = peers.get(row["owner_seat"], {}).get("cross_seat", {}).get("appends", {})
        if plan_id not in owner_receipts:
            report_items.append({
                "check_id": "append-" + plan_id[:12],
                "doctrine": "OWNER-APPEND",
                "status": "PENDING",
                "plan_id": plan_id,
                "owner_seat": row["owner_seat"],
                "value_name": row["value_name"],
            })

    if failures:
        raise CrossSeatRejected(failures)
    result["cross_seat_checks"].sort(key=lambda item: item["check_id"])
    report_items.sort(key=lambda item: item["check_id"])
    return CrossSeatResult(result, {}, report_items)


def render_report_block(items):
    lines = ["<!-- BETTY-CROSS-SEAT-BEGIN -->", "## Cross-seat checks"]
    if not items:
        lines.append("- None.")
    for item in items:
        if item["status"] == "UNDECLARED":
            lines.append(
                f"- UNDECLARED {item['check_id']} (STRUCTURED-ARTIFACT): "
                f"{item['value_name']} is present but the mapping does not declare it."
            )
            continue
        if item["status"] == "ABSENT":
            lines.append(
                f"- ABSENT {item['check_id']} (FILL_EXEMPT): {item['value_name']} stayed empty; "
                "no documentation hint was promoted into a promise."
            )
            continue
        if item["status"] == "UNBACKED":
            lines.append(
                f"- UNBACKED {item['check_id']} ({item['doctrine']}): "
                f"{item['local']['seat']} {item['local']['path']} has a promise but "
                f"delivering seat {item['peer']['seat']} is absent."
            )
            continue
        if item["status"] == "PENDING":
            if item.get("doctrine") == "MIGRATION":
                lines.append(
                    f"- PENDING {item['check_id']} (MIGRATION): trigger {item['migration_trigger']} "
                    f"is present; explicit promotion to {item['migrates_to']} is required. No auto-flip occurred."
                )
                continue
            lines.append(
                f"- PENDING {item['check_id']} (OWNER-APPEND): plan {item['plan_id']} "
                f"awaits apply on {item['owner_seat']} for {item['value_name']}; it was not silently omitted."
            )
            continue
        lines.append(
            f"- EYEBALL {item['check_id']} ({item['doctrine']}): "
            f"{item['local']['seat']} {item['local']['path']} = {item['local']['value']!r}; "
            f"{item['peer']['seat']} {item['peer']['path']} = {item['peer']['value']!r}. "
            "Values were preserved; no auto-unification occurred."
        )
    lines.append("<!-- BETTY-CROSS-SEAT-END -->")
    return "\n".join(lines) + "\n"


def replace_report_block(text, items):
    block = render_report_block(items)
    pattern = re.compile(r"<!-- BETTY-CROSS-SEAT-BEGIN -->.*?<!-- BETTY-CROSS-SEAT-END -->\n?", re.S)
    if pattern.search(text):
        return pattern.sub(block, text)
    return text.rstrip() + "\n\n" + block


def resolve_pointer_config_rows(current, mapping, registry, *, engine_version,
                                extract_pointer_value=None):
    """Resolve K-rows through declared cross-seat pointers without silent defaults."""
    peers = _load_registry(registry)
    pointer_rows = {row.get("value_name"): row
                    for row in mapping.get("cross_seat", {}).get("pointers", [])}
    resolved = []
    failures = []
    for row in mapping.get("config_keys", []):
        if row.get("value_from") != "pointer":
            continue
        name = row.get("pointer_name")
        pointer = pointer_rows.get(name)
        if not pointer:
            failures.append((f"mapping.config_keys.{row.get('path')}",
                             f"pointer {name!r} is not declared")); continue
        owner = pointer.get("owner_seat")
        if owner in peers:
            try:
                _validate_peer_version(owner, peers[owner], engine_version)
                value = _read_pointer(peers[owner], pointer["owner_value_path"])
            except (KeyError, IndexError, TypeError, ValueError, CrossSeatRejected) as exc:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 f"owner pointer unresolvable: {exc}")); continue
            state = "owner"
        elif row.get("fallback_from") == "holding_answer":
            try:
                value = _read_pointer(
                    current,
                    pointer.get("holding_value_path", f"/answers/{pointer['holding_question_id']}"),
                )
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 f"holding answer unresolvable: {exc}")); continue
            state = "held_holding_answer"
        elif "fallback" in row:
            value = copy.deepcopy(row["fallback"])
            state = "held_fallback"
        else:
            failures.append((f"mapping.config_keys.{row.get('path')}",
                             "owner is absent and no fallback is declared")); continue
        if row.get("extractor") is not None:
            if extract_pointer_value is None:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 "pointer extractor capability is unavailable")); continue
            try:
                value = extract_pointer_value(row, value)
            except (KeyError, TypeError, ValueError) as exc:
                failures.append((f"mapping.config_keys.{row.get('path')}",
                                 f"pointer extraction failed: {exc}")); continue
        resolved.append({
            "row_type": "config_key", "config_path": row["path"],
            "question_id": f"pointer:{name}", "file": "config.json#" + row["path"],
            "count": 1, "value": value, "resolution": state, "owner_seat": owner,
            "mode": row.get("mode", "replace"),
        })
    if failures:
        raise CrossSeatRejected(failures)
    return resolved


def apply_append_plan(owner, appender, plan_id, *, engine_version):
    """Apply one persisted plan to an owner config in memory, replay-safe by plan id."""
    if not isinstance(owner, dict):
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "owner payload must be an object")])
    if not isinstance(appender, dict):
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "appender payload must be an object")])
    appender_cross = appender.get("cross_seat", {})
    if not isinstance(appender_cross, dict):
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "appender cross_seat must be an object")])
    owner_result = copy.deepcopy(owner)
    plans = appender_cross.get("append_plans", {})
    if not isinstance(plans, dict):
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "append_plans must be an object")])
    plan = plans.get(plan_id)
    if not isinstance(plan, dict) or plan.get("status") != "planned":
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "persisted appender plan is missing or invalid")])
    if owner_result.get("seat") != plan.get("owner_seat"):
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "owner seat identity mismatch")])
    _validate_peer_version(owner_result.get("seat"), owner_result, engine_version)
    existing_cross = owner_result.get("cross_seat", {})
    if not isinstance(existing_cross, dict):
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "owner cross_seat must be an object")])
    cross = owner_result.setdefault("cross_seat", existing_cross)
    receipts = cross.setdefault("appends", {})
    if plan_id in receipts:
        if receipts[plan_id].get("value_sha256") != plan.get("value_sha256"):
            raise CrossSeatRejected([(f"append_plan.{plan_id}", "owner receipt conflicts with plan")])
        return owner_result, False
    try:
        node, leaf = _pointer_parent_for_write(owner_result, plan["owner_target_path"])
        roster = node[leaf]
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise CrossSeatRejected([(f"append_plan.{plan_id}", f"owner target unresolvable: {exc}")]) from exc
    if not isinstance(roster, list):
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "owner target is not a roster list")])
    if plan["value"] not in roster:
        roster.append(copy.deepcopy(plan["value"]))
    receipts[plan_id] = {
        "direction": "inbound",
        "owner_seat": plan["owner_seat"],
        "owner_question_id": plan["owner_question_id"],
        "appender_seat": plan["appender_seat"],
        "appender_question_id": plan["appender_question_id"],
        "value_name": plan["value_name"],
        "value_sha256": plan["value_sha256"],
    }
    return owner_result, True


def _pointer_parent_for_write(payload, pointer):
    parts = _pointer_parts(pointer)
    if not parts:
        raise ValueError("owner target cannot be the document root")
    node = payload
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    leaf = int(parts[-1]) if isinstance(node, list) else parts[-1]
    return node, leaf


def pending_append_plans(appender, owner):
    receipts = owner.get("cross_seat", {}).get("appends", {})
    return [copy.deepcopy(plan) for plan_id, plan in sorted(
        appender.get("cross_seat", {}).get("append_plans", {}).items()
    ) if plan_id not in receipts]
