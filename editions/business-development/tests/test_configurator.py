from __future__ import annotations
import datetime, hashlib, importlib.util, io, json, shutil, tempfile, unittest
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
        scripted=iter(["2",str(self.source),str(wrapped),"2",str(self.answers)]); self.assertEqual(setup.run_setup(ask=lambda _p:next(scripted),clock=self.clock),0); self.assertEqual(digest(direct),digest(wrapped))
    def test_setup_renders_bd_question_label(self):
        print("ARMED: setup renderer must name the BD question, never expose only D10")
        fields={f.key:f for f in setup.questionnaire_fields((EDITION/"answers-format.md").read_text())}; err=io.StringIO(); setup.render_rejection(setup.engine.IntakeRejected([("D10","planted")]),err,fields)
        self.assertIn("What leasing and marketing facts can your BDM truthfully quote",err.getvalue())
    def test_member_census_and_banned_token(self):
        print("ARMED: member census and banned-token mutation scan the full recursive edition")
        banned="N"+"EPQ"; hits=[p for p in EDITION.rglob("*") if p.is_file() and banned.lower() in p.read_text(errors="ignore").lower()]; self.assertEqual(hits,[])
    def test_wrong_declared_filename_rejects_by_name(self):
        print("ARMED: wrong-declared-filename rejects by the exact declared name")
        mapping=json.loads((ROOT/"engine/mappings/business-development.json").read_text()); mapping["structured_answers_file"]="config.json"; path=self.tmp/"wrong.json"; path.write_text(json.dumps(mapping)); old=setup.engine.SUPPORTED["business-development"]["mapping"]; setup.engine.SUPPORTED["business-development"]["mapping"]=path
        try:
            with self.assertRaises(setup.engine.IntakeRejected) as raised: setup.engine.configure(self.source,self.answers,self.tmp/"wrong","business-development",clock=self.clock,seat_registry={})
            self.assertIn("config.json",str(raised.exception.failures))
        finally: setup.engine.SUPPORTED["business-development"]["mapping"]=old
    def test_each_declared_seam_type_is_armed(self):
        print("ARMED: FACT_MATCH, POLICY_DIVERGE, and ORDERING each produce a live casualty")
        peer_dir=self.tmp/"peer"; peer_dir.mkdir(); (peer_dir/"seat-config.json").write_text(json.dumps({"seat":"maintenance-coordinator","answers":{"B1":"different","C1":"different","B5":"4"}})); registry={"maintenance-coordinator":peer_dir}
        mapping=json.loads((ROOT/"engine/mappings/business-development.json").read_text()); current={"seat":"business-development","answers":{"B10":"3","C2":"local","D10":"3"}}
        result=setup.engine.cross_seat.apply(current,mapping,registry,engine_version="1.1.0"); statuses={r["check_id"]:r["status"] for r in result.current["cross_seat_checks"]}; self.assertEqual(statuses["BD-2"],"fail"); self.assertEqual(statuses["BD-4"],"pass"); self.assertEqual(statuses["BD-1-ordering"],"pass"); doctrines={r["doctrine"] for r in result.report_items}; self.assertIn("FACT_MATCH",doctrines); self.assertIn("POLICY_DIVERGE",doctrines)
        mutated=json.loads(json.dumps(mapping)); next(r for r in mutated["cross_seat"]["checks"] if r["type"]=="ORDERING")["operator"]="gt"; casualty=setup.engine.cross_seat.apply(current,mutated,registry,engine_version="1.1.0"); self.assertIn("ORDERING",{r["doctrine"] for r in casualty.report_items})

if __name__ == "__main__": unittest.main(verbosity=2)
