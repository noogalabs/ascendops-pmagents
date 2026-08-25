#!/usr/bin/env python3
import hashlib, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TOOL=ROOT/"configure_agent.py"; FIX=ROOT/"fixtures/ridgeline-maintenance-answers.md"
TELEGRAM_REALISH="AbCdEfGhIjKlMnOpQrStUvWxYz012345678"
TELEGRAM_PLACEHOLDER="1234567890:AA"+("x"*33)
TELEGRAM_MUTATED_PLACEHOLDER=TELEGRAM_PLACEHOLDER[:-1]+"y"
assert len(TELEGRAM_REALISH)==35 and len(TELEGRAM_PLACEHOLDER)==len(TELEGRAM_MUTATED_PLACEHOLDER)==46
def digest(root):
    return [(str(p.relative_to(root)),hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(root.rglob("*")) if p.is_file()]
def tag_answer(text, question, tag):
    lines=text.splitlines(); current=None
    for index,line in enumerate(lines):
        match=__import__("re").match(r"^([A-D]\d+)\.\s",line)
        if match: current=match.group(1)
        elif current==question and line.startswith("Answer:"):
            lines[index]="Answer: "+tag+" "+line.partition(":")[2].strip(); return "\n".join(lines)+"\n"
    raise AssertionError(f"answer not found: {question}")
class ConfiguratorTests(unittest.TestCase):
 def setUp(self):
  self.t=Path(tempfile.mkdtemp()); self.src=self.t/"source"; self.src.mkdir()
  import re
  confirmed=re.sub(r"(^D9\..*?^Answer:)[^\n]*",r"\1 Friday 16:30 destination: Maintenance Supervisor; Monday 09:00 destination: Leadership Team",FIX.read_text(),count=1,flags=re.M|re.S)
  self.answers=self.t/"confirmed-answers.md"; self.answers.write_text(confirmed)
  (self.src/"config.json").write_text(json.dumps({"timezone":"America/New_York","day_mode_start":"07:30","day_mode_end":"20:30","untouched":{"x":1},"crons":[{"name":"heartbeat","prompt":"Read heartbeat"}]},indent=2)+"\n")
  for n in ("GUARDRAILS.md","IDENTITY.md","SOUL.md"): (self.src/n).write_text("# Organic\nOld threshold 999 and vendor rules.\n")
 def tearDown(self): shutil.rmtree(self.t)
 def execute(self,out="out",lib=None):
  cmd=[sys.executable,str(TOOL),str(self.src),str(self.answers),str(self.t/out)]
  if lib: cmd += ["--library-source",str(lib)]
  return subprocess.run(cmd,text=True,capture_output=True)
 def test_golden_and_library_six_docs_index(self):
  skill=self.src/".claude/skills/organic/SKILL.md"; skill.parent.mkdir(parents=True); skill.write_text("# Maintenance Coordinator Judgment Guide (Generic Baseline)\nOld day start 07:30.\n")
  r=self.execute(); self.assertEqual(r.returncode,0,r.stderr); out=self.t/"out"
  self.assertEqual(len(list((out/"library").glob("*.md"))),6); self.assertTrue((out/".claude/skills/seat-library/SKILL.md").is_file())
  self.assertIn("Your seat library lives at library/",(out/"GUARDRAILS.md").read_text())
  self.assertNotIn("Your seat library lives at library/",(out/"IDENTITY.md").read_text())
  self.assertIn("NEVER-DISPATCH",(out/"GUARDRAILS.md").read_text()); self.assertNotIn("NEVER-DISPATCH",(out/"IDENTITY.md").read_text())
  self.assertIn("In-house technicians",(out/"IDENTITY.md").read_text()); self.assertNotIn("In-house technicians",(out/"GUARDRAILS.md").read_text())
  guard=(out/"GUARDRAILS.md").read_text(); identity=(out/"IDENTITY.md").read_text()
  for required in ("Owner pre-approval and overrides", "Priority SLAs", "External communications window"): self.assertIn(required,guard)
  for required in ("org=ridgeline", "maintenance@ridgeline.example", "America/Denver", "WorkTrail"): self.assertIn(required,identity)
  cfg=json.loads((out/"config.json").read_text()); self.assertEqual((cfg["day_mode_start"],cfg["day_mode_end"]),("08:00","20:00")); self.assertEqual(cfg["timezone"],"America/Denver")
  self.assertIn("SLAs:",cfg["crons"][0]["prompt"]); self.assertEqual(len(cfg["crons"]),3)
  sys.path.insert(0,str(ROOT)); import configure_agent as c
  seat=json.loads((out/"seat-config.json").read_text()); self.assertEqual(set(seat["answers"]),set(c.QUESTION_IDS))
  contradiction=(out/"contradiction-report.md").read_text(); self.assertIn(".claude/skills/organic/SKILL.md",contradiction); self.assertIn("before value for `day_mode_start`",contradiction)
  self.assertEqual([c["name"] for c in cfg["crons"][1:]],["weekly-open-ticket-summary","weekly-kpi-snapshot"])
 def test_idempotency_and_hand_edit_dies(self):
  self.assertEqual(self.execute().returncode,0); out=self.t/"out"; guard=out/"GUARDRAILS.md"
  guard.write_text(guard.read_text().replace("Owner pre-approval","HAND EDIT Owner pre-approval")); self.assertIn("HAND EDIT",guard.read_text()); first_config=(out/"config.json").read_bytes()
  shutil.rmtree(self.src); shutil.copytree(out,self.src); shutil.rmtree(out)
  self.assertEqual(self.execute().returncode,0); self.assertNotIn("HAND EDIT",guard.read_text()); self.assertEqual(first_config,(out/"config.json").read_bytes())
  d1=digest(out); shutil.rmtree(self.src); shutil.copytree(out,self.src); shutil.rmtree(out); self.assertEqual(self.execute().returncode,0); self.assertEqual(d1,digest(out))
 def test_planted_token_fails_shut_no_partial_copy(self):
  (self.src/"safe.txt").write_text("BOT_TOKEN=12345678:"+TELEGRAM_REALISH)
  r=self.execute(); self.assertNotEqual(r.returncode,0); self.assertIn("Telegram bot token",r.stderr); self.assertFalse((self.t/"out").exists())
 def assert_telegram_shape_dies(self,text):
  (self.src/"ordinary-notes.txt").write_text(text)
  r=self.execute(); self.assertNotEqual(r.returncode,0); self.assertIn("Telegram bot token",r.stderr); self.assertFalse((self.t/"out").exists())
 def test_telegram_token_indented_assignment_dies(self):
  self.assert_telegram_shape_dies("    BOT_TOKEN=12345678:"+TELEGRAM_REALISH+"\n")
 def test_telegram_token_json_value_dies(self):
  self.assert_telegram_shape_dies('{"BOT_TOKEN":"12345678:'+TELEGRAM_REALISH+'"}\n')
 def test_telegram_exact_blue_documentation_placeholder_stays_clean(self):
  (self.src/"agent-management.md").write_text('5. Copy the token (format: `'+TELEGRAM_PLACEHOLDER+'`)\n')
  r=self.execute(); self.assertEqual(r.returncode,0,r.stderr)
 def test_telegram_one_character_mutated_placeholder_dies_with_location(self):
  (self.src/"agent-management.md").write_text('5. Copy the token (format: `'+TELEGRAM_MUTATED_PLACEHOLDER+'`)\n')
  r=self.execute(); self.assertNotEqual(r.returncode,0); self.assertIn("agent-management.md:1",r.stderr); self.assertIn("human confirmation",r.stderr); self.assertFalse((self.t/"out").exists())
 def assert_openai_shape_dies(self,text):
  (self.src/"unsafe.txt").write_text(text)
  r=self.execute(); self.assertNotEqual(r.returncode,0); self.assertIn("OpenAI key",r.stderr); self.assertFalse((self.t/"out").exists())
 def test_openai_key_negative_ask_back_stays_clean(self):
  (self.src/"safe.txt").write_text("The ask-back-only rule is ordinary prose.\n")
  r=self.execute(); self.assertEqual(r.returncode,0,r.stderr)
 def test_openai_key_env_assignment_dies(self):
  self.assert_openai_shape_dies("OPENAI_API_KEY=sk-plantedsecretvalue\n")
 def test_openai_key_json_value_dies(self):
  self.assert_openai_shape_dies('{"api_key": "sk-plantedsecretvalue"}\n')
 def test_openai_key_bare_line_start_dies(self):
  self.assert_openai_shape_dies("sk-plantedsecretvalue\n")
 def test_openai_key_quoted_shell_dies(self):
  self.assert_openai_shape_dies('KEY="sk-plantedsecretvalue"\n')
 def test_drop_doc_mutation_dies(self):
  lib=self.t/"lib"; shutil.copytree(ROOT/"library-src",lib); (lib/"invoice-review-example.md").unlink()
  r=self.execute(lib=lib); self.assertNotEqual(r.returncode,0); self.assertIn("library-load",r.stderr); self.assertFalse((self.t/"out").exists())
 def test_unowned_key_mutation_dies(self):
  sys.path.insert(0,str(ROOT)); import configure_agent as c
  before={"day_mode_start":"1","day_mode_end":"2","crons":[{"name":"other","cron":"0 1 * * *","prompt":"x"}]}; after=json.loads(json.dumps(before)); after["crons"][0]["cron"]="0 2 * * *"
  with self.assertRaisesRegex(RuntimeError,"unowned key changed"): c.census(before,after)
 def test_parser_empty_present_and_multiline(self):
  sys.path.insert(0,str(ROOT)); import configure_agent as c
  import re
  text=FIX.read_text(); text=re.sub(r"Answer: 186 residential doors.*", "Answer:\n  continuation value",text,count=1); p=self.t/"answers.md"; p.write_text(text)
  _,answers=c.parse_answers(p); self.assertEqual(answers["A1"],"\ncontinuation value")
  answers["C8"]=""; self.assertEqual(c.seat({"company_name":"x"},answers)["derived"]["exclusions"],[])
 def test_source_symlink_skipped_not_followed(self):
  (self.src/"escape").symlink_to("/private/tmp")
  r=self.execute(); self.assertEqual(r.returncode,0,r.stderr); self.assertFalse((self.t/"out/escape").exists())
  self.assertIn("escape",json.loads((self.t/"out/copy-exclusions.json").read_text())["paths"])
 def test_copy_boundary_rejects_output_inside_source(self):
  cmd=[sys.executable,str(TOOL),str(self.src),str(self.answers),str(self.src/"nested")]; r=subprocess.run(cmd,text=True,capture_output=True)
  self.assertNotEqual(r.returncode,0); self.assertIn("copy-boundary",r.stderr)
 def test_parser_rejects_duplicate_answer_and_missing_cover(self):
  sys.path.insert(0,str(ROOT)); import configure_agent as c
  p=self.t/"bad.md"; p.write_text(FIX.read_text().replace("Company name:","Missing company:",1))
  with self.assertRaisesRegex(RuntimeError,"cover label"): c.parse_answers(p)
  p.write_text(FIX.read_text().replace("Answer: 186 residential doors","Answer: one\nAnswer: 186 residential doors",1))
  with self.assertRaisesRegex(RuntimeError,"duplicate Answer"): c.parse_answers(p)
 def test_no_network_static(self):
  text=TOOL.read_text().lower(); forbidden=["import socket","import urllib","import http","requests","fetch(","curl "]
  self.assertEqual([x for x in forbidden if x in text],[])
 def test_needs_david_k_destinations_are_named_skips(self):
  text=FIX.read_text().replace("Timezone: America/Denver","Timezone: [documented] America/Denver")
  for q in ("B5","B10","D6","D9"): text=tag_answer(text,q,"[NEEDS-DAVID]")
  held=self.t/"needs-owner-confirmation.md"; held.write_text(text)
  cmd=[sys.executable,str(TOOL),str(self.src),str(held),str(self.t/"held")]
  r=subprocess.run(cmd,text=True,capture_output=True); self.assertEqual(r.returncode,0,r.stderr)
  for q in ("B5","B10","D6","D9"): self.assertIn(f"named skip {q}",r.stdout)
  self.assertIn("D9: config crons NOT created - answer value unconfirmed (NEEDS-DAVID); lands on confirmation.",r.stdout)
  cfg=json.loads((self.t/"held/config.json").read_text()); self.assertEqual(cfg["timezone"],"America/Denver"); self.assertEqual(cfg["crons"],[{"name":"heartbeat","prompt":"Read heartbeat"}])
  seat=json.loads((self.t/"held/seat-config.json").read_text()); self.assertEqual(seat["company"]["timezone"],"[documented] America/Denver"); self.assertIn("[NEEDS-DAVID]",seat["answers"]["D9"])
  census=json.loads((self.t/"held/key-census.json").read_text()); self.assertEqual([s["answer"] for s in census["owned_skips"]],["B5","B10","D6","D9"])
 def test_documented_and_inferred_tags_strip_from_every_executable_destination(self):
  text=self.answers.read_text().replace("Timezone: America/Denver","Timezone: [documented] America/Denver")
  for q,tag in (("B8","[inferred]"),("B5","[documented]"),("B10","[inferred]"),("D6","[documented]"),("D9","[inferred]")): text=tag_answer(text,q,tag)
  self.answers.write_text(text); r=self.execute(); self.assertEqual(r.returncode,0,r.stderr)
  cfg=json.loads((self.t/"out/config.json").read_text()); flattened=[]
  def strings(value):
   if isinstance(value,dict):
    for child in value.values(): yield from strings(child)
   elif isinstance(value,list):
    for child in value: yield from strings(child)
   elif isinstance(value,str): yield value
  flattened=list(strings(cfg)); self.assertFalse(any(__import__("re").search(r"\[[^\]]+\]",value) for value in flattened))
  self.assertEqual(cfg["timezone"],"America/Denver"); self.assertEqual((cfg["day_mode_start"],cfg["day_mode_end"]),("08:00","20:00")); self.assertIn("SLAs:",cfg["crons"][0]["prompt"]); self.assertEqual(len(cfg["crons"]),3)
  seat=json.loads((self.t/"out/seat-config.json").read_text()); self.assertEqual(seat["company"]["timezone"],"[documented] America/Denver"); self.assertTrue(seat["answers"]["B5"].startswith("[documented]")); self.assertTrue(seat["answers"]["D9"].startswith("[inferred]"))
 def test_unknown_provenance_tag_fails_shut_with_question_and_value(self):
  self.answers.write_text(tag_answer(self.answers.read_text(),"D9","[future-tag]")); r=self.execute()
  self.assertNotEqual(r.returncode,0); self.assertIn("unknown provenance tag on D9",r.stderr); self.assertIn("future-tag",r.stderr); self.assertIn("human confirmation",r.stderr); self.assertFalse((self.t/"out").exists())
 def test_generated_config_marker_checker_rejects_planted_owned_value(self):
  sys.path.insert(0,str(ROOT)); import configure_agent as c
  after={"timezone":"[documented] America/New_York"}; report={"changes":[{"key":"timezone","before":"America/New_York","after":after["timezone"],"owned":True}]}
  with self.assertRaisesRegex(RuntimeError,r"generated executable value contains a provenance marker: timezone"): c.assert_generated_config_tag_free(after,report)
 def test_confirmed_d9_exact_crons_and_existing_untouched(self):
  before=json.loads((self.src/"config.json").read_text()); r=self.execute(); self.assertEqual(r.returncode,0,r.stderr)
  after=json.loads((self.t/"out/config.json").read_text()); self.assertEqual(after["crons"][0]["name"],before["crons"][0]["name"])
  self.assertEqual(after["crons"][1],{"name":"weekly-open-ticket-summary","type":"recurring","cron":"30 16 * * 5","prompt":"Compile the weekly open-ticket summary and deliver to Maintenance Supervisor."})
  self.assertEqual(after["crons"][2],{"name":"weekly-kpi-snapshot","type":"recurring","cron":"0 9 * * 1","prompt":"Compile the weekly maintenance KPI snapshot and deliver to Leadership Team."})
 def test_ridgeline_fixture_crons_use_cover_timezone_and_clean_punctuation(self):
  cmd=[sys.executable,str(TOOL),str(self.src),str(FIX),str(self.t/"ridge")]; r=subprocess.run(cmd,text=True,capture_output=True); self.assertEqual(r.returncode,0,r.stderr)
  cfg=json.loads((self.t/"ridge/config.json").read_text()); self.assertEqual(cfg["timezone"],"America/Denver")
  self.assertEqual(cfg["crons"][-2]["cron"],"0 16 * * 5"); self.assertEqual(cfg["crons"][-1]["cron"],"0 9 * * 1")
  self.assertEqual(cfg["crons"][-1]["prompt"],"Compile the weekly maintenance KPI snapshot and deliver to Executive Operations inbox.")
 def test_confirmed_d9_missing_time_and_conflict_fail(self):
  bad=self.answers.read_text().replace("Friday 16:30","Friday afternoon"); self.answers.write_text(bad); r=self.execute(); self.assertNotEqual(r.returncode,0); self.assertIn("D9 confirmed format",r.stderr)
  self.answers.write_text(bad.replace("Friday afternoon","Friday 16:30")); cfg=json.loads((self.src/"config.json").read_text()); cfg["crons"].append({"name":"weekly-open-ticket-summary","type":"recurring","cron":"0 1 * * 5","prompt":"conflict"}); (self.src/"config.json").write_text(json.dumps(cfg))
  r=self.execute(); self.assertNotEqual(r.returncode,0); self.assertIn("conflicting preexisting generated cron",r.stderr)
if __name__=="__main__":
 print("ARMED: Contract 2 copier, parser, merge census, marker injection, library load, and credential-failure casualties",flush=True)
 unittest.main(verbosity=2)
