#!/usr/bin/env python3
"""Production file intake and atomic rerun wrapper for sealed Betty seat configurators."""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import placeholders
import cross_seat
import credential_scan
import intake
import transaction

ENGINE_VERSION = "1.1.0"
ROOT = Path(__file__).resolve().parents[1]
MAINTENANCE_EDITION = ROOT / "editions" / "maintenance"
PM_ASSIST_EDITION = ROOT / "editions" / "pm-assist"
LEASING_EDITION = ROOT / "editions" / "leasing"
TURNOVER_EDITION = ROOT / "editions" / "turnover"
SEALED_CORE = MAINTENANCE_EDITION / "configure_agent.py"
SEALED_CORE_SHA256 = "0540ea08aa8d47ecb1aebbb7f51db85c5a67ab252172804e9ba24e56c2403551"
SUPPORTED = {
    "maintenance-coordinator": {
        "library_id": "maintenance-2026-08-23",
        "answers": MAINTENANCE_EDITION / "answers-format.md",
        "library": MAINTENANCE_EDITION / "library-src",
        "mapping": Path(__file__).resolve().parent / "mappings" / "maintenance-coordinator.json",
        "question_ids": [*(f"A{i}" for i in range(1, 9)), *(f"B{i}" for i in range(1, 13)), *(f"C{i}" for i in range(1, 10)), *(f"D{i}" for i in range(1, 10))],
        "runner": "sealed",
    },
    "pm-assist": {
        "library_id": "pm-assist-2026-08-25",
        "answers": PM_ASSIST_EDITION / "answers-format.md",
        "library": PM_ASSIST_EDITION / "library-src",
        "mapping": Path(__file__).resolve().parent / "mappings" / "pm-assist.json",
        "question_ids": [*(f"A{i}" for i in range(1, 11)), *(f"B{i}" for i in range(1, 15)), *(f"C{i}" for i in range(1, 9)), *(f"D{i}" for i in range(1, 10))],
        "runner": "mapping",
    },
    "leasing-coordinator": {
        "library_id": "leasing-2026-08-25",
        "answers": LEASING_EDITION / "answers-format.md",
        "library": LEASING_EDITION / "library-src",
        "mapping": Path(__file__).resolve().parent / "mappings" / "leasing-coordinator.json",
        "question_ids": [*(f"A{i}" for i in range(1, 15)), *(f"B{i}" for i in range(1, 10)), *(f"C{i}" for i in range(1, 7)), *(f"D{i}" for i in range(1, 11))],
        "runner": "mapping",
    },
    "turnover-coordinator": {
        "library_id": "turnover-2026-08-25",
        "answers": TURNOVER_EDITION / "answers-format.md",
        "library": TURNOVER_EDITION / "library-src",
        "mapping": Path(__file__).resolve().parent / "mappings" / "turnover-coordinator.json",
        "question_ids": [*(f"A{i}" for i in range(1, 7)), *(f"B{i}" for i in range(1, 7)), *(f"C{i}" for i in range(1, 8)), *(f"D{i}" for i in range(1, 8)), *(f"E{i}" for i in range(1, 9))],
        "runner": "mapping",
    },
}


IntakeRejected = intake.IntakeRejected


def load_seat_mapping(seat: str):
    if seat not in SUPPORTED:
        raise IntakeRejected([("seat", f"no mapping table/library is installed for {seat!r}")])
    try:
        return placeholders.load_mapping(SUPPORTED[seat]["mapping"])
    except placeholders.PlaceholderRejected as exc:
        raise IntakeRejected(exc.failures) from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise IntakeRejected([("mapping", f"cannot read valid JSON: {exc}")]) from exc


