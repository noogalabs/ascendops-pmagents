#!/usr/bin/env python3
from __future__ import annotations

import datetime
import ast
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pmagents_setup", ROOT / "setup.py")
setup = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(setup)
PRODUCTION_INTAKE_CONSUMER_MANIFEST = {
    "setup.py": {"kind": "shared"},
    "engine/intake.py": {"kind": "shared"},
    "editions/maintenance/configure_agent.py": {
        "kind": "sealed",
        "sha256": "0540ea08aa8d47ecb1aebbb7f51db85c5a67ab252172804e9ba24e56c2403551",
    },
}


def production_intake_consumer_sets(root: Path, supported):
    on_disk = {
        str(path.relative_to(root))
        for path in root.glob("editions/*/configure_agent.py")
    }
    registry_sealed = {
        str((entry["answers"].parent / "configure_agent.py").relative_to(root))
        for entry in supported.values() if entry.get("runner") == "sealed"
    }
    return {"setup.py", "engine/intake.py", *on_disk}, registry_sealed, on_disk


def tree_digest(root: Path):
    return [
        (str(path.relative_to(root)), hashlib.sha256(path.read_bytes()).hexdigest())
        for path in sorted(root.rglob("*")) if path.is_file()
    ]


class ZeroTouchSetupTests(unittest.TestCase):
    def test_named_every_intake_text_consumer_uses_shared_multiline_surface(self):
        print("ARMED: intake-format readers and writers cannot fork a single-line value grammar")
        discovered_consumers, registry_sealed, on_disk = production_intake_consumer_sets(
            ROOT, setup.engine.SUPPORTED)
        self.assertEqual(on_disk, registry_sealed,
                         "edition configurator exists outside the sealed registry")
        self.assertEqual(discovered_consumers, set(PRODUCTION_INTAKE_CONSUMER_MANIFEST),
                         "production intake consumer manifest is incomplete")
        sources = {
            path: (ROOT / path).read_text()
            for path, row in PRODUCTION_INTAKE_CONSUMER_MANIFEST.items()
            if row["kind"] == "shared"
        }
        framing_allowlist = {
            ("setup.py", "answer_values", "cover-label-frame"):
                "matches only the cover label; indented_value consumes its value",
            ("setup.py", "answer_values", "question-heading-frame"):
                "selects the question id; indented_value consumes the Answer block",
            ("engine/intake.py", "preflight", "cover-label-frame"):
                "matches only the cover label; indented_value consumes its value",
            ("engine/intake.py", "preflight", "question-heading-frame"):
                "selects the question id; indented_value consumes the Answer block",
        }
        discovered = []
        private_grammars = []
        for module, source in sources.items():
            tree = ast.parse(source)
            parents = {}
            for parent in ast.walk(tree):
                for child in ast.iter_child_nodes(parent):
                    parents[child] = parent
            def owning_function(node):
                while node in parents:
                    node = parents[node]
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        return node.name
                return "<module>"
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    if (r"^[ \t]+(?:\S[^\n]*)?$" in node.value or
                            r"[^\n]*(?:\n[ \t]+[^\n]*)*" in node.value):
                        private_grammars.append((module, node.lineno, node.value))
                if not isinstance(node, ast.Call):
                    continue
                function = owning_function(node)
                segment = ast.get_source_segment(source, node) or ""
                if "indented_value(" in segment:
                    discovered.append((module, function, "shared-reader"))
                elif "collect_answer(" in segment:
                    discovered.append((module, function, "shared-interactive-collector"))
                elif ("re.escape(label)" in segment
                      and ("re.match" in segment or "re.findall" in segment)):
                    discovered.append((module, function, "cover-label-frame"))
                elif "QUESTION_LINE.match" in segment:
                    discovered.append((module, function, "question-heading-frame"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute) and node.attr == "INTAKE_VALUE_SPAN":
                    function = owning_function(node)
                    discovered.append((module, function, "shared-writer-span"))

        canonical_grammars = [row for row in private_grammars if row[0] == "engine/intake.py"]
        self.assertEqual(len(canonical_grammars), 2, canonical_grammars)
        self.assertFalse([row for row in private_grammars if row[0] != "engine/intake.py"])
        unclassified = [row for row in discovered
                        if not row[2].startswith("shared-") and row not in framing_allowlist]
        self.assertFalse(unclassified, f"unclassified intake consumers: {unclassified}")
        self.assertEqual({row for row in discovered if row[2].endswith("-frame")},
                         set(framing_allowlist))
        for path, row in PRODUCTION_INTAKE_CONSUMER_MANIFEST.items():
            if row["kind"] != "sealed":
                continue
            self.assertIn(path, registry_sealed)
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
                             row["sha256"],
                             f"sealed intake consumer {path} changed without census review")
        self.assertGreaterEqual(sum(row[2] == "shared-reader" for row in discovered), 4)
        self.assertGreaterEqual(sum(row[2] == "shared-writer-span" for row in discovered), 2)
        self.assertGreaterEqual(sum(row[2] == "shared-interactive-collector" for row in discovered), 2)

    def test_named_unmanifested_edition_configurator_dies(self):
        print("ARMED: an edition configurator outside the production manifest kills the census")
        root = Path(tempfile.mkdtemp(prefix="pmagents-consumer-census-"))
        self.addCleanup(shutil.rmtree, root)
        (root / "setup.py").write_text("")
        (root / "engine").mkdir()
        (root / "engine/intake.py").write_text("")
        edition = root / "editions" / "rogue"
        edition.mkdir(parents=True)
        (edition / "configure_agent.py").write_text("def parse_answers(path): pass\n")
        discovered, registry_sealed, on_disk = production_intake_consumer_sets(root, {})
        self.assertNotEqual(on_disk, registry_sealed)
        self.assertNotEqual(discovered, set(PRODUCTION_INTAKE_CONSUMER_MANIFEST))

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pmagents-zero-touch-"))
        self.source = self.tmp / "source"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", self.source)
        replacements = {
            "agent_name": "ridge-maint",
            "org": "ridgeline",
            "current_timestamp": "2026-08-25T00:00:00Z",
            "upstream_update_minute": "17",
        }
        for path in self.source.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text()
            for name, value in replacements.items():
                text = text.replace("{{" + name + "}}", value)
            path.write_text(text)
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        parsed = setup.engine.intake.preflight(fixture, setup.engine.load_core().QUESTION_IDS)
        self.responses = list(parsed.raw_cover.values()) + [
            parsed.raw_answers[q] for q in setup.engine.load_core().QUESTION_IDS
        ]

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def configure_completed(self, seat: str, output: Path, out=None):
        fixtures = {
            "turnover-coordinator": ROOT / "editions/turnover/fixtures/ridgeline-turnover-answers.md",
            "accounting": ROOT / "editions/accounting/fixtures/ridgeline-accounting-answers.md",
        }
        seat_number = next(number for number, row in enumerate(setup.SEATS, 1)
                           if row["id"] == seat)
        scripted = iter([
            str(seat_number), str(setup.engine.SUPPORTED[seat]["library"]),
            str(output), "2", str(fixtures[seat]),
        ])
        rendered = io.StringIO() if out is None else out
        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), out=rendered,
            clock=lambda: datetime.date(2026, 8, 26),
        ), 0)
        return rendered

    def structured_payload(self, seat: str, output: Path):
        mapping = setup.engine.load_seat_mapping(seat)
        filename = setup.engine.cross_seat.structured_answers_filename(mapping)
        return json.loads((output / filename).read_text())

    def test_named_sibling_discovery_resolves_live_turnover_owner_read_only(self):
        print("ARMED: removing sibling discovery returns the accounting pointer to held")
        installs = self.tmp / "installed"
        turnover = installs / "turnover"
        accounting = installs / "accounting"
        self.configure_completed("turnover-coordinator", turnover)
        peer_before = tree_digest(turnover)
        stdout = self.configure_completed("accounting", accounting)
        payload = self.structured_payload("accounting", accounting)
        pointer = payload["cross_seat"]["pointers"]["deposit_chargeback_threshold"]
        self.assertEqual(
            (pointer["owner_seat"], pointer["owner_question_id"], pointer["state"]),
            ("turnover-coordinator", "C7", "resolved"),
        )
        self.assertIsInstance(pointer["resolved_owner_schema"], int)
        self.assertNotIn("deposit_chargeback_threshold", payload["cross_seat"]["held"])
        self.assertIn(
            "Connected pointer deposit_chargeback_threshold: resolved from turnover-coordinator",
            stdout.getvalue(),
        )
        self.assertEqual(tree_digest(turnover), peer_before)

    def test_named_sibling_discovery_is_order_independent_on_rerun(self):
        print("ARMED: reverse-order installs resolve when the dependent seat reruns")
        installs = self.tmp / "reverse-installed"
        accounting = installs / "accounting"
        turnover = installs / "turnover"
        self.configure_completed("accounting", accounting)
        first = self.structured_payload("accounting", accounting)
        self.assertEqual(first["cross_seat"]["held"]["deposit_chargeback_threshold"][
            "held_pending_seat"], "turnover-coordinator")
        self.configure_completed("turnover-coordinator", turnover)
        peer_before = tree_digest(turnover)
        self.configure_completed("accounting", accounting)
        second = self.structured_payload("accounting", accounting)
        self.assertEqual(second["cross_seat"]["pointers"]["deposit_chargeback_threshold"][
            "state"], "resolved")
        self.assertEqual(tree_digest(turnover), peer_before)

    def test_named_single_seat_install_keeps_pending_owner_visible(self):
        print("ARMED: absent sibling owners stay explicitly held")
        output = self.tmp / "single-installed" / "accounting"
        stdout = self.configure_completed("accounting", output)
        payload = self.structured_payload("accounting", output)
        held = payload["cross_seat"]["held"]["deposit_chargeback_threshold"]
        self.assertEqual(held["held_pending_seat"], "turnover-coordinator")
        self.assertIn(
            "Connected pointer deposit_chargeback_threshold: held pending turnover-coordinator",
            stdout.getvalue(),
        )

    def test_named_incompatible_sibling_is_excluded_loudly(self):
        print("ARMED: a newer peer cannot enter the member-run registry")
        installs = self.tmp / "version-installed"
        turnover = installs / "turnover"
        accounting = installs / "accounting"
        self.configure_completed("turnover-coordinator", turnover)
        peer = self.structured_payload("turnover-coordinator", turnover)
        peer["configuration_engine"]["version"] = "999.0.0"
        (turnover / "turnover-config.json").write_text(json.dumps(peer, indent=2) + "\n")
        peer_before = tree_digest(turnover)
        stdout = self.configure_completed("accounting", accounting)
        payload = self.structured_payload("accounting", accounting)
        self.assertIn("deposit_chargeback_threshold", payload["cross_seat"]["held"])
        self.assertIn("Excluded connected seat turnover-coordinator", stdout.getvalue())
        self.assertIn("newer than reader", stdout.getvalue())
        self.assertEqual(tree_digest(turnover), peer_before)

    def test_named_incomplete_sibling_is_not_registered(self):
        print("ARMED: neither half of a completed sibling can enter the registry alone")
        installs = self.tmp / "incomplete-installed"
        config_only = installs / "config-only"
        config_only.mkdir(parents=True)
        (config_only / "config.json").write_text("{}\n")
        complete = self.tmp / "complete-turnover"
        self.configure_completed("turnover-coordinator", complete)
        artifact_only = installs / "artifact-only"
        artifact_only.mkdir(parents=True)
        shutil.copy2(complete / "turnover-config.json", artifact_only)
        accounting = installs / "accounting"
        self.configure_completed("accounting", accounting)
        payload = self.structured_payload("accounting", accounting)
        self.assertIn("deposit_chargeback_threshold", payload["cross_seat"]["held"])

    def test_named_duplicate_complete_sibling_identity_rejects_before_output(self):
        print("ARMED: removing duplicate identity detection silently selects a stale peer")
        complete = self.tmp / "duplicate-source"
        self.configure_completed("turnover-coordinator", complete)
        installs = self.tmp / "duplicate-installed"
        first = installs / "turnover-a"
        second = installs / "turnover-b"
        shutil.copytree(complete, first)
        shutil.copytree(complete, second)
        output = installs / "accounting"
        seat_number = next(number for number, row in enumerate(setup.SEATS, 1)
                           if row["id"] == "accounting")
        fixture = ROOT / "editions/accounting/fixtures/ridgeline-accounting-answers.md"
        scripted = iter([
            str(seat_number), str(setup.engine.SUPPORTED["accounting"]["library"]),
            str(output), "2", str(fixture),
        ])
        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), out=io.StringIO(), err=stderr,
            clock=lambda: datetime.date(2026, 8, 26),
        ), 2)
        rendered = stderr.getvalue()
        self.assertIn("duplicate connected seat turnover-coordinator", rendered)
        self.assertIn(str(first), rendered)
        self.assertIn(str(second), rendered)
        self.assertFalse(output.exists())

    def test_named_setup_constructs_sibling_registry_once_for_both_answer_modes(self):
        print("ARMED: guided and completed modes cannot fork sibling discovery")
        source = (ROOT / "setup.py").read_text()
        tree = ast.parse(source)
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Name)
                 and node.func.id == "discover_seat_registry"]
        self.assertEqual(len(calls), 1)
        run_setup = next(node for node in tree.body
                         if isinstance(node, ast.FunctionDef) and node.name == "run_setup")
        self.assertIn(calls[0], set(ast.walk(run_setup)))

    def test_named_fresh_member_readme_path_materializes_before_engine_start(self):
        print("ARMED: removing setup materialization reproduces the fresh-seat token wall")
        output = self.tmp / "orgs" / "ridgeline" / "agents" / "ridge-maint"
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        result = subprocess.run(
            [sys.executable, str(ROOT / "setup.py")],
            cwd=ROOT,
            input=f"1\n\n{output}\n2\n{fixture}\n",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"Configured agent: {output.resolve()}", result.stdout)
        self.assertTrue((output / "seat-config.json").is_file())
        rendered = "\n".join(
            path.read_text(encoding="utf-8")
            for path in output.rglob("*")
            if path.is_file() and not path.is_symlink()
        )
        for token in setup.SCAFFOLD_TOKENS:
            self.assertNotIn("{{" + token + "}}", rendered)
        config = json.loads((output / "config.json").read_text())
        self.assertEqual(config["agent_name"], "ridge-maint")
        self.assertIn("**Organization:** ridgeline", (output / "SYSTEM.md").read_text())
        update_cron = next(row for row in config["crons"]
                           if row["name"] == "daily-framework-upstream-auto-update")
        self.assertEqual(update_cron["cron"].split()[0],
                         str(setup.upstream_update_minute("ridge-maint")))
        self.assertEqual(json.loads((output / "copilot-thresholds.json").read_text())["agent"],
                         "ridge-maint")

    def test_named_guided_happy_path_equals_direct_configure_bytes(self):
        print("ARMED: wrapper artifact mutation dies against direct configure bytes")
        wrapped = self.tmp / "wrapped"
        direct = self.tmp / "direct"
        answers = self.tmp / "guided-answers.md"
        terminated = [item for response in self.responses for item in (response, "")]
        scripted = iter([
            "1", str(self.source), str(wrapped), "1", str(answers), *terminated,
        ])
        clock = lambda: datetime.date(2026, 8, 25)
        stdout = io.StringIO()
        code = setup.run_setup(ask=lambda _prompt: next(scripted), out=stdout, clock=clock)
        self.assertEqual(code, 0)
        setup.engine.configure(
            self.source,
            answers,
            direct,
            "maintenance-coordinator",
            clock=clock,
            seat_registry={},
        )
        self.assertEqual(tree_digest(wrapped), tree_digest(direct))
        self.assertIn(f"Configured agent: {wrapped.resolve()}", stdout.getvalue())

    def test_named_mapping_declared_extra_cover_fields_flow_through_guided_setup(self):
        print("ARMED: mapping-declared extra cover fields flow through production guided setup")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        answers_template = self.tmp / "extra-cover-answers-format.md"
        answers_template.write_text(fixture.read_text().replace(
            "Timezone: America/Denver\n",
            "Timezone: America/Denver\nPortfolio code: ____________________\n",
        ))
        mapping = self.tmp / "extra-cover-mapping.json"
        mapping_payload = json.loads(
            setup.engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text()
        )
        mapping_payload["cover_fields"] = [
            {"label": label, "key": key}
            for label, key in setup.engine.intake.COVER_FIELDS.items()
        ] + [{"label": "Portfolio code", "key": "portfolio_code"}]
        mapping.write_text(json.dumps(mapping_payload, indent=2) + "\n")
        seat = "test-extra-cover"
        original_seats = setup.SEATS
        setup.engine.SUPPORTED[seat] = {
            "library_id": "test-extra-cover-2026-08-25",
            "answers": answers_template,
            "library": ROOT / "editions" / "maintenance" / "library-src",
            "mapping": mapping,
            "question_ids": list(setup.engine.load_core().QUESTION_IDS),
            "runner": "mapping",
        }
        setup.SEATS = (*original_seats, {"id": seat, "label": "Test extra cover"})
        try:
            output = self.tmp / "extra-cover-output"
            answers = self.tmp / "extra-cover-guided.md"
            (self.source / "seat-config.json").write_text("{}\n")
            scripted = iter([
                str(len(setup.SEATS)), str(self.source), str(output), "1", str(answers),
                "portfolio-17\nsecondary", "",
            ])
            self.assertEqual(setup.run_setup(
                ask=lambda _prompt: next(scripted),
                clock=lambda: datetime.date(2026, 8, 25),
            ), 0)
            configured = json.loads((output / "seat-config.json").read_text())
            self.assertEqual(configured["cover_sheet"]["portfolio_code"],
                             "[documented] portfolio-17\nsecondary")
            self.assertIn("Portfolio code: [documented] portfolio-17\n  secondary",
                          answers.read_text())
        finally:
            setup.SEATS = original_seats
            setup.engine.SUPPORTED.pop(seat, None)

    def test_named_mapping_without_cover_declaration_gets_exact_standard_four(self):
        print("ARMED: absent cover_fields declaration defaults to exactly the standard four")
        fields = setup.engine.cover_fields_for_seat("maintenance-coordinator")
        self.assertEqual(fields, setup.engine.intake.COVER_FIELDS)
        prompted = [field.label for field in setup.questionnaire_fields(
            setup.engine.SUPPORTED["maintenance-coordinator"]["answers"].read_text(), fields
        ) if field.key.startswith("cover.")]
        self.assertEqual(prompted, list(setup.engine.intake.COVER_FIELDS))

    def test_named_guided_setup_collects_declared_e_questions(self):
        print("ARMED: production guided setup collects declared E questions")
        template = self.tmp / "e-question-answers-format.md"
        template.write_text(
            "Company name: ____________________\n"
            "Org short-name: ____________________\n"
            "Forward email: ____________________\n"
            "Timezone: ____________________\n\n"
            "E1. What is the turnover escalation rule?\n\n"
            "Answer: ____________________\n"
        )
        answers = self.tmp / "e-question-answers.md"
        seat = "test-e-question"
        setup.engine.SUPPORTED[seat] = {
            "library_id": "test-e-question-2026-08-26",
            "answers": template,
            "library": ROOT / "editions" / "maintenance" / "library-src",
            "mapping": setup.engine.SUPPORTED["maintenance-coordinator"]["mapping"],
            "question_ids": ["E1"],
            "runner": "mapping",
        }
        try:
            raw_responses = [
                "Example Company", "example", "ops@example.invalid", "America/Denver",
                "Escalate after operator review",
            ]
            responses = iter([item for response in raw_responses for item in (response, "")])
            setup.guided_answers(answers, lambda _prompt: next(responses), io.StringIO(), seat)
            text = answers.read_text()
            self.assertIn("E1. What is the turnover escalation rule?", text)
            self.assertIn("Answer: [documented] Escalate after operator review", text)
            self.assertEqual(
                setup.answer_values(text)["E1"],
                "[documented] Escalate after operator review",
            )
            parsed = setup.engine.validate(answers, seat)
            self.assertEqual(
                parsed.raw_answers["E1"],
                "[documented] Escalate after operator review",
            )
        finally:
            setup.engine.SUPPORTED.pop(seat, None)

    def test_named_guided_multiline_answer_reaches_two_labeled_runtime_values(self):
        print("ARMED: guided multiline B8-style answer reaches both labeled config values")
        template = ROOT / "editions" / "leasing" / "answers-format.md"
        fixture = ROOT / "editions" / "leasing" / "fixtures" / "ridgeline-leasing-answers.md"
        mapping = self.tmp / "multiline-mapping.json"
        mapping_payload = json.loads(
            setup.engine.SUPPORTED["leasing-coordinator"]["mapping"].read_text()
        )
        mapping_payload["config_keys"].extend([
            {"path": "/owner_draw_deadline_day", "source": "B8",
             "extractor": "labeled_integer", "label": "Owner draw deadline day",
             "value_type": "integer", "minimum": 1, "mode": "create"},
            {"path": "/owner_draw_target_day", "source": "B8",
             "extractor": "labeled_integer", "label": "Owner draw target day",
             "value_type": "integer", "minimum": 1, "mode": "create"},
        ])
        mapping.write_text(json.dumps(mapping_payload, indent=2) + "\n")
        source = ROOT / "editions" / "leasing" / "library-src"
        output = self.tmp / "multiline-output"
        answers = self.tmp / "multiline-guided.md"
        seat = "test-multiline"
        original_seats = setup.SEATS
        setup.engine.SUPPORTED[seat] = {
            "library_id": "test-multiline-2026-08-26", "answers": template,
            "library": source, "mapping": mapping,
            "question_ids": setup.engine.SUPPORTED["leasing-coordinator"]["question_ids"],
            "runner": "mapping",
        }
        setup.SEATS = (*original_seats, {"id": seat, "label": "Test multiline"})
        try:
            parsed = setup.engine.validate(fixture, "leasing-coordinator")
            responses = list(parsed.raw_cover.values()) + [
                parsed.raw_answers[q]
                for q in setup.engine.SUPPORTED["leasing-coordinator"]["question_ids"]
            ]
            b8_index = len(parsed.raw_cover) + list(
                setup.engine.SUPPORTED["leasing-coordinator"]["question_ids"]
            ).index("B8")
            responses[b8_index] = (
                "Owner draw deadline day: 15\nOwner draw target day: 10"
            )
            terminated = [item for response in responses for item in (response, "")]
            scripted = iter([
                str(len(setup.SEATS)), str(source), str(output), "1", str(answers),
                *terminated,
            ])
            self.assertEqual(setup.run_setup(
                ask=lambda _prompt: next(scripted),
                clock=lambda: datetime.date(2026, 8, 26),
            ), 0)
            config = json.loads((output / "config.json").read_text())
            self.assertEqual(
                (config["owner_draw_deadline_day"], config["owner_draw_target_day"]),
                (15, 10),
            )
            self.assertIn(
                "Answer: [documented] Owner draw deadline day: 15\n"
                "  Owner draw target day: 10",
                answers.read_text(),
            )
            self.assertIn("### What Happens Next", answers.read_text())
            self.assertIn("Keep the answers current", answers.read_text())
        finally:
            setup.SEATS = original_seats
            setup.engine.SUPPORTED.pop(seat, None)

    def test_named_indented_blank_preserves_and_replaces_answer_paragraphs(self):
        print("ARMED: indented blank separators preserve and replace full answer paragraphs")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        answers = self.tmp / "paragraph-answers.md"
        field = next(
            item for item in setup.questionnaire_fields(fixture.read_text())
            if item.key == "A1"
        )
        value = "[documented] First paragraph.\n\nSecond paragraph."
        rendered = setup.set_answer(fixture.read_text(), field, value)
        answers.write_text(rendered)
        self.assertIn(
            "Answer: [documented] First paragraph.\n  \n  Second paragraph.",
            rendered,
        )
        self.assertEqual(setup.answer_values(rendered)["A1"], value)
        parsed = setup.engine.intake.preflight(answers, setup.engine.load_core().QUESTION_IDS)
        self.assertEqual(parsed.raw_answers["A1"], value)

        replacement = "[documented] Replacement paragraph."
        corrected = setup.set_answer(rendered, field, replacement)
        self.assertNotIn("Second paragraph.", corrected)
        self.assertEqual(setup.answer_values(corrected)["A1"], replacement)

    def test_named_create_then_reconfigure_succeeds_through_wrapper(self):
        print("ARMED: wrapper create then reconfigure uses the production rerun entry")
        output = self.tmp / "configured"
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        clock = lambda: datetime.date(2026, 8, 25)
        for _run in (1, 2):
            scripted = iter(["1", str(self.source), str(output), "2", str(fixture)])
            self.assertEqual(setup.run_setup(ask=lambda _prompt: next(scripted), clock=clock), 0)
        self.assertTrue((output / "seat-config.json").is_file())

    def test_named_member_interrupt_leaves_no_partial_configured_output(self):
        print("ARMED: interrupt before configure leaves zero output bytes")
        output = self.tmp / "never-configured"
        answers = self.tmp / "partial-answers.md"
        responses = iter(["1", str(self.source), str(output), "1", str(answers)])

        def interrupt_after_paths(_prompt):
            try:
                return next(responses)
            except StopIteration:
                raise KeyboardInterrupt

        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(ask=interrupt_after_paths, err=stderr), 130)
        self.assertFalse(output.exists())
        self.assertTrue(answers.is_file())
        self.assertIn("No partial configured agent was written", stderr.getvalue())

    def test_named_interrupt_during_configuration_removes_wrapper_candidates(self):
        print("ARMED: configure-time interrupt removes candidate and scratch sidecars")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        output = self.tmp / "interrupted-output"
        scripted = iter(["1", str(self.source), str(output), "2", str(fixture)])

        def interrupting_configure(_source, _answers, destination, _seat, **_kwargs):
            (destination.parent / f".{destination.name}.glue-scratch-planted").mkdir()
            (destination.parent / f".{destination.name}.glue-candidate-planted").mkdir()
            raise KeyboardInterrupt

        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), err=stderr, configure_fn=interrupting_configure,
        ), 130)
        self.assertFalse(output.exists())
        self.assertEqual(list(output.parent.glob(f".{output.name}.glue-*-*")), [])

    def test_named_answer_retry_fixes_in_place_without_restarting_flow(self):
        print("ARMED: named answer rejection and retry resolve the full question label")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        answers = self.tmp / "answers-with-one-error.md"
        answers.write_text(fixture.read_text().replace(
            "Answer: 12 percent.",
            "Answer: [documented] 900 percent.",
        ))
        output = self.tmp / "retry-output"
        scripted = iter(["1", str(self.source), str(output), "2", str(answers),
                         "15 percent", ""])
        prompts = []

        def ask(prompt):
            prompts.append(prompt)
            return next(scripted)

        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(ask=ask, err=stderr), 0)
        self.assertTrue(output.is_dir())
        full_question = "B4. At what percentage above estimate does an invoice get flagged for review before payment?"
        self.assertIn(f"Question to fix: {full_question}", stderr.getvalue())
        self.assertTrue(any(full_question in prompt for prompt in prompts))

    def test_named_unresolvable_question_label_falls_back_to_bare_code(self):
        print("ARMED: missing questionnaire label falls open to the raw question code")
        stderr = io.StringIO()
        setup.render_rejection(
            setup.engine.IntakeRejected([("B4", "percentage invalid")]),
            stderr,
            {},
        )
        self.assertIn("Issue: B4: percentage invalid", stderr.getvalue())
        self.assertIn("Question to fix: B4", stderr.getvalue())

    def test_named_unknown_rejection_stays_visible_with_support_language(self):
        print("ARMED: unknown rejection is shown, never swallowed")
        self._assert_renderer_case(
            "novel.future.row",
            "a future structured reason",
            "not recognized by this wrapper",
        )

    def test_named_unexpected_exception_is_clean_error_without_traceback(self):
        print("ARMED: fallback removal exposes traceback")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        output = self.tmp / "unexpected-output"
        scripted = iter(["1", str(self.source), str(output), "2", str(fixture)])
        stderr = io.StringIO()

        def explode(*_args, **_kwargs):
            raise RuntimeError("planted invariant")

        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), err=stderr, configure_fn=explode,
        ), 1)
        self.assertEqual(stderr.getvalue(), "ERROR planted invariant\n")
        self.assertNotIn("Traceback", stderr.getvalue())
        self.assertFalse(output.exists())

    def test_named_renderer_table_covers_every_code_family(self):
        table = (ROOT / "docs" / "rejection-renderer.md").read_text()
        for prefix, _question, _problem, _example in setup.REJECTION_RULES:
            with self.subTest(prefix=prefix):
                self.assertIn(prefix.rstrip("."), table)

    def _assert_renderer_case(self, row, reason, expected_question):
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        output = self.tmp / f"rejected-{re.sub('[^a-z0-9]+', '-', row.lower())}"
        scripted = iter(["1", str(self.source), str(output), "2", str(fixture), ""])
        stderr = io.StringIO()

        def reject(*_args, **_kwargs):
            raise setup.engine.IntakeRejected([(row, reason)])

        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), err=stderr, configure_fn=reject,
        ), 2)
        rendered = stderr.getvalue()
        self.assertIn(f"Issue: {row}: {reason}", rendered)
        self.assertIn(expected_question, rendered)
        self.assertNotIn("Traceback", rendered)
        self.assertFalse(output.exists())


