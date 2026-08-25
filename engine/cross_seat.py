"""Graduated cross-seat schema, pointer resolution, and contradiction surfacing."""
from __future__ import annotations

import copy
import hashlib
import json
import re
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


def _load_registry(registry):
    result = {}
    for seat, path in registry.items():
        candidate = Path(path) / "seat-config.json" if Path(path).is_dir() else Path(path)
        if not candidate.is_file():
            continue
        payload = json.loads(candidate.read_text())
        if payload.get("seat") != seat:
            raise CrossSeatRejected([(f"registry.{seat}", "seat-config identity mismatch")])
        result[seat] = payload
    return result


def _validate_peer_version(seat, payload, reader_version):
    schema = _schema_version(payload)
    if schema > SCHEMA_VERSION:
        raise CrossSeatRejected([(f"cross_seat.{seat}",
                                  f"seat schema {schema} is newer than supported {SCHEMA_VERSION}")])
    producer = payload.get("configuration_engine", {}).get("version")
    if producer is not None and _version(producer) > _version(reader_version):
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
                _read_pointer(peers[owner], owner_path)
            except (KeyError, IndexError, TypeError, ValueError, CrossSeatRejected) as exc:
                detail = exc.failures if isinstance(exc, CrossSeatRejected) else str(exc)
                failures.append((f"cross_seat.pointers.{name}", f"owner value unresolvable: {detail}")); continue
            cross["held"].pop(name, None)
            cross["pointers"][name] = {
                "owner_seat": owner,
                "owner_question_id": owner_question,
                "state": "resolved",
                "resolved_owner_schema": owner_schema,
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

    for row in doctrine.get("checks", []):
        check_id = row.get("check_id")
        kind = row.get("doctrine")
        peer = row.get("peer_seat")
        if kind not in {"POLICY", "SPLIT"} or not all(
                isinstance(item, str) and item for item in
                (check_id, peer, row.get("local_ref"), row.get("peer_ref"))):
            failures.append((f"cross_seat_checks.{check_id}", "check definition is invalid")); continue
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
        else:
            try:
                _validate_peer_version(peer, peers[peer], engine_version)
                peer_value = _read_pointer(peers[peer], row["peer_ref"])
            except (KeyError, IndexError, TypeError, ValueError, CrossSeatRejected) as exc:
                detail = exc.failures if isinstance(exc, CrossSeatRejected) else str(exc)
                failures.append((f"cross_seat_checks.{check_id}", f"peer value unresolvable: {detail}")); continue
            record["peer_sha256"] = _digest(peer_value)
            record["status"] = "agree" if local_value == peer_value else "disagree"
            if record["status"] == "disagree":
                report_items.append({
                    "check_id": check_id,
                    "doctrine": kind,
                    "local": {"seat": result.get("seat"), "path": row["local_ref"], "value": local_value},
                    "peer": {"seat": peer, "path": row["peer_ref"], "value": peer_value},
                    "status": "EYEBALL",
                })
        result["cross_seat_checks"].append(record)

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
        if item["status"] == "PENDING":
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


def apply_append_plan(owner, appender, plan_id, *, engine_version):
    """Apply one persisted plan to an owner config in memory, replay-safe by plan id."""
    owner_result = copy.deepcopy(owner)
    plans = appender.get("cross_seat", {}).get("append_plans", {})
    plan = plans.get(plan_id)
    if not isinstance(plan, dict) or plan.get("status") != "planned":
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "persisted appender plan is missing or invalid")])
    if owner_result.get("seat") != plan.get("owner_seat"):
        raise CrossSeatRejected([(f"append_plan.{plan_id}", "owner seat identity mismatch")])
    _validate_peer_version(owner_result.get("seat"), owner_result, engine_version)
    cross = owner_result.setdefault("cross_seat", {})
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