def cover_fields_for_mapping(mapping):
    rows = mapping.get("cover_fields")
    if rows is None:
        return dict(intake.COVER_FIELDS)
    failures = []
    fields = {}
    if not isinstance(rows, list) or not rows:
        failures.append(("mapping.cover_fields", "must be a nonempty list of label/key objects"))
    else:
        for index, row in enumerate(rows):
            subject = f"mapping.cover_fields[{index}]"
            if not isinstance(row, dict) or set(row) != {"label", "key"}:
                failures.append((subject, "must contain exactly string label and key fields"))
                continue
            label, key = row["label"], row["key"]
            if not isinstance(label, str) or not label.strip() or not isinstance(key, str) or not key.strip():
                failures.append((subject, "label and key must be nonblank strings"))
            elif label in fields or key in fields.values():
                failures.append((subject, "label and key must each be unique"))
            else:
                fields[label] = key
    if failures:
        raise IntakeRejected(failures)
    return fields


def cover_fields_for_seat(seat: str):
    return cover_fields_for_mapping(load_seat_mapping(seat))


def read_member_json(path: Path, subject: str):
    try:
        payload = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise IntakeRejected([(subject, f"cannot read valid JSON: {exc}")]) from exc
    if not isinstance(payload, dict):
        raise IntakeRejected([(subject, "JSON document must be an object")])
    return payload


