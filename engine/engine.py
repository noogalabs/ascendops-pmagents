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
import intake
import transaction

ENGINE_VERSION = "1.1.0"
ROOT = Path(__file__).resolve().parents[1]
MAINTENANCE_EDITION = ROOT / "editions" / "maintenance"
SEALED_CORE = MAINTENANCE_EDITION / "configure_agent.py"
SEALED_CORE_SHA256 = "0540ea08aa8d47ecb1aebbb7f51db85c5a67ab252172804e9ba24e56c2403551"
SUPPORTED = {
    "maintenance-coordinator": {
        "library_id": "maintenance-2026-08-23",
        "answers": MAINTENANCE_EDITION / "answers-format.md",
        "library": MAINTENANCE_EDITION / "library-src",
        "mapping": Path(__file__).resolve().parent / "mappings" / "maintenance-coordinator.json",
    }
}


IntakeRejected = intake.IntakeRejected


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
    return intake.preflight(path, load_core().QUESTION_IDS)


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
        core.copy_safe(source, prepared)
        cover, parsed, raw_cover, raw_answers = (parsed_intake.cover, parsed_intake.answers,
                                                  parsed_intake.raw_cover, parsed_intake.raw_answers)
        mapping = placeholders.load_mapping(SUPPORTED[seat]["mapping"])
        try:
            structured_filename = cross_seat.structured_answers_filename(mapping)
        except cross_seat.CrossSeatRejected as exc:
            raise IntakeRejected(exc.failures)
        old_manifest = []
        old_preserved = []
        old_seat = source / structured_filename
        if old_seat.is_file():
            old_engine = json.loads(old_seat.read_text()).get("configuration_engine", {})
            old_manifest = old_engine.get("managed_surfaces", [])
            old_preserved = old_engine.get("preserved_runtime_tokens", [])
            try:
                cross_seat.validate_compatibility_guards(old_manifest, ENGINE_VERSION)
            except cross_seat.CrossSeatRejected as exc:
                raise IntakeRejected(exc.failures)
        try:
            if old_manifest:
                managed = placeholders.apply_rerun(prepared, mapping, raw_cover, raw_answers, core, old_manifest)
            elif old_seat.is_file():
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
        preserved = (placeholders.verify_preserved_runtime_tokens(prepared, old_preserved)
                     if old_preserved else placeholders.preserved_runtime_manifest(prepared))
        configuration_date = run_sealed_core(
            core, prepared, answers, staged, SUPPORTED[seat]["library"], clock
        )
        structured_path = staged / structured_filename
        core_structured_path = staged / "seat-config.json"
        if structured_path != core_structured_path and core_structured_path.is_file():
            if structured_path.exists():
                raise IntakeRejected([(
                    "structured_answers_file",
                    f"declared structured artifact {structured_filename} conflicts with core output",
                )])
            core_structured_path.replace(structured_path)
        if not structured_path.is_file():
            raise IntakeRejected([("structured_answers_file",
                                   f"declared structured artifact {structured_filename} is absent")])
        copy_protected(source, staged)
        placeholders.verify_preserved_runtime_tokens(staged, preserved)
        doctrine = mapping.get("cross_seat")
        if doctrine is not None:
            if seat_registry is None:
                raise IntakeRejected([("cross_seat", "schema v2 seam mapping requires an explicit seat registry")])
            seat_path = structured_path
            seat_payload = json.loads(seat_path.read_text())
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
    appender_payload = json.loads(appender_seat.read_text())
    owner.parent.mkdir(parents=True, exist_ok=True)
    with transaction.DestinationLock(owner):
        transaction.recover_directory_transaction(owner)
        staged = owner.parent / f".{owner.name}.append-candidate-{os.getpid()}"
        if staged.exists():
            raise RuntimeError(f"append candidate already exists: {staged}")
        try:
            shutil.copytree(owner, staged, symlinks=True)
            staged_path = staged / owner_filename
            staged_payload = json.loads(staged_path.read_text())
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
        configure(*(p.resolve() for p in (args.source_agent_dir, args.answers_file, args.output_dir)), args.seat)
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