RENDER_CASES = (
    ("mapping_config_keys", "mapping.config_keys./timezone", "bad type", "configuration question"),
    ("config_keys", "config_keys./timezone", "bad path", "configuration question"),
    ("mapping", "mapping", "bad mapping", "edition's setup mapping"),
    ("template", "template.IDENTITY.md", "unmanaged marker", "template agent directory"),
    ("protected_state", "protected_state", "copy failed", "existing agent directory"),
    ("structured_answers", "structured_answers_file", "missing", "configured-answer artifact"),
    ("sealed_core", "sealed_core.parse", "rejected", "questionnaire answer"),
    ("cross_seat", "cross_seat.pointer", "missing peer", "connected-seat question"),
    ("append_plan", "append-plan", "missing artifact", "cross-seat handoff plan"),
    ("appender", "appender.seat-config.json", "bad JSON", "appending seat"),
    ("owner", "owner.seat-config.json", "bad JSON", "owner seat"),
    ("file", "file", "not UTF-8", "completed answers file"),
    ("output", "output", "not a directory", "configured agent destination"),
    ("seat", "seat", "not installed", "setup edition"),
    (
        "question",
        "B4",
        "percentage invalid",
        "Question to fix: B4. At what percentage above estimate does an invoice get flagged for review before payment?",
    ),
    ("cover", "cover.Timezone", "missing", "Timezone"),
)


def _renderer_test(name, row, reason, expected):
    def test(self):
        print(f"ARMED: renderer family {row} remains mapped and visible")
        self._assert_renderer_case(row, reason, expected)
    test.__name__ = f"test_named_renderer_{name}"
    return test


for _name, _row, _reason, _expected in RENDER_CASES:
    setattr(
        ZeroTouchSetupTests,
        f"test_named_renderer_{_name}",
        _renderer_test(_name, _row, _reason, _expected),
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