def load_core():
    actual = hashlib.sha256(SEALED_CORE.read_bytes()).hexdigest()
    if actual != SEALED_CORE_SHA256:
        raise RuntimeError(f"sealed-core: byte identity mismatch: {actual}")
    spec = importlib.util.spec_from_file_location("betty_sealed_configurator", SEALED_CORE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def run_sealed_core(core, source: Path, answers: Path, output: Path, library: Path, clock):
    """Run the sealed core with one invocation-scoped date provider."""
    configuration_date = clock()
    if not isinstance(configuration_date, datetime.date):
        raise TypeError("configuration clock must return datetime.date")

    class InvocationDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(
                configuration_date.year,
                configuration_date.month,
                configuration_date.day,
            )

    original_datetime = core.datetime
    core.datetime = types.SimpleNamespace(date=InvocationDate)
    try:
        core.run(source, answers, output, library)
    finally:
        core.datetime = original_datetime
    return configuration_date.isoformat()


def validate(path: Path, seat: str):
    if seat not in SUPPORTED:
        raise IntakeRejected([("seat", f"no mapping table/library is installed for {seat!r}")])
    return intake.preflight(
        path,
        SUPPORTED[seat]["question_ids"],
        cover_fields=cover_fields_for_seat(seat),
        semantic_profile="maintenance" if seat == "maintenance-coordinator" else "structural",
    )


def run_mapping_core(core, source: Path, answers: Path, output: Path, library: Path, clock, seat: str, parsed_intake):
    """Materialize a mapping-driven seat without changing the sealed maintenance core."""
    configuration_date = clock()
    if not isinstance(configuration_date, datetime.date):
        raise TypeError("configuration clock must return datetime.date")
    core.copy_safe(source, output)
    raw_cover, raw_answers = parsed_intake.raw_cover, parsed_intake.raw_answers
    structured = output / "seat-config.json"
    try:
        payload = json.loads(structured.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise IntakeRejected([("structured_answers_file", f"mapping-driven template needs valid seat-config.json: {exc}")]) from exc
    payload["seat"] = seat
    payload["cover_sheet"] = raw_cover
    payload["answers"] = raw_answers
    payload.setdefault("flags", {}).setdefault("unresolved", [])
    structured.write_text(json.dumps(payload, indent=2) + "\n")
    report = output / "contradiction-report.md"
    if not report.exists():
        report.write_text("# Contradiction review list\n\nGenerated cross-seat findings appear below.\n")
    return configuration_date.isoformat()


def restore_mapping_core_counterpart(prepared: Path, structured_filename: str, seat: str, old_manifest):
    """Restore the mapping core's canonical artifact only for an accepted managed rerun."""
    if structured_filename == "seat-config.json" or not old_manifest:
        return
    declared = prepared / structured_filename
    canonical = prepared / "seat-config.json"
    if not declared.is_file():
        return
    payload = read_member_json(declared, structured_filename)
    if payload.get("seat") != seat:
        raise IntakeRejected([(
            f"{structured_filename}.seat",
            f"configured artifact belongs to {payload.get('seat')!r}, expected {seat!r}",
        )])
    if canonical.exists():
        if not canonical.is_file() or canonical.read_bytes() != declared.read_bytes():
            raise IntakeRejected([(
                "structured_answers_file",
                f"declared structured artifact {structured_filename} conflicts with core counterpart seat-config.json",
            )])
        return
    shutil.copy2(declared, canonical)


def copy_protected(source: Path, staged: Path):
    census = transaction.protected_class_census(source)
    names = sorted({item.split("/", 1)[0] for items in census.values() for item in items})
    for name in names:
        src = source / name
        if not src.exists():
            continue
        dst = staged / name
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        if src.is_dir():
            shutil.copytree(src, dst, symlinks=True)
        else:
            shutil.copy2(src, dst, follow_symlinks=False)


def stamp(staged: Path, seat: str, managed_surfaces, preserved_tokens, provenance,
          configuration_date: str, structured_filename="seat-config.json"):
    path = staged / structured_filename
    payload = json.loads(path.read_text())
    payload["configuration_engine"] = {
        "version": ENGINE_VERSION,
        "sealed_core_sha256": SEALED_CORE_SHA256,
        "seat_library": SUPPORTED[seat]["library_id"],
        "managed_surfaces": managed_surfaces,
        "preserved_runtime_tokens": preserved_tokens,
        "answer_provenance": provenance,
        "configuration_date": configuration_date,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def configure(source: Path, answers: Path, output: Path, seat: str,
              *, clock=datetime.date.today, seat_registry=None):
    parsed_intake = validate(answers, seat)  # complete validation before staging or writes
    mapping = load_seat_mapping(seat)
    try:
        placeholders.validate_consumed_values(
            mapping, parsed_intake.raw_cover, parsed_intake.raw_answers
        )
    except placeholders.PlaceholderRejected as exc:
        raise IntakeRejected(exc.failures) from exc
    core = load_core()
    if output.exists() and not output.is_dir():
        raise IntakeRejected([("output", "existing output must be an agent directory")])
    output.parent.mkdir(parents=True, exist_ok=True)
    with transaction.DestinationLock(output):
      transaction.recover_directory_transaction(output)
      transaction.require_existing_output_as_source(source, output)
      staging_root = Path(tempfile.mkdtemp(prefix=f".{output.name}.glue-scratch-", dir=output.parent))
      staged = output.parent / f".{output.name}.glue-candidate-{os.getpid()}"
      if staged.exists():
        raise RuntimeError(f"candidate already exists: {staged}")
      try:
        prepared = staging_root / "prepared-source"
        try:
            core.copy_safe(source, prepared)
        except (OSError, shutil.Error) as exc:
            raise IntakeRejected([("template", f"cannot copy source tree: {exc}")]) from exc
        try:
            credential_scan.scan_tree(prepared)
        except credential_scan.CredentialScanRejected as exc:
            raise IntakeRejected(exc.failures) from exc
        cover, parsed, raw_cover, raw_answers = (parsed_intake.cover, parsed_intake.answers,
                                                  parsed_intake.raw_cover, parsed_intake.raw_answers)
        try:
            structured_filename = cross_seat.structured_answers_filename(mapping)
        except cross_seat.CrossSeatRejected as exc:
            raise IntakeRejected(exc.failures)
        old_manifest = []
        old_preserved = []
        old_seat = source / structured_filename
        if old_seat.is_file():
            old_engine = read_member_json(old_seat, structured_filename).get("configuration_engine", {})
            if not isinstance(old_engine, dict):
                raise IntakeRejected([(f"{structured_filename}.configuration_engine",
                                       "must be an object")])
            old_manifest = old_engine.get("managed_surfaces", [])
            old_preserved = old_engine.get("preserved_runtime_tokens", [])
            if (not isinstance(old_manifest, list) or any(not isinstance(item, dict) for item in old_manifest)
                    or not isinstance(old_preserved, list)
                    or any(not isinstance(item, dict) for item in old_preserved)):
                raise IntakeRejected([(f"{structured_filename}.configuration_engine",
                                       "managed surfaces and preserved tokens must be lists of objects")])
            try:
                cross_seat.validate_compatibility_guards(old_manifest, ENGINE_VERSION)
            except cross_seat.CrossSeatRejected as exc:
                raise IntakeRejected(exc.failures)
        try:
            if old_manifest:
                managed = placeholders.apply_rerun(prepared, mapping, raw_cover, raw_answers, core, old_manifest)
            elif old_seat.is_file() and (seat == "maintenance-coordinator" or old_engine):
                residual = [(str(path.relative_to(prepared)), name) for path in placeholders._text_files(prepared)
                            for name in placeholders.TOKEN.findall(path.read_text())]
                unknown = [(path, name) for path, name in residual if name not in placeholders.PRESERVED_RUNTIME_TOKENS]
                if unknown:
                    raise placeholders.PlaceholderRejected([(f"template.{path}", f"unmanaged placeholder {{{{{name}}}}} remains in configured source") for path, name in unknown])
                managed = []
            else:
                managed = placeholders.apply_initial(prepared, mapping, raw_cover, raw_answers, core)
        except placeholders.PlaceholderRejected as exc:
            raise IntakeRejected(exc.failures)
        try:
            preserved = (placeholders.verify_preserved_runtime_tokens(prepared, old_preserved)
                         if old_preserved else placeholders.preserved_runtime_manifest(prepared))
        except placeholders.PlaceholderRejected as exc:
            raise IntakeRejected(exc.failures)
        restore_mapping_core_counterpart(prepared, structured_filename, seat, old_manifest)
        try:
            if SUPPORTED[seat].get("runner") == "mapping":
                configuration_date = run_mapping_core(
                    core, prepared, answers, staged, SUPPORTED[seat]["library"], clock, seat, parsed_intake
                )
            else:
                configuration_date = run_sealed_core(
                    core, prepared, answers, staged, SUPPORTED[seat]["library"], clock
                )
        except RuntimeError as exc:
            stage = str(exc).partition(":")[0]
            if stage in {"credential-scan", "parse", "merge"}:
                raise IntakeRejected([(f"sealed_core.{stage}", str(exc))]) from exc
            raise
        structured_path = staged / structured_filename
        core_structured_path = staged / "seat-config.json"
        if structured_path != core_structured_path and core_structured_path.is_file():
            if structured_path.exists():
                source_declared_is_stale_counterpart = (
                    old_seat.is_file()
                    and structured_path.is_file()
                    and structured_path.read_bytes() == old_seat.read_bytes()
                )
                if source_declared_is_stale_counterpart:
                    structured_path.unlink()
                else:
                    raise IntakeRejected([(
                        "structured_answers_file",
                        f"declared structured artifact {structured_filename} conflicts with core output",
                    )])
            core_structured_path.replace(structured_path)
        if not structured_path.is_file():
            raise IntakeRejected([("structured_answers_file",
                                   f"declared structured artifact {structured_filename} is absent")])
        try:
            copy_protected(source, staged)
        except (OSError, shutil.Error) as exc:
            raise IntakeRejected([("protected_state", f"cannot preserve source state: {exc}")]) from exc
        placeholders.verify_preserved_runtime_tokens(staged, preserved)
        doctrine = mapping.get("cross_seat")
        if doctrine is not None:
            if seat_registry is None:
                raise IntakeRejected([("cross_seat", "schema v2 seam mapping requires an explicit seat registry")])
            seat_path = structured_path
            seat_payload = read_member_json(seat_path, structured_filename)
            try:
                seam_result = cross_seat.apply(
                    seat_payload, mapping, seat_registry, engine_version=ENGINE_VERSION
                )
            except cross_seat.CrossSeatRejected as exc:
                raise IntakeRejected(exc.failures)
            undeclared = cross_seat.undeclared_structured_artifacts(staged, mapping)
            if undeclared:
                seam_result.report_items.extend({
                    "check_id": f"undeclared-structured-{name}",
                    "doctrine": "STRUCTURED-ARTIFACT", "status": "UNDECLARED",
                    "value_name": name,
                } for name in undeclared)
            seat_path.write_text(json.dumps(seam_result.current, indent=2) + "\n")
            try:
                pointer_config = cross_seat.resolve_pointer_config_rows(
                    seam_result.current, mapping, seat_registry, engine_version=ENGINE_VERSION
                )
                config_rows = {row["path"]: row for row in mapping.get("config_keys", [])}
                for item in pointer_config:
                    try:
                        item["value"] = placeholders._typed_value(
                            config_rows[item["config_path"]], item["value"]
                        )
                    except ValueError as exc:
                        raise IntakeRejected([(
                            f"mapping.config_keys.{item['config_path']}",
                            f"pointer value coercion failed: {exc}",
                        )]) from exc
                placeholders.commit_config_manifest(staged, pointer_config)
            except (cross_seat.CrossSeatRejected, placeholders.PlaceholderRejected) as exc:
                raise IntakeRejected(exc.failures)
            managed.extend(pointer_config)
            report_path = staged / "contradiction-report.md"
            report_path.write_text(cross_seat.replace_report_block(
                report_path.read_text(), seam_result.report_items
            ))
            managed.append(cross_seat.compatibility_guard(ENGINE_VERSION))
        stamp(
            staged,
            seat,
            managed,
            preserved,
            parsed_intake.provenance,
            configuration_date,
            structured_filename,
        )
        try:
            credential_scan.scan_tree(staged)
        except credential_scan.CredentialScanRejected as exc:
            raise IntakeRejected(exc.failures) from exc
        shutil.rmtree(staging_root)
        result = transaction.replace_directory_transactional(staged, output, already_locked=True)
        if result.cleanup_warning:
            print(f"WARNING {result.cleanup_warning}", file=sys.stderr)
      except Exception:
        shutil.rmtree(staging_root, ignore_errors=True)
        shutil.rmtree(staged, ignore_errors=True)
        raise


def apply_persisted_append(appender: Path, owner: Path, plan_id: str,
                           *, appender_mapping=None, owner_mapping=None):
    """Replay one appender-owned plan through an atomic owner-directory transaction."""
    try:
        appender_filename = cross_seat.structured_answers_filename(appender_mapping or {})
        owner_filename = cross_seat.structured_answers_filename(owner_mapping or {})
    except cross_seat.CrossSeatRejected as exc:
        raise IntakeRejected(exc.failures)
    appender_seat = appender / appender_filename
    owner_seat = owner / owner_filename
    if not appender_seat.is_file() or not owner_seat.is_file():
        raise IntakeRejected([(
            "append-plan",
            f"declared structured artifacts {appender_filename} and {owner_filename} are required",
        )])
    appender_payload = read_member_json(appender_seat, f"appender.{appender_filename}")
    owner.parent.mkdir(parents=True, exist_ok=True)
    with transaction.DestinationLock(owner):
        transaction.recover_directory_transaction(owner)
        staged = owner.parent / f".{owner.name}.append-candidate-{os.getpid()}"
        if staged.exists():
            raise RuntimeError(f"append candidate already exists: {staged}")
        try:
            shutil.copytree(owner, staged, symlinks=True)
            staged_path = staged / owner_filename
            staged_payload = read_member_json(staged_path, f"owner.{owner_filename}")
            try:
                updated, changed = cross_seat.apply_append_plan(
                    staged_payload, appender_payload, plan_id, engine_version=ENGINE_VERSION
                )
            except cross_seat.CrossSeatRejected as exc:
                raise IntakeRejected(exc.failures)
            if not changed:
                shutil.rmtree(staged)
                return False
            staged_path.write_text(json.dumps(updated, indent=2) + "\n")
            transaction.replace_directory_transactional(staged, owner, already_locked=True)
            return True
        except Exception:
            shutil.rmtree(staged, ignore_errors=True)
            raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_agent_dir", type=Path)
    parser.add_argument("answers_file", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--seat", default="maintenance-coordinator")
    args = parser.parse_args()
    try:
        configure(
            *(p.resolve() for p in (args.source_agent_dir, args.answers_file, args.output_dir)),
            args.seat,
            seat_registry={},
        )
    except IntakeRejected as exc:
        print(exc.render(), file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
