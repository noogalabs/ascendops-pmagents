#!/usr/bin/env python3
"""Contract-level goldens that do not derive expected bytes from the run under test."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import unittest
import csv
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parent
DEMO = REPO / "editions" / "maintenance"
PROVENANCE_TSV = REPO / "provenance" / "source-files.tsv"
BASELINE_META = Path(__file__).with_name("fixtures") / "freeze-forward-baseline.json"
BASELINE_MANIFEST = Path(__file__).with_name("fixtures") / "freeze-forward-baseline.sha256"
RERUN_EVIDENCE_MANIFEST = (
    Path(__file__).with_name("fixtures") / "freeze-forward-rerun-evidence.sha256"
)

SPEC = importlib.util.spec_from_file_location("glue_engine_contract_goldens", HERE / "engine.py")
engine = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(engine)

P_ROWS = {
    "approval_threshold": "B1",
    "triage_sla_minutes": "B5",
    "property_manager_name": "C1",
    "platform": "D1",
    "day_mode_start": "B8",
    "day_mode_end": "B8",
    "timezone": "cover.timezone",
    "company_name": "cover.company_name",
    "org_name": "cover.org_short_name",
    "forward_email": "cover.forward_email",
}
ADD_AGENT_ROWS = {
    "agent_name": "maintenance",
    "org": "sample-org",
    "current_timestamp": "2026-08-24T00:00:00Z",
    "upstream_update_minute": "17",
}
GOLDEN_DATE = date(2026, 8, 25)


def tree_digest(path: Path):
    return [
        (str(item.relative_to(path)), hashlib.sha256(item.read_bytes()).hexdigest())
        for item in sorted(path.rglob("*"))
        if item.is_file()
    ]


def read_manifest(path: Path):
    rows = {}
    for line in path.read_text().splitlines():
        digest, relative = line.split("  ./", 1)
        rows[relative] = digest
    return rows


def read_baseline_manifest():
    return read_manifest(BASELINE_MANIFEST)


def assert_matches_frozen_baseline(test: unittest.TestCase, output: Path):
    expected = read_baseline_manifest()
    actual = {relative: digest for relative, digest in tree_digest(output)}
    test.assertEqual(set(actual), set(expected), "frozen baseline file census changed")
    test.assertEqual(actual, expected, "frozen baseline bytes changed")


def assert_matches_frozen_rerun(test: unittest.TestCase, output: Path):
    primary = read_baseline_manifest()
    evidence = read_manifest(RERUN_EVIDENCE_MANIFEST)
    actual = {relative: digest for relative, digest in tree_digest(output)}
    test.assertEqual(set(actual), set(primary), "rerun file census changed")
    for relative, digest in primary.items():
        if relative not in evidence:
            test.assertEqual(actual[relative], digest, f"rerun changed {relative}")
    test.assertEqual(
        {relative: actual[relative] for relative in evidence},
        evidence,
        "rerun evidence bytes changed",
    )


def prepare_raw_template(source: Path):
    shutil.copytree(HERE / "tests" / "fixtures" / "raw-maintenance-template", source, symlinks=True)
    for path in source.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for placeholder, value in ADD_AGENT_ROWS.items():
            text = text.replace("{{" + placeholder + "}}", value)
        path.write_text(text, encoding="utf-8")


def golden_clock():
    return GOLDEN_DATE


def assert_placeholder_manifest(test: unittest.TestCase, output: Path):
    seat_config = json.loads((output / "seat-config.json").read_text())
    rows = seat_config["configuration_engine"]["managed_surfaces"]
    test.assertIsInstance(rows, list)
    test.assertTrue(rows, "managed-surface manifest must not be empty")
    by_placeholder = {row["placeholder"]: [] for row in rows}
    for row in rows:
        test.assertEqual(
            set(row), {"placeholder", "question_id", "file", "count", "value"}
        )
        test.assertIn(row["placeholder"], P_ROWS)
        test.assertEqual(row["question_id"], P_ROWS[row["placeholder"]])
        test.assertIsInstance(row["file"], str)
        test.assertGreater(row["count"], 0)
        test.assertIsInstance(row["value"], str)
        by_placeholder.setdefault(row["placeholder"], []).append(row)
    test.assertEqual(set(by_placeholder), set(P_ROWS))

    for placeholder in P_ROWS:
        token = ("{{" + placeholder + "}}").encode()
        remaining = []
        for path in output.rglob("*"):
            if path.is_file() and token in path.read_bytes():
                remaining.append(str(path.relative_to(output)))
        test.assertEqual(remaining, [], f"unresolved P-row token {placeholder}")

    for placeholder, rows_for_placeholder in by_placeholder.items():
        recorded = sum(row["count"] for row in rows_for_placeholder)
        test.assertGreater(recorded, 0, f"manifest lacks substitutions for {placeholder}")
    preserved = seat_config["configuration_engine"]["preserved_runtime_tokens"]
    test.assertEqual(preserved, [{"token":"{{CTX_ROOT}}", "file":"ONBOARDING.md", "count":1}])
    test.assertEqual((output / "ONBOARDING.md").read_text().count("{{CTX_ROOT}}"), 1)


class ContractGoldenTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="betty-glue-contract-"))
        self.production_mapping = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        self.production_version = engine.ENGINE_VERSION
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = (
            HERE / "tests" / "fixtures" / "e2" / "maintenance-mapping-v1.json"
        )
        engine.ENGINE_VERSION = "1.0.0"

    def tearDown(self):
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = self.production_mapping
        engine.ENGINE_VERSION = self.production_version
        shutil.rmtree(self.tmp)

    def test_named_excluded_evidence_is_hash_pinned_without_importing_history(self):
        """Pin excluded evidence by hash and retention location, not private Git history."""
        print("ARMED: excluded review evidence is hash-pinned in seed provenance")
        with PROVENANCE_TSV.open(newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        excluded = [row for row in rows if row["disposition"] == "excluded-evidence"]
        self.assertEqual(len(excluded), 33)
        self.assertEqual(len({row["artifact_id"] for row in excluded}), len(excluded))
        for row in excluded:
            self.assertRegex(row["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(row["reviewed_head"], r"^[0-9a-f]{8,40}$")
            self.assertTrue(row["retention_location"].startswith("orgs/ascendops/ops/pmagents-evidence/"))

    def test_named_freeze_forward_metadata_pins_real_qa_approved_bytes(self):
        print("ARMED: freeze-forward manifest and provenance are immutable")
        metadata = json.loads(BASELINE_META.read_text())
        self.assertEqual(metadata["pinned_configuration_date"], GOLDEN_DATE.isoformat())
        self.assertEqual(metadata["sealed_core_sha256"], engine.SEALED_CORE_SHA256)
        self.assertEqual(
            hashlib.sha256(BASELINE_MANIFEST.read_bytes()).hexdigest(),
            metadata["manifest_sha256"],
        )
        self.assertEqual(len(read_baseline_manifest()), metadata["file_count"])
        self.assertEqual(
            metadata["reproducibility_runs"],
            ["freeze-forward-raw-1", "freeze-forward-raw-2"],
        )
        rerun = metadata["rerun_evidence"]
        self.assertEqual(
            hashlib.sha256(RERUN_EVIDENCE_MANIFEST.read_bytes()).hexdigest(),
            rerun["manifest_sha256"],
        )
        self.assertEqual(
            rerun["runs"],
            ["freeze-forward-rerun-1", "freeze-forward-rerun-2"],
        )
        self.assertEqual(metadata["qa"]["status"], "seed-derived-from-approved-baseline")

    def test_named_raw_and_configured_rerun_match_frozen_baseline(self):
        print("ARMED: raw and configured rerun byte-diff against frozen QA baseline")
        reruns = []
        for number in (1, 2):
            source = self.tmp / f"raw-rerun-{number}"
            output = self.tmp / f"configured-rerun-{number}"
            prepare_raw_template(source)
            engine.configure(
                source,
                DEMO / "fixtures" / "ridgeline-maintenance-answers.md",
                output,
                "maintenance-coordinator",
                clock=golden_clock,
            )
            assert_matches_frozen_baseline(self, output)
            engine.configure(
                output,
                DEMO / "fixtures" / "ridgeline-maintenance-answers.md",
                output,
                "maintenance-coordinator",
                clock=golden_clock,
            )
            assert_matches_frozen_rerun(self, output)
            reruns.append(tree_digest(output))
        self.assertEqual(reruns[0], reruns[1])

    def test_named_non_date_mutation_kills_frozen_manifest_comparison(self):
        print("ARMED: planted non-date mutation kills frozen full-tree comparison")
        source = self.tmp / "raw"
        output = self.tmp / "configured"
        prepare_raw_template(source)
        engine.configure(
            source,
            DEMO / "fixtures" / "ridgeline-maintenance-answers.md",
            output,
            "maintenance-coordinator",
            clock=golden_clock,
        )
        assert_matches_frozen_baseline(self, output)
        with (output / "GUARDRAILS.md").open("a") as handle:
            handle.write("\nPLANTED-NON-DATE-MUTATION\n")
        with self.assertRaisesRegex(AssertionError, "frozen baseline bytes changed"):
            assert_matches_frozen_baseline(self, output)

    def test_named_unmapped_seat_rejects_through_configure_with_zero_writes(self):
        print("ARMED: unmapped seat production path rejects with zero filesystem writes")
        source = self.tmp / "source"
        source.mkdir()
        answers = DEMO / "fixtures" / "ridgeline-maintenance-answers.md"
        output = self.tmp / "output"
        before = tree_digest(self.tmp)
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(source, answers, output, "bookkeeper")
        self.assertIn("no mapping table/library", caught.exception.render())
        self.assertFalse(output.exists())
        self.assertEqual(tree_digest(self.tmp), before)

    def test_named_manifest_same_count_decoy_cannot_launder_hand_edit(self):
        """A value/count manifest must not confuse an organic decoy with its surface."""
        print("ARMED: same-count decoy cannot redirect a managed rerun replacement")
        target = self.tmp / "agent"
        target.mkdir()
        path = target / "GUARDRAILS.md"
        path.write_text("managed: HAND_EDIT\norganic: 500\n")
        mapping = {
            "placeholders": [
                {
                    "placeholder": "approval_threshold",
                    "source": "B1",
                    "extractor": "currency",
                }
            ]
        }
        manifest = [
            {
                "placeholder": "approval_threshold",
                "question_id": "B1",
                "file": "GUARDRAILS.md",
                "count": 1,
                "value": "500",
            }
        ]
        core = engine.load_core()
        before = path.read_bytes()
        with self.assertRaises(engine.placeholders.PlaceholderRejected):
            engine.placeholders.apply_rerun(
                target, mapping, {}, {"B1": "$750 base owner threshold"}, core, manifest
            )
        self.assertEqual(path.read_bytes(), before)

    def test_named_raw_template_golden_has_zero_p_rows_and_two_way_manifest(self):
        """Raw template applies every P-row and preserves classified runtime tokens."""
        print("ARMED: raw template P-row substitution and manifest two-way census")
        source = self.tmp / "raw-maintenance"
        prepare_raw_template(source)
        output = self.tmp / "configured"
        engine.configure(
            source,
            DEMO / "fixtures" / "ridgeline-maintenance-answers.md",
            output,
            "maintenance-coordinator",
        )
        assert_placeholder_manifest(self, output)

    def test_named_frozen_clock_makes_two_fresh_raw_runs_byte_identical(self):
        """A real frozen date makes a future committed tree manifest reproducible."""
        print("ARMED: frozen golden clock yields byte-identical independent raw runs")
        outputs = []
        for number in (1, 2):
            source = self.tmp / f"raw-{number}"
            output = self.tmp / f"configured-{number}"
            prepare_raw_template(source)
            engine.configure(
                source,
                DEMO / "fixtures" / "ridgeline-maintenance-answers.md",
                output,
                "maintenance-coordinator",
                clock=golden_clock,
            )
            outputs.append(output)
        self.assertEqual(tree_digest(outputs[0]), tree_digest(outputs[1]))
        seat_config = json.loads((outputs[0] / "seat-config.json").read_text())
        self.assertEqual(seat_config["provenance"]["date"], GOLDEN_DATE.isoformat())
        self.assertEqual(
            seat_config["configuration_engine"]["configuration_date"],
            GOLDEN_DATE.isoformat(),
        )


if __name__ == "__main__":
    print("ARMED: immutable accepted evidence, production rejection, and raw-template golden")
    unittest.main(verbosity=2)
