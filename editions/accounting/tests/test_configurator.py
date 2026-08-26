#!/usr/bin/env python3
import csv, datetime, hashlib, importlib.util, io, json, re, shutil, subprocess, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("pmagents_engine", ROOT / "engine" / "engine.py")
engine = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(engine)
SETUP_SPEC = importlib.util.spec_from_file_location("pmagents_setup", ROOT / "setup.py")
setup = importlib.util.module_from_spec(SETUP_SPEC); SETUP_SPEC.loader.exec_module(setup)
FIXTURE = ROOT / "editions" / "accounting" / "fixtures" / "ridgeline-accounting-answers.md"
SOURCE = ROOT / "editions" / "accounting" / "library-src"
MAPPING = ROOT / "engine" / "mappings" / "accounting.json"


def digest(root):
    return [(str(p.relative_to(root)), hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(root.rglob("*")) if p.is_file()]


class AccountingConfiguratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pmagents-accounting-"))
        self.source = SOURCE

    def tearDown(self): shutil.rmtree(self.tmp)

    def fixture_variant(self, question_id, answer):
        text = FIXTURE.read_text()
        pattern = re.compile(
            rf"(?ms)^({re.escape(question_id)}\..*?\n(?:.*?\n)*?Answer: ).*?"
            rf"(?=\n{engine.intake.QUESTION_ID_PATTERN}\.|\Z)"
        )
        changed, count = pattern.subn(rf"\g<1>{answer}\n", text, count=1)
        self.assertEqual(count, 1, f"fixture substitution drifted for {question_id}")
        path = self.tmp / f"{question_id}-variant.md"
        path.write_text(changed)
        return path

    def test_production_entry_and_declared_filename(self):
        print("ARMED: wrong declared accounting filename rejects by name")
        out = self.tmp / "out"
        engine.configure(self.source, FIXTURE, out, "accounting", seat_registry={})
        self.assertTrue((out / "accounting-config.json").is_file())
        self.assertFalse((out / "seat-config.json").exists())
        self.assertEqual(json.loads((out / "accounting-config.json").read_text())["seat"], "accounting")

    def test_create_then_reconfigure_is_byte_stable(self):
        out = self.tmp / "out"
        clock = lambda: datetime.date(2026, 8, 25)
        engine.configure(self.source, FIXTURE, out, "accounting", clock=clock, seat_registry={})
        engine.configure(out, FIXTURE, out, "accounting", clock=clock, seat_registry={})
        payload = json.loads((out / "accounting-config.json").read_text())
        self.assertEqual(payload["configuration_engine"]["configuration_date"], "2026-08-25")
        self.assertTrue((out / "GUARDRAILS.md").is_file())

    def test_declared_filename_mutation_rejects_by_name(self):
        mapping = json.loads(MAPPING.read_text())
        mapping["structured_answers_file"] = "../wrong.json"
        with self.assertRaises(engine.cross_seat.CrossSeatRejected) as caught:
            engine.cross_seat.structured_answers_filename(mapping)
        self.assertIn("structured_answers_file", str(caught.exception.failures))

    def test_named_zero_touch_wrapper_equals_direct_and_uses_accounting_labels(self):
        print("ARMED: setup renders accounting labels and wrapper bytes equal direct configure")
        wrapped, direct = self.tmp / "wrapped", self.tmp / "direct"
        seat_number = next(number for number, row in enumerate(setup.SEATS, 1)
                           if row["id"] == "accounting")
        scripted = iter([str(seat_number), str(self.source), str(wrapped), "2", str(FIXTURE)])
        stdout = io.StringIO()
        self.assertEqual(setup.run_setup(ask=lambda _p: next(scripted), out=stdout,
                                         clock=lambda: datetime.date(2026, 8, 25)), 0)
        engine.configure(self.source, FIXTURE, direct, "accounting",
                         clock=lambda: datetime.date(2026, 8, 25), seat_registry={})
        self.assertEqual(digest(wrapped), digest(direct))
        labels = setup.questionnaire_fields(FIXTURE.read_text(),
                                             engine.cover_fields_for_seat("accounting"))
        self.assertIn("D9. Where are W-9s stored, and does a current 1099 tracker exist?",
                      {row.label for row in labels})

    def test_named_content_divergent_fixture_cannot_substitute_for_accounting(self):
        print("ARMED: accounting production intake rejects a sibling fixture without writes")
        output = self.tmp / "divergent"
        sibling = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, sibling, output, "accounting",
                             clock=lambda: datetime.date(2026, 8, 25), seat_registry={})
        self.assertIn("A17", caught.exception.render())
        self.assertFalse(output.exists())

    def test_sealed_core_unchanged(self):
        self.assertEqual(hashlib.sha256(engine.SEALED_CORE.read_bytes()).hexdigest(),
                         "0540ea08aa8d47ecb1aebbb7f51db85c5a67ab252172804e9ba24e56c2403551")

    def test_named_accounting_provenance_destination_hashes_match_shipped_bytes(self):
        print("ARMED: every accounting included-product provenance row matches shipped bytes")
        with (ROOT / "provenance" / "source-files.tsv").open(newline="") as handle:
            rows = [row for row in csv.DictReader(handle, delimiter="\t")
                    if row["disposition"] == "included-product"
                    and row["destination_path"].startswith("editions/accounting/")
                    and not re.fullmatch(r"[0-9a-f]{8,40}", row["reviewed_head"])]
        self.assertEqual({row["artifact_id"] for row in rows},
                         {f"artifact-{number}" for number in range(167, 196)})
        self.assertEqual(len(rows), 29)
        for row in rows:
            destination = ROOT / row["destination_path"]
            with self.subTest(artifact_id=row["artifact_id"]):
                self.assertTrue(destination.is_file(), row["destination_path"])
                self.assertRegex(row["destination_sha256"], r"^[0-9a-f]{64}$")
                self.assertEqual(hashlib.sha256(destination.read_bytes()).hexdigest(),
                                 row["destination_sha256"])

    def test_named_accounting_readme_routes_only_through_guided_setup(self):
        print("ARMED: accounting README names guided setup and bans manual replacement")
        readme = (SOURCE / "README.md").read_text()
        self.assertIn("python3 setup.py", readme)
        self.assertIn("`accounting-config.json` is the\nsource of truth", readme)
        self.assertNotIn("Setup (manual)", readme)
        self.assertNotIn("replace the placeholders", readme.casefold())

    def test_named_accounting_onboarding_verifies_config_without_second_interview(self):
        print("ARMED: accounting first boot verifies configured custody without recollecting answers")
        onboarding = (SOURCE / "ONBOARDING.md").read_text()
        self.assertIn("Read `accounting-config.json` in full", onboarding)
        self.assertIn("Telegram bot token, chat\n"
                      "id, and allowed sender id", onboarding)
        for required in ("`BOT_TOKEN`", "`CHAT_ID`", "`ALLOWED_USER`",
                         "Validate that all three are nonblank"):
            self.assertIn(required, onboarding)
        self.assertIn("rerun\n   `python3 setup.py`", onboarding)
        for stale in ("what should my name be", "Which accounting system", "approval thresholds"):
            self.assertNotIn(stale, onboarding)

    def test_named_accounting_onboarding_skill_is_verify_only_and_skill_census_is_exact(self):
        print("ARMED: all nine accounting skills are dispositioned and onboarding never re-interviews")
        skills = SOURCE / ".claude" / "skills"
        self.assertEqual({path.parent.name for path in skills.glob("*/SKILL.md")}, {
            "ap-vendor-payments", "approvals", "ar-rent-posting", "onboarding", "owner-draws",
            "owner-statement-drafting", "security-deposit-accounting", "trust-compliance",
            "trust-reconciliation",
        })
        onboarding = (skills / "onboarding" / "SKILL.md").read_text()
        for required in ("Repository `setup.py` is the single configuration interview",
                         "read `accounting-config.json` in full",
                         "silently substitute accounting answers"):
            self.assertIn(required, onboarding)
        for banned in ("reverse-prompting interview", "ask the operator questions",
                       "write their answers into your own configuration",
                       "What should I call myself?", "What timezone are you in?"):
            self.assertNotIn(banned, onboarding)

    def test_named_accounting_skill_references_resolve_inside_shipped_tree(self):
        print("ARMED: every accounting skill reference resolves inside the shipped tree")
        skills = SOURCE / ".claude" / "skills"
        references = []
        for path in sorted(skills.glob("*/SKILL.md")):
            for name in re.findall(r"\.claude/skills/([a-z0-9-]+)/SKILL\.md",
                                   path.read_text()):
                references.append((path, name))
        self.assertTrue(references)
        missing = [
            f"{path.relative_to(SOURCE)} -> .claude/skills/{name}/SKILL.md"
            for path, name in references
            if not (skills / name / "SKILL.md").is_file()
        ]
        self.assertEqual(missing, [])

    def test_named_accounting_approval_boundary_derives_from_never_graduate_mapping(self):
        print("ARMED: accounting approval routing is mapping-derived and never PM-assist-specific")
        mapping = json.loads(MAPPING.read_text())
        approval = (SOURCE / ".claude/skills/approvals/SKILL.md").read_text()
        for row in mapping["cross_seat"]["never_graduate"]:
            with self.subTest(gate_id=row["gate_id"]):
                self.assertIn(f"`{row['gate_id']}`", approval)
                self.assertIn(row["reason"], approval)
        for stale in (
            "Property Manager's Assistant", "draft-release-gate",
            "escalation-triage", "broker-escalation",
        ):
            self.assertNotIn(stale, approval)
        self.assertIn("approval is not execution", approval)

    def test_named_accounting_completion_preserves_five_custody_properties(self):
        print("ARMED: accounting completion is gated, rollback-safe, durable, and heartbeat-last")
        onboarding = (SOURCE / "ONBOARDING.md").read_text()
        gate = onboarding.index("## First Boot Gate")
        remove_set = onboarding.index("for c in ar-digest")
        first_role = onboarding.index('add-cron "$CTX_AGENT_NAME" ar-digest')
        marker = onboarding.index('touch "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"')
        heartbeat = onboarding.index('add-cron "$CTX_AGENT_NAME" heartbeat')
        self.assertLess(gate, remove_set)
        self.assertLess(remove_set, first_role)
        self.assertLess(first_role, marker)
        self.assertLess(marker, heartbeat)
        failure = onboarding.split("  else\n", 1)[1]
        self.assertIn('rm -f "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"', failure)
        self.assertIn("for c in ar-digest bank-rec-am bank-rec-pm", failure)
        self.assertNotIn("for c in heartbeat ar-digest", failure)

    def test_named_every_accounting_onboarding_bash_block_parses(self):
        print("ARMED: every embedded accounting onboarding Bash block passes bash -n")
        blocks = re.findall(
            r"(?m)^([ \t]*)```bash\n(.*?)\n\1```$", (SOURCE / "ONBOARDING.md").read_text(), re.S
        )
        self.assertEqual(len(blocks), 1)
        for index, (_indent, block) in enumerate(blocks, 1):
            parsed = subprocess.run(["bash", "-n"], input=block, text=True,
                                    capture_output=True, check=False)
            self.assertEqual(parsed.returncode, 0,
                             f"ONBOARDING bash block {index}: {parsed.stderr}")

    def test_named_accounting_marker_blocks_crons_and_durable_completion(self):
        print("ARMED: an unfilled accounting identity marker refuses crons and .onboarded")
        agent = self.tmp / "agent"
        engine.configure(self.source, FIXTURE, agent, "accounting", seat_registry={})
        identity = agent / "IDENTITY.md"
        identity.write_text(
            '<!-- Set during onboarding: deliberately reintroduced casualty -->\n'
            + identity.read_text()
        )
        blocks = re.findall(
            r"(?m)^([ \t]*)```bash\n(.*?)\n\1```$", (agent / "ONBOARDING.md").read_text(), re.S
        )
        self.assertEqual(len(blocks), 1)
        state_root = self.tmp / "state-root"
        env = {"CTX_ROOT": str(state_root), "CTX_AGENT_NAME": "accounting"}
        result = subprocess.run(["bash"], input=blocks[0][1], text=True, cwd=agent,
                                env=env, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("still contain a rendered placeholder or the unfilled identity marker",
                      result.stdout)
        self.assertFalse((state_root / "state" / "accounting" / ".onboarded").exists())
        self.assertNotIn("cortextos: command not found", result.stderr)
        self.assertIn(
            "if grep -rlE '\\{\\{[^{}]+\\}\\}|<!-- Set during onboarding' . "
            "--include='*.md' --include='*.json' 2>/dev/null | grep -vE "
            "'ONBOARDING\\.md|README\\.md|skills/onboarding/|node_modules'; then",
            blocks[0][1],
        )

    def test_named_accounting_companion_claim_matches_shipped_reality(self):
        print("ARMED: accounting companion claim says no separate documents ship")
        claim = "No separate companion documents ship in this edition."
        self.assertIn(claim, (ROOT / "editions/accounting/answers-format.md").read_text())
        self.assertIn(claim, FIXTURE.read_text())
        for stale in ("five generic bookkeeping documents", "Bookkeeping Tracking Board in this folder"):
            self.assertNotIn(stale, (ROOT / "editions/accounting/answers-format.md").read_text())
            self.assertNotIn(stale, FIXTURE.read_text())

    def test_named_accounting_day_mode_has_no_false_local_value(self):
        print("ARMED: accounting day mode awaits the maintenance-owned config window")
        config = json.loads((SOURCE / "config.json").read_text())
        self.assertNotIn("day_mode_start", config)
        self.assertNotIn("day_mode_end", config)
        soul = (SOURCE / "SOUL.md").read_text()
        self.assertNotIn("08:00 – 17:00", soul)
        self.assertNotIn("Day Mode", soul)

    def test_named_accounting_historical_credential_blast_rejects_before_writes(self):
        print("ARMED: accounting AKIA regression rejects before config and onboarding writes")
        fixture = self.fixture_variant("B1", "$375 AKIAABCDEFGHIJKLMNOP")
        output = self.tmp / "credential-blast"
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, fixture, output, "accounting", seat_registry={})
        self.assertIn("credential-scan", caught.exception.render())
        self.assertFalse(output.exists())

    def test_named_accounting_seam_contract_is_single_authority_and_graded(self):
        print("ARMED: accounting seams preserve table authority and deferred boundaries")
        mapping = json.loads(MAPPING.read_text())
        pointers = {row["value_name"]: row for row in mapping["cross_seat"]["pointers"]}
        self.assertEqual({
            (row["value_name"], row["owner_seat"], row["owner_question_id"],
             row["holding_question_id"], row["owner_value_path"])
            for row in pointers.values()
        }, {
            ("deposit_disposition_deadline", "maintenance-coordinator", "A3", "A6", "/answers/A3"),
            ("deposit_clock_trigger", "leasing-coordinator", "B1", "A6", "/answers/B1"),
            ("licensed_trades", "maintenance-coordinator", "A7", "A15", "/answers/A7"),
            ("deposit_chargeback_threshold", "turnover-coordinator", "C7", "B13", "/answers/C7"),
            ("eviction_attorney", "pm-assist", "A4", "C5", "/answers/A4"),
            ("accounting_platform", "maintenance-coordinator", "D1", "D1", "/answers/D1"),
            ("decision_log_location", "pm-assist", "D7", "D6", "/answers/D7"),
        })
        self.assertNotIn("day_mode_window", pointers)
        deposit_config = next(
            row for row in mapping["config_keys"] if row["path"] == "/deposit_return_days"
        )
        self.assertEqual(deposit_config["source"],
                         pointers["deposit_disposition_deadline"]["holding_question_id"])
        self.assertEqual(
            (deposit_config["extractor"], deposit_config["label"],
             deposit_config["value_type"], deposit_config["minimum"]),
            ("labeled_integer", "Deposit return days", "integer", 1),
        )
        self.assertEqual({
            (row["check_id"], row["type"], row["local_ref"],
             row["peer_seat"], row["peer_ref"])
            for row in mapping["cross_seat"]["checks"]
        }, {
            ("SEAM-8", "POLICY_DIVERGE", "/answers/B1", "maintenance-coordinator", "/answers/B1"),
            ("SEAM-11", "POLICY_DIVERGE", "/answers/C1", "maintenance-coordinator", "/answers/C1"),
            ("SEAM-12", "POLICY_DIVERGE", "/answers/C4", "maintenance-coordinator", "/answers/C9"),
            ("SEAM-17", "POLICY_DIVERGE", "/answers/D8", "maintenance-coordinator", "/answers/D6"),
        })
        self.assertEqual(
            {row["gate_id"] for row in mapping["cross_seat"]["never_graduate"]},
            {"vendor_payment", "owner_draw", "deposit_disposition", "trust_reconciliation",
             "ledger_adjustment", "vendor_banking_change", "external_financial_send"},
        )

    def test_named_classroom_destination_retarget_reaches_runtime(self):
        print("ARMED: QAd semantic values reach the reviewed classroom tree")
        output = self.tmp / "classroom-retarget"
        engine.configure(self.source, FIXTURE, output, "accounting", seat_registry={})
        self.assertIn("Read `accounting-config.json` in full", (output / "AGENTS.md").read_text())
        payload = json.loads((output / "accounting-config.json").read_text())
        self.assertEqual(payload["answers"]["B1"].splitlines()[0], "$375. Below it the bookkeeper pays on a matched work order; at or above it the property")
        for path in output.rglob("*"):
            if path.is_file():
                self.assertNotRegex(path.read_text(errors="ignore"), r"\{\{(?:agent_name|company_name|operator_name|owner_name|timezone|maintenance_agent_name|leasing_agent_name)\}\}")

    def test_named_accounting_numeric_config_is_strict_positive_and_semantically_labeled(self):
        print("ARMED: every declared accounting numeric uses a positive domain and no first-number guess")
        mapping = json.loads(MAPPING.read_text())
        numeric = {row["path"]: row for row in mapping["config_keys"]
                   if row.get("value_type") == "integer"}
        self.assertEqual(set(numeric), {
            "/late_fee_grace_days", "/nonpayment_notice_days", "/deposit_return_days",
            "/nsf_fee_cap", "/file_or_hold_decision_days", "/trust_record_retention_years",
            "/contractor_license_threshold", "/decision_log_retention_years",
            "/vendor_bill_approval_threshold", "/dual_auth_threshold", "/reserve_floor",
            "/unidentified_payment_escalation_threshold", "/reconciliation_variance_threshold",
            "/variance_alert_amount", "/variance_alert_age_days", "/owner_draw_deadline_day",
            "/owner_draw_target_day", "/owner_statement_release_day",
            "/deposit_chargeback_per_line", "/deposit_chargeback_per_unit",
        })
        self.assertEqual(numeric["/vendor_bill_approval_threshold"].get("minimum"), 0)
        self.assertTrue(all(row.get("minimum") == 1 for path, row in numeric.items()
                            if path != "/vendor_bill_approval_threshold"))
        for path in ("/owner_draw_deadline_day", "/owner_draw_target_day",
                     "/owner_statement_release_day"):
            self.assertEqual(numeric[path].get("maximum"), 31)
        self.assertTrue(all(row.get("mode") == "create" for row in numeric.values()))
        self.assertNotIn("first_integer", {row["extractor"] for row in numeric.values()})
        for row in numeric.values():
            if row["extractor"] == "labeled_integer":
                self.assertTrue(row.get("label"), row["path"])

    def test_named_accounting_fixture_numbers_land_in_config(self):
        print("ARMED: accounting fixture values reach typed runtime config exactly")
        output = self.tmp / "typed-config"
        engine.configure(self.source, FIXTURE, output, "accounting", seat_registry={})
        config = json.loads((output / "config.json").read_text())
        self.assertEqual({key: config[key] for key in (
            "late_fee_grace_days", "nonpayment_notice_days", "deposit_return_days",
            "nsf_fee_cap", "file_or_hold_decision_days", "trust_record_retention_years",
            "contractor_license_threshold", "decision_log_retention_years",
            "vendor_bill_approval_threshold", "dual_auth_threshold", "reserve_floor",
            "unidentified_payment_escalation_threshold", "reconciliation_variance_threshold",
            "variance_alert_amount", "variance_alert_age_days", "owner_draw_deadline_day",
            "owner_draw_target_day", "owner_statement_release_day",
            "deposit_chargeback_per_line", "deposit_chargeback_per_unit",
        )}, {
            "late_fee_grace_days": 5, "nonpayment_notice_days": 14,
            "deposit_return_days": 30, "nsf_fee_cap": 30,
            "file_or_hold_decision_days": 3, "trust_record_retention_years": 7,
            "contractor_license_threshold": 2500, "decision_log_retention_years": 7,
            "vendor_bill_approval_threshold": 375, "dual_auth_threshold": 1500,
            "reserve_floor": 400, "unidentified_payment_escalation_threshold": 550,
            "reconciliation_variance_threshold": 40, "variance_alert_amount": 10,
            "variance_alert_age_days": 3, "owner_draw_deadline_day": 15,
            "owner_draw_target_day": 10, "owner_statement_release_day": 12,
            "deposit_chargeback_per_line": 150, "deposit_chargeback_per_unit": 400,
        })

    def test_named_accounting_reserve_floor_uses_labeled_base_not_earlier_override(self):
        print("ARMED: accounting B3 extracts the labeled base reserve, never an earlier override")
        output = self.tmp / "reserve-label"
        fixture = self.fixture_variant(
            "B3",
            "Juniper override $650.\n  Base reserve: 400\n  Northstar override $250.",
        )
        engine.configure(self.source, fixture, output, "accounting", seat_registry={})
        config = json.loads((output / "config.json").read_text())
        self.assertEqual(config["reserve_floor"], 400)

    def test_named_accounting_guided_setup_preserves_b8_labeled_multiline_values(self):
        print("ARMED: real accounting guided setup preserves both B8 labeled values")
        parsed = engine.validate(FIXTURE, "accounting")
        answers = self.tmp / "guided-accounting.md"
        output = self.tmp / "guided-accounting-output"
        responses = list(parsed.raw_cover.values()) + [
            parsed.raw_answers[q] for q in engine.SUPPORTED["accounting"]["question_ids"]
        ]
        terminated = [item for response in responses for item in (response, "")]
        seat_number = next(number for number, row in enumerate(setup.SEATS, 1)
                           if row["id"] == "accounting")
        scripted = iter([
            str(seat_number), str(self.source), str(output), "1", str(answers),
            *terminated,
        ])
        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), out=io.StringIO(),
            clock=lambda: datetime.date(2026, 8, 26),
        ), 0)
        config = json.loads((output / "config.json").read_text())
        self.assertEqual(
            (config["owner_draw_deadline_day"], config["owner_draw_target_day"]),
            (15, 10),
        )
        rendered = answers.read_text()
        self.assertIn("Answer: [documented] Owner draw deadline day: 15\n"
                      "  Owner draw target day: 10", rendered)

    def test_named_accounting_guided_fractional_currency_refuses_with_whole_dollar_fix(self):
        print("ARMED: guided fractional currency refuses with a whole-dollar correction")
        parsed = engine.validate(FIXTURE, "accounting")
        answers = self.tmp / "guided-fractional-currency.md"
        output = self.tmp / "guided-fractional-currency-output"
        responses = list(parsed.raw_cover.values()) + [
            "$30.50" if question == "B1" else parsed.raw_answers[question]
            for question in engine.SUPPORTED["accounting"]["question_ids"]
        ]
        terminated = [item for response in responses for item in (response, "")]
        seat_number = next(number for number, row in enumerate(setup.SEATS, 1)
                           if row["id"] == "accounting")
        scripted = iter([
            str(seat_number), str(self.source), str(output), "1", str(answers),
            *terminated,
            "",
        ])
        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), out=io.StringIO(), err=stderr,
            clock=lambda: datetime.date(2026, 8, 26),
        ), 2)
        self.assertIn("threshold must be stated in whole dollars", stderr.getvalue())
        self.assertFalse(output.exists())

    def test_named_accounting_onboarding_wiring_is_identical_across_surfaces(self):
        print("ARMED: accounting first boot carries the complete Telegram wiring triple")
        required = {"BOT_TOKEN", "CHAT_ID", "ALLOWED_USER"}
        for relative in ("ONBOARDING.md", ".claude/skills/onboarding/SKILL.md"):
            text = (self.source / relative).read_text()
            with self.subTest(relative=relative):
                self.assertEqual({name for name in required if f"`{name}`" in text}, required)
        skill = (self.source / ".claude/skills/onboarding/SKILL.md").read_text()
        self.assertIn("allowed sender id", skill)

    def test_named_zero_vendor_threshold_means_every_bill_requires_approval(self):
        print("ARMED: zero vendor threshold is a valid conservative approval policy")
        output = self.tmp / "zero-vendor-threshold"
        engine.configure(self.source, self.fixture_variant(
            "B1", "$0. Every vendor bill requires PM approval before payment."
        ), output, "accounting", seat_registry={})
        self.assertEqual(json.loads((output / "config.json").read_text())[
            "vendor_bill_approval_threshold"], 0)

    def test_named_calendar_day_fields_reject_day_32_before_activation(self):
        print("ARMED: impossible day-of-month values reject before accounting writes")
        for question_id, answer in (
            ("B8", "Owner draw deadline day: 32\n  Owner draw target day: 10"),
            ("B8", "Owner draw deadline day: 15\n  Owner draw target day: 32"),
            ("B10", "Owner statement release day: 32"),
        ):
            with self.subTest(question_id=question_id, answer=answer):
                output = self.tmp / ("day-32-" + hashlib.sha256(answer.encode()).hexdigest()[:8])
                with self.assertRaises(engine.IntakeRejected) as caught:
                    engine.configure(self.source, self.fixture_variant(question_id, answer), output,
                                     "accounting", seat_registry={})
                self.assertIn("maximum", caught.exception.render())
                self.assertFalse(output.exists())

    def test_named_accounting_multiple_jurisdiction_clocks_reject_loudly(self):
        print("ARMED: multi-jurisdiction clocks reject instead of flattening to one value")
        answers = (
            "Late fee grace days: 5\n  Late fee grace days: 10\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia late fee grace days: 10\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Late fee grace days for Georgia: 10\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Late fee grace days (Georgia): 10\n  Counsel confirmed both jurisdictions.",
            "Pine Basin County: 5 days\n  Cedar Mesa County: 7 days\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 1 day\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 calendar days\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Riverside Parish: 10 business days\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 calendar days.\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days,\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 calendar days;\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 business days:\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days!\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 1 day?\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days)\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days]\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days}\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days\"\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days'\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days”\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days’\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days…\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia: 10 days..\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia - 10 days\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia – 10 calendar days.\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Georgia — 10 business days)\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Late fee grace days: 10.\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Late fee grace days: 10)\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Late fee grace days: 10..\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Late fee grace days: 10!\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Late fee grace days: 10?\n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5\n  Late fee grace days: 10   \n  Counsel confirmed both jurisdictions.",
            "Late fee grace days: 5!\n  Late fee grace days: 10?\n  Counsel confirmed both jurisdictions.",
        )
        for index, answer in enumerate(answers, 1):
            with self.subTest(answer=answer):
                output = self.tmp / f"multiple-jurisdiction-clocks-{index}"
                fixture = self.fixture_variant("A1", answer)
                with self.assertRaises(engine.IntakeRejected) as caught:
                    engine.configure(self.source, fixture, output, "accounting", seat_registry={})
                self.assertIn("A1 accepts exactly one structured day-count line",
                              caught.exception.render())
                self.assertIn("tracked per-jurisdiction capability", caught.exception.render())
                self.assertNotIn("task_", caught.exception.render())
                self.assertFalse(output.exists())

    def test_named_accounting_structured_duration_aside_refuses_with_honest_a1_contract(self):
        print("ARMED: unrelated structured duration refuses with the honest A1 contract")
        output = self.tmp / "structured-duration-aside"
        fixture = self.fixture_variant(
            "A1",
            "Late fee grace days: 6\n  Payment window: 30 days\n"
            "  Counsel confirmed the one supported clock.",
        )
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, fixture, output, "accounting", seat_registry={})
        message = caught.exception.render()
        self.assertIn("A1 accepts exactly one structured day-count line", message)
        self.assertIn("Additional label: N day(s) lines", message)
        self.assertIn("calendar/business qualifiers", message)
        self.assertIn("state other timing details as plain prose", message)
        self.assertNotIn("multiple jurisdiction grace clocks", message)
        self.assertFalse(output.exists())
        hint = (ROOT / "editions" / "accounting" / "answers-format.md").read_text()
        self.assertIn("A1 accepts exactly one structured day-count line", hint)
        self.assertIn("every other timing detail as plain prose", hint)
        self.assertIn("Label: N calendar days", hint)
        self.assertIn("Label: N business days", hint)

    def test_named_accounting_single_jurisdiction_clock_configures_exactly(self):
        print("ARMED: one counsel-confirmed grace clock with explanatory prose configures exactly")
        output = self.tmp / "single-jurisdiction-clock"
        engine.configure(self.source, self.fixture_variant(
            "A1", "Late fee grace days: 6\n  Counsel confirms this 6-day grace for the supported jurisdiction."
        ), output, "accounting", seat_registry={})
        self.assertEqual(json.loads((output / "config.json").read_text())[
            "late_fee_grace_days"], 6)

    def test_named_accounting_prose_form_jurisdiction_clock_rejects_loudly(self):
        print("ARMED: prose-form jurisdiction grace clock cannot silently flatten")
        for index, conflict in enumerate((
            "Georgia late fee grace period is 10 days.",
            "For Georgia, the late fee grace period is 10 calendar days.",
            "10 days late fee grace for Georgia.",
            "Late fee grace period is 10 days in Georgia.",
        ), 1):
            with self.subTest(conflict=conflict):
                output = self.tmp / f"prose-form-jurisdiction-clock-{index}"
                fixture = self.fixture_variant(
                    "A1",
                    "Late fee grace days: 5\n"
                    f"  {conflict}\n"
                    "  Counsel confirmed both jurisdictions.",
                )
                with self.assertRaises(engine.IntakeRejected) as caught:
                    engine.configure(self.source, fixture, output, "accounting",
                                     seat_registry={})
                self.assertIn("A1 accepts exactly one structured day-count line",
                              caught.exception.render())
                self.assertFalse(output.exists())

    def test_named_accounting_clock_union_arms_each_exclusive_branch_and_extended_jurisdictions(self):
        print("ARMED: phrase and jurisdiction-vocabulary clock branches each close exclusive gaps")
        conflicts = (
            "Georgia grace period is 10 days.",  # closed-vocabulary branch only
            "Riverside late fee grace period is 10 days.",  # phrase branch only
            "DC grace period is 10 days.",
            "Puerto Rico grace period is 10 calendar days.",
            "Guam grace period is 10 business days.",
        )
        for index, conflict in enumerate(conflicts, 1):
            with self.subTest(conflict=conflict):
                output = self.tmp / f"clock-union-exclusive-{index}"
                with self.assertRaises(engine.IntakeRejected) as caught:
                    engine.configure(self.source, self.fixture_variant(
                        "A1", f"Late fee grace days: 5\n  {conflict}"
                    ), output, "accounting", seat_registry={})
                self.assertIn("A1 accepts exactly one structured day-count line",
                              caught.exception.render())
                self.assertFalse(output.exists())

    def test_named_accounting_clock_union_requires_every_closed_vocabulary_leg(self):
        print("ARMED: closed-vocabulary clock branch requires jurisdiction, grace, and days")
        benign_lines = (
            "Georgia requires a 10-day filing deadline.",
            "Counsel confirms this 5-day grace period.",
            "Counsel reviews the separate payment window within 30 business days.",
        )
        for index, benign in enumerate(benign_lines, 1):
            with self.subTest(benign=benign):
                output = self.tmp / f"clock-union-missing-leg-{index}"
                engine.configure(self.source, self.fixture_variant(
                    "A1", f"Late fee grace days: 6\n  {benign}"
                ), output, "accounting", seat_registry={})
                self.assertEqual(json.loads((output / "config.json").read_text())[
                    "late_fee_grace_days"], 6)

    def test_named_accounting_single_punctuated_clock_preserves_raw_then_refuses_extraction(self):
        print("ARMED: punctuated canonical passes guard without rewriting raw extraction bytes")
        answer = "Late fee grace days: 6.\n  Counsel confirmed the one supported clock."
        fixture = self.fixture_variant("A1", answer)
        parsed = engine.validate(fixture, "accounting")
        parsed_answer = "Late fee grace days: 6.\nCounsel confirmed the one supported clock."
        self.assertEqual(parsed.raw_answers["A1"], parsed_answer)
        self.assertEqual(parsed.answers["A1"], parsed_answer)
        output = self.tmp / "single-punctuated-clock"
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, fixture, output, "accounting", seat_registry={})
        self.assertIn("labeled integer line 'Late fee grace days': NN not found",
                      caught.exception.render())
        self.assertFalse(output.exists())

    def test_named_accounting_punctuated_prose_survives_persisted_artifact_exactly(self):
        print("ARMED: persisted accounting answers retain operator punctuation byte-for-byte")
        answer = (
            "Late fee grace days: 6\n"
            "  Counsel confirmed this rule (Georgia)."
        )
        expected = "Late fee grace days: 6\nCounsel confirmed this rule (Georgia)."
        output = self.tmp / "punctuated-prose-persistence"
        engine.configure(self.source, self.fixture_variant("A1", answer), output,
                         "accounting", seat_registry={})
        persisted = json.loads((output / "accounting-config.json").read_text())
        self.assertEqual(persisted["answers"]["A1"], expected)

    def test_named_accounting_unstructured_qualified_duration_prose_configures_exactly(self):
        print("ARMED: qualified duration prose without labeled clock shape remains valid")
        output = self.tmp / "qualified-duration-prose"
        engine.configure(self.source, self.fixture_variant(
            "A1", "Late fee grace days: 6\n"
            "  Counsel reviews the separate payment window within 30 business days."
        ), output, "accounting", seat_registry={})
        self.assertEqual(json.loads((output / "config.json").read_text())[
            "late_fee_grace_days"], 6)

    def test_named_accounting_labeled_duration_with_trailing_words_remains_prose(self):
        print("ARMED: letters after a labeled duration keep the line outside the clock grammar")
        output = self.tmp / "labeled-duration-trailing-prose"
        engine.configure(self.source, self.fixture_variant(
            "A1", "Late fee grace days: 6\n"
            "  Payment: 10 days later we bill."
        ), output, "accounting", seat_registry={})
        self.assertEqual(json.loads((output / "config.json").read_text())[
            "late_fee_grace_days"], 6)

    def test_named_accounting_deferred_money_value_rejects_before_activation(self):
        print("ARMED: unresolved accounting money sentinel names B1 and writes nothing")
        output = self.tmp / "deferred-money"
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, self.fixture_variant("B1", "[NEEDS-CONFIRM]"), output,
                             "accounting", seat_registry={})
        rendered = caught.exception.render()
        self.assertIn("B1", rendered)
        self.assertIn("human confirmation is required", rendered)
        self.assertFalse(output.exists())


if __name__ == "__main__": unittest.main()
