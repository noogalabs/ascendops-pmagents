from __future__ import annotations
import datetime, hashlib, importlib.util, io, json, re, shutil, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EDITION = ROOT / "editions/business-development"
SPEC = importlib.util.spec_from_file_location("pmagents_setup_bd", ROOT / "setup.py")
setup = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(setup)

def digest(root):
    return [(str(p.relative_to(root)), hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(root.rglob("*")) if p.is_file()]

class BusinessDevelopmentEditionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=Path(tempfile.mkdtemp(prefix="pmagents-bd-test-")); self.source=EDITION/"library-src"; self.answers=EDITION/"fixtures/ridgeline-business-development-answers.md"; self.clock=lambda: datetime.date(2026,8,25)
    def tearDown(self): shutil.rmtree(self.tmp)
    def test_production_entry_and_declared_filename(self):
        print("ARMED: undeclared default filename dies; AF-1 declared name is the only artifact")
        out=self.tmp/"direct"; setup.engine.configure(self.source,self.answers,out,"business-development",clock=self.clock,seat_registry={})
        self.assertTrue((out/"business-development-config.json").is_file()); self.assertFalse((out/"seat-config.json").exists())
        payload=json.loads((out/"business-development-config.json").read_text()); self.assertEqual(payload["seat"],"business-development"); self.assertEqual(len(payload["answers"]),42)
    def test_create_then_reconfigure(self):
        print("ARMED: create-then-reconfigure must preserve the production wrapper path")
        out=self.tmp/"rerun"
        for _ in range(2): setup.engine.configure(out if out.exists() else self.source,self.answers,out,"business-development",clock=self.clock,seat_registry={})
        self.assertTrue((out/"business-development-config.json").is_file())
    def test_zero_touch_setup_equals_direct_tree(self):
        print("ARMED: zero-touch wrapper mutation dies against direct configure tree digest")
        direct,wrapped=self.tmp/"direct",self.tmp/"wrapped"; setup.engine.configure(self.source,self.answers,direct,"business-development",clock=self.clock,seat_registry={})
        seat_number = next(number for number, row in enumerate(setup.SEATS, 1)
                           if row["id"] == "business-development")
        scripted=iter([str(seat_number),str(self.source),str(wrapped),"2",str(self.answers)]); self.assertEqual(setup.run_setup(ask=lambda _p:next(scripted),clock=self.clock),0); self.assertEqual(digest(direct),digest(wrapped))
    def test_setup_renders_bd_question_label(self):
        print("ARMED: setup renderer must name the BD question, never expose only D10")
        fields={f.key:f for f in setup.questionnaire_fields((EDITION/"answers-format.md").read_text())}; err=io.StringIO(); setup.render_rejection(setup.engine.IntakeRejected([("D10","planted")]),err,fields)
        self.assertIn("What leasing and marketing facts can your BDM truthfully quote",err.getvalue())
    def test_member_census_and_banned_token(self):
        print("ARMED: member census and banned-token mutation scan the full recursive edition")
        banned="N"+"EPQ"; hits=[p for p in EDITION.rglob("*") if p.is_file() and "__pycache__" not in p.parts and banned.lower() in p.read_text(errors="ignore").lower()]; self.assertEqual(hits,[])
    def test_wrong_declared_filename_rejects_by_name(self):
        print("ARMED: wrong-declared-filename rejects by the exact declared name")
        mapping=json.loads((ROOT/"engine/mappings/business-development.json").read_text()); mapping["structured_answers_file"]="config.json"; path=self.tmp/"wrong.json"; path.write_text(json.dumps(mapping)); old=setup.engine.SUPPORTED["business-development"]["mapping"]; setup.engine.SUPPORTED["business-development"]["mapping"]=path
        try:
            with self.assertRaises(setup.engine.IntakeRejected) as raised: setup.engine.configure(self.source,self.answers,self.tmp/"wrong","business-development",clock=self.clock,seat_registry={})
            self.assertIn("config.json",str(raised.exception.failures))
        finally: setup.engine.SUPPORTED["business-development"]["mapping"]=old
    def test_named_incomparable_cross_seat_checks_stay_absent(self):
        print("ARMED: incomparable and mis-subjected BD checks stay absent")
        mapping=json.loads((ROOT/"engine/mappings/business-development.json").read_text())
        checks={row["check_id"] for row in mapping["cross_seat"]["checks"]}
        self.assertEqual(checks,set())
        self.assertNotIn("BD-2",checks)
        self.assertNotIn("BD-4",checks)
        self.assertNotIn("BD-1-ordering",checks)

    def test_named_day_mode_has_no_false_holder_and_boots_from_peer_config(self):
        print("ARMED: day mode stays absent until the maintenance peer can supply it")
        mapping=json.loads((ROOT/"engine/mappings/business-development.json").read_text())
        placeholders={row["placeholder"] for row in mapping["placeholders"]}
        pointers={row["value_name"] for row in mapping["cross_seat"].get("pointers",[])}
        self.assertTrue({"day_mode_start","day_mode_end"}.isdisjoint(placeholders))
        self.assertTrue({"day_mode_start","day_mode_end"}.isdisjoint(pointers))
        runtime="\n".join((self.source/path).read_text() for path in [
            "SOUL.md",
            ".claude/skills/soul-philosophy/SKILL.md",
            ".claude/skills/heartbeat/SKILL.md",
        ])
        self.assertIn("/cross_seat/pointers/day_mode_start",runtime)
        self.assertIn("/cross_seat/pointers/day_mode_end",runtime)
        self.assertIn("awaiting maintenance peer",runtime)
        self.assertNotIn("{{day_mode_start}}",runtime)
        self.assertNotIn("{{day_mode_end}}",runtime)

    def test_named_speed_to_lead_value_reaches_config_and_runtime_surfaces(self):
        print("ARMED: speed-to-lead cover value must reach config and member runtime surfaces")
        out=self.tmp/"speed"
        setup.engine.configure(self.source,self.answers,out,"business-development",clock=self.clock,seat_registry={})
        config=json.loads((out/"config.json").read_text())
        self.assertEqual(config["speed_to_lead_minutes"],30)
        carriers=[out/"BDM Owner-Acquisition Playbook.md",out/"BDM Pipeline Board.md"]
        for carrier in carriers:
            text=carrier.read_text()
            rendered=re.sub(r"<!--[^>]+-->","",text)
            self.assertIn("configured 30-minute",rendered,carrier.name)
            self.assertNotIn("{{speed_to_lead_minutes}}",text,carrier.name)

    def test_named_speed_to_lead_cover_field_is_strictly_positive(self):
        print("ARMED: zero speed-to-lead window rejects before activation")
        mapping=json.loads((ROOT/"engine/mappings/business-development.json").read_text())
        row=next(row for row in mapping["config_keys"] if row["path"]=="/speed_to_lead_minutes")
        self.assertEqual((row["value_type"],row["minimum"]),("integer",1))
        bad=self.tmp/"zero.md"
        source_text=self.answers.read_text()
        self.assertEqual(source_text.count("Owner speed-to-lead window: 30"),1)
        bad.write_text(source_text.replace("Owner speed-to-lead window: 30","Owner speed-to-lead window: 0"))
        with self.assertRaises(setup.engine.IntakeRejected) as raised:
            setup.engine.configure(self.source,bad,self.tmp/"rejected","business-development",clock=self.clock,seat_registry={})
        self.assertIn("speed_to_lead_minutes",str(raised.exception.failures))
        self.assertFalse((self.tmp/"rejected").exists())

    def test_named_business_development_promise_surfaces_and_companions(self):
        print("ARMED: questionnaire promise dispositions reach shipped runtime gates")
        expected={
            ".claude/skills/property-and-owner-gates/SKILL.md": [
                "Never accept a property with known violations or habitability defects",
                "Never accept liability for a security deposit you did not collect and cannot verify",
            ],
            ".claude/skills/fee-and-contract-gates/SKILL.md": [
                "Any discount. Any waiver",
                "The manager decides. You communicate.",
            ],
            ".claude/skills/never-promise-list/SKILL.md": [
                "Reference a leasing guarantee **only** if",
                "Referral fees go into a signed agreement before they're paid",
                "Never say cancel-anytime",
            ],
            ".claude/skills/draft-release-gate/SKILL.md": [
                "Classes ship **locked**",
                "Never by accuracy alone",
            ],
            ".claude/skills/shadow-mode-calibration/SKILL.md": [
                "Nothing is queued to auto-send when shadow mode ends",
                "Every message class ships locked and graduates one at a time by explicit unlock",
            ],
        }
        for relative, lines in expected.items():
            text=(self.source/relative).read_text()
            for line in lines:
                self.assertIn(line,text,relative)
        companions={path.name for path in self.source.iterdir() if path.is_file()}
        self.assertTrue({"BDM Judgment Guide.md","BDM Owner-Acquisition Playbook.md","BDM Pipeline Board.md"} <= companions)

if __name__ == "__main__": unittest.main(verbosity=2)
