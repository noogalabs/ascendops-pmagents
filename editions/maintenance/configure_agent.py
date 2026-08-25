#!/usr/bin/env python3
"""Betty maintenance configurator: always creates a credential-safe sandbox copy."""
import argparse, copy, datetime, json, os, re, shutil, sys, tempfile
from pathlib import Path

BEGIN = "<!-- BETTY-CONFIG-BEGIN -->"
END = "<!-- BETTY-CONFIG-END -->"
PRECEDENCE = ("This section was generated from your setup questionnaire on {date} and is this agent's current company configuration. "
              "If anything elsewhere in this file or in an older document disagrees with it, this section governs. "
              "To change a value, update the questionnaire answer and re-run the configuration; do not edit this block by hand.")
QUESTION_IDS = [*(f"A{i}" for i in range(1,9)), *(f"B{i}" for i in range(1,13)), *(f"C{i}" for i in range(1,10)), *(f"D{i}" for i in range(1,10))]
LIBRARY = ["occupied-unit-maintenance-workflow.md", "occupied-unit-maintenance-board.md", "coordinator-scope-playbook.md", "invoice-review-example.md", "maintenance-coordinator-judgment-guide.md", "maintenance-auto-send-message-library.md"]
TELEGRAM_PLACEHOLDER_ALLOWLIST = {b"1234567890:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
SECRET_PATTERNS = [("OpenAI key", re.compile(rb"(?<![A-Za-z0-9_])sk-[A-Za-z0-9_-]{8,}")), ("GitHub token", re.compile(rb"ghp_[A-Za-z0-9]{8,}")), ("AWS key", re.compile(rb"AKIA[A-Z0-9]{12,}")), ("Slack token", re.compile(rb"xox[a-z]-[A-Za-z0-9-]{8,}")), ("Telegram bot token", re.compile(rb"(?P<value>\d{8,10}:[A-Za-z0-9_-]{35})")), ("private key", re.compile(rb"PRIVATE KEY"))]

def fail(stage, message): raise RuntimeError(f"{stage}: {message}")
def excluded(path):
    parts = path.parts
    name = path.name.lower()
    explicit_secret_files={".cortextos-env",".mcp.json","settings.json"}
    return any(p in {".state", "state", "memory"} for p in parts) or path.name == ".env" or path.name.startswith(".env.") or name in explicit_secret_files or "token" in name or "credential" in name
def copy_safe(source, target):
    if not source.is_dir(): fail("copy", f"source-agent-dir missing: {source}")
    skipped=[]
    def ignore(directory,names):
        result=[]
        for name in names:
            p=Path(directory,name)
            if excluded(p) or p.is_symlink(): result.append(name); skipped.append(str(p.relative_to(source)))
        return result
    shutil.copytree(source, target, ignore=ignore, symlinks=False)
    (target/"copy-exclusions.json").write_text(json.dumps({"policy":"secret/state paths and every symlink are skipped; symlink targets are never followed","paths":sorted(set(skipped))},indent=2)+"\n")
def credential_scan(root):
    for path in root.rglob("*"):
        if path.is_file():
            try: data=path.read_bytes()
            except OSError as e: fail("credential-scan",f"cannot scan {path.relative_to(root)}: {e}")
            for label, pattern in SECRET_PATTERNS:
                for match in pattern.finditer(data):
                    if label == "Telegram bot token":
                        if match.group("value") in TELEGRAM_PLACEHOLDER_ALLOWLIST: continue
                        line=data.count(b"\n",0,match.start())+1
                        fail("credential-scan",f"{label} found in {path.relative_to(root)}:{line}; documented placeholders require human confirmation before their exact value is added to TELEGRAM_PLACEHOLDER_ALLOWLIST")
                    fail("credential-scan", f"{label} found in {path.relative_to(root)}")

def provenance_value(raw, field):
    match=re.match(r"^\s*\[([^\]]+)\]\s*(.*)$",raw,re.S)
    if not match: return raw
    tag,value=match.group(1),match.group(2)
    if tag in {"documented","inferred"}: return value
    if tag=="NEEDS-DAVID": return raw
    fail("parse",f"unknown provenance tag on {field}: {raw!r}; human confirmation is required before this value can be used")

def parse_answers(path, preserve_raw=False):
    text=path.read_text(encoding="utf-8")
    cover={}; raw_cover={}
    for label,key in [("Company name","company_name"),("Org short-name","org_short_name"),("Forward email","forward_email"),("Timezone","timezone")]:
        matches=re.findall(rf"^{re.escape(label)}:\s*(.*)$", text, re.M)
        if len(matches)!=1: fail("parse",f"cover label {label} must appear exactly once")
        raw=matches[0].strip(); cover[key]=provenance_value(raw,key); raw_cover[key]=raw
    answers={}; raw_answers={}; counts={}; current=None
    for line in text.splitlines():
        q=re.match(r"^([A-D]\d+)\.\s", line)
        if q: current=q.group(1)
        elif current and line.startswith("Answer:"):
            counts[current]=counts.get(current,0)+1
            if counts[current]>1: fail("parse",f"duplicate Answer line for {current}")
            raw_answers[current]=line.partition(":")[2].strip()
        elif current and line.startswith("  ") and current in raw_answers: raw_answers[current]+="\n"+line[2:]
    missing=[q for q in QUESTION_IDS if q not in raw_answers]
    if missing: fail("parse", "missing answers: "+", ".join(missing))
    for question,raw in raw_answers.items(): answers[question]=provenance_value(raw,question)
    return (cover,answers,raw_cover,raw_answers) if preserve_raw else (cover,answers)

def times(answer):
    spans=re.findall(r"(\d{1,2}:\d{2})\s*(?:[-–]|to)\s*(\d{1,2}:\d{2})",answer,re.I)
    if not spans: fail("merge", "B8 lacks HH:MM-HH:MM communications window")
    return spans[-1]
def d9_crons(answer):
    m=re.fullmatch(r"\s*Friday\s+(\d{2}):(\d{2})\s+destination:\s*(.+?)\s*;\s*Monday\s+(\d{2}):(\d{2})\s+destination:\s*(.+?)\s*",answer,re.I)
    if not m: fail("merge","D9 confirmed format must be: Friday HH:MM destination: <destination>; Monday HH:MM destination: <destination>")
    fh,fm,mh,mm=map(int,(m.group(1),m.group(2),m.group(4),m.group(5)))
    if fh>23 or mh>23 or fm>59 or mm>59: fail("merge","D9 time is outside 00:00-23:59")
    friday,monday=m.group(3).strip().removesuffix("."),m.group(6).strip().removesuffix(".")
    return [{"name":"weekly-open-ticket-summary","type":"recurring","cron":f"{fm} {fh} * * 5","prompt":f"Compile the weekly open-ticket summary and deliver to {friday}."},{"name":"weekly-kpi-snapshot","type":"recurring","cron":f"{mm} {mh} * * 1","prompt":f"Compile the weekly maintenance KPI snapshot and deliver to {monday}."}]
def owned_merge(before, answers, cover, raw_answers=None):
    raw_answers=raw_answers or answers
    after=copy.deepcopy(before); skips=[]; expected_appends=[]
    after["timezone"]=cover["timezone"]
    if "NEEDS-DAVID" in raw_answers["B8"]: skips.append({"answer":"B8","destination":"config day-mode keys","reason":"answer value unconfirmed (NEEDS-DAVID)","message":"B8: config day-mode keys NOT written - answer value unconfirmed (NEEDS-DAVID); lands on confirmation."})
    else:
        start,end=times(answers["B8"]); after["day_mode_start"],after["day_mode_end"]=start,end
    confirmed=[]
    for q,label in (("B5","SLAs"),("B10","Escalations/closeout"),("D6","Alert channels")):
        if "NEEDS-DAVID" in raw_answers[q]: skips.append({"answer":q,"destination":"heartbeat prompt","reason":"answer value unconfirmed (NEEDS-DAVID)","message":f"{q}: heartbeat prompt NOT updated - answer value unconfirmed (NEEDS-DAVID); lands on confirmation."})
        else: confirmed.append(f"{label}: {answers[q]}")
    suffix=(" BETTY CONFIG: "+" ".join(confirmed)) if confirmed else ""
    for cron in after.get("crons",[]):
        if cron.get("name")=="heartbeat": cron["prompt"]=re.sub(r"\s*BETTY CONFIG:.*$","",cron.get("prompt",""))+suffix
    if "NEEDS-DAVID" in raw_answers["D9"]: skips.append({"answer":"D9","destination":"weekly report crons","reason":"answer value unconfirmed (NEEDS-DAVID)","message":"D9: config crons NOT created - answer value unconfirmed (NEEDS-DAVID); lands on confirmation."})
    else:
        approved=d9_crons(answers["D9"]); existing={c.get("name"):c for c in after.get("crons",[])}
        for cron in approved:
            if cron["name"] in existing:
                if existing[cron["name"]]!=cron: fail("merge",f"conflicting preexisting generated cron: {cron['name']}")
            else: after.setdefault("crons",[]).append(cron); expected_appends.append(cron)
    return after,skips,expected_appends
def paths(obj,p=""):
    out={}
    if isinstance(obj,dict):
        for k,v in obj.items(): out.update(paths(v,f"{p}.{k}" if p else k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): out.update(paths(v,f"{p}[{i}]"))
    else: out[p]=obj
    return out
def census(before,after,skips=None,expected_appends=None):
    skips=skips or []; expected_appends=expected_appends or []
    b,a=paths(before),paths(after); owned={"day_mode_start","day_mode_end","timezone"}
    changes=[]
    for k in sorted(set(b)|set(a)):
        if b.get(k)!=a.get(k):
            cm=re.fullmatch(r"crons\[(\d+)\]\.(.+)",k)
            allowed=k in owned
            if cm:
                idx=int(cm.group(1))
                if idx<len(before.get("crons",[])) and idx<len(after.get("crons",[])): allowed=cm.group(2)=="prompt" and before["crons"][idx].get("name")==after["crons"][idx].get("name")=="heartbeat"
                elif idx>=len(before.get("crons",[])): allowed=after["crons"][idx] in expected_appends
            if not allowed: fail("key-census", f"unowned key changed: {k}")
            changes.append({"key":k,"before":b.get(k),"after":a.get(k),"owned":True})
    return {"before_keys":sorted(b),"after_keys":sorted(a),"changes":changes,"owned_skips":skips,"unowned_keys_byte_identical":True}

def assert_generated_config_tag_free(after, report):
    flattened=paths(after)
    for change in report["changes"]:
        value=flattened.get(change["key"])
        if isinstance(value,str) and re.search(r"\[[^\]]+\]",value):
            fail("merge",f"generated executable value contains a provenance marker: {change['key']}")

def bool_flag(text,name): return bool(re.search(rf"{name}\s*=\s*true",text,re.I))
def generated(cover,a,kind):
    certified=bool_flag(a["A4"],"CERTIFIED-MAIL-CONFIRMED")
    lease=bool_flag(a["B3"],"LEASE-CLAUSE-CONFIRMED")
    silence=bool_flag(a["B6"],"SILENCE-CLAUSE-CONFIRMED")
    lines=[BEGIN,PRECEDENCE.format(date=datetime.date.today().isoformat()),""]
    if kind=="guardrails":
      lines += ["Your seat library lives at library/; the index skill routes you.","",f"## {cover['company_name']} maintenance rules",f"- Property-class urgency: {a['A1']}",f"- Entry notice rules: {a['A2']}",f"- Deposit disposition: {a['A3']}",f"- Certified-mail gate: configured={str(certified).lower()}; disabled class text: high-consequence certified-mail delivery cannot be used unless confirmed.",f"- Damage dispute and lease sections: {a['A5']} / {a['A6']}",f"- Always-vendor licensed trades: {a['A7']}",f"- Habitability triggers: {a['A8']}",f"- Owner pre-approval and overrides: {a['B1']}",f"- After-hours emergency spend cap: {a['B2']}",f"- Priority SLAs: {a['B5']}",f"- External communications window: {a['B8']}",f"- Resident-responsibility gate: configured={str(lease).lower()}; disabled class text: resident-responsibility messages cannot fire unless the lease clause is confirmed.",f"- Proceed-on-silence gate: configured={str(silence).lower()}; disabled class text: proceed-on-silence messages cannot fire unless the signed-agreement clause is confirmed.",f"- Callback, warranty, and self-repair windows: {a['B7']} / {a['B12']}",f"- Region-first routing: {a['C4']}",f"- NEVER-DISPATCH exclusions: {a['C8']}",f"- Resident/owner channels and sender identity: {a['D3']} / {a['D5']}",f"- Warranty and secure access routing: {a['D7']} / {a['D8']}"]
    else:
      lines += [f"## {cover['company_name']} maintenance seat identity",f"- Company identity: org={cover['org_short_name']}; forward-email={cover['forward_email']}; timezone={cover['timezone']}",f"- Portfolio and property classes: {a['A1']}",f"- On-call coverage: {a['B9']}",f"- Decision makers: {a['C1']} / on-call {a['C2']} / backup {a['C9']}",f"- In-house technicians: {a['C3']}",f"- Vendor roster: {a['C5']}",f"- After-hours intake and invoice handoff: {a['C6']} / {a['C7']}",f"- Platform operating context and quirks: {a['D1']} / {a['D2']}"]
    lines += [END]
    return "\n".join(lines)+"\n"
def inject(path,block):
    old=path.read_text(encoding="utf-8")
    if BEGIN in old or END in old:
        if old.count(BEGIN)!=1 or old.count(END)!=1 or old.index(BEGIN)>old.index(END): fail("inject",f"malformed markers in {path.name}")
        old=old[:old.index(BEGIN)].rstrip()+"\n\n"+block+old[old.index(END)+len(END):].lstrip("\n")
    else: old=old.rstrip()+"\n\n"+block
    path.write_text(old,encoding="utf-8")
def seat(cover,a):
    flags={"certified_mail_confirmed":bool_flag(a["A4"],"CERTIFIED-MAIL-CONFIRMED"),"lease_clause_confirmed":bool_flag(a["B3"],"LEASE-CLAUSE-CONFIRMED"),"silence_clause_confirmed":bool_flag(a["B6"],"SILENCE-CLAUSE-CONFIRMED")}
    phase_zero=[]
    if re.search(r"\bno (?:approved )?roster\b",a["C5"],re.I): phase_zero.append("approved-vendor-roster")
    if re.search(r"\b(?:no|none|missing|does not exist)\b",a["D7"],re.I): phase_zero.append("warranty-records")
    if not a["C9"].strip(): phase_zero.append("backup-decision-maker")
    exclusions=[a["C8"]] if a["C8"].strip() else []
    return {"seat":"maintenance-coordinator","company":cover,"answers":a,"derived":{"thresholds":{"owner_preapproval":a["B1"],"emergency_spend":a["B2"],"tenant_responsibility":a["B3"],"invoice_variance":a["B4"]},"slas":{"priority":a["B5"],"escalation":a["B10"]},"windows":{"external_comms":a["B8"],"on_call":a["B9"]},"people":{"manager":a["C1"],"on_call":a["C2"],"backup":a["C9"]},"roster":{"technicians":a["C3"],"vendors":a["C5"],"regions":a["C4"]},"channels":{"resident":a["D3"],"resources":a["D4"],"owner":a["D5"],"escalation":a["D6"]},"gates":{"confirmed_flags":flags,"runtime_enforcement_claimed":False,"production_requirement":"armed disabled-class-cannot-fire test"},"exclusions":exclusions,"phase_zero":phase_zero},"provenance":{"questionnaire_version":"2026-08-21","filled_by":cover.get("company_name",""),"date":str(datetime.date.today())}}
def load_library(root,libsrc):
    missing=[n for n in LIBRARY if not (libsrc/n).is_file()]
    if missing: fail("library-load", "required docs missing: "+", ".join(missing))
    dest=root/"library"
    if dest.exists(): shutil.rmtree(dest)
    dest.mkdir()
    for n in LIBRARY: shutil.copy2(libsrc/n,dest/n)
    skill=root/".claude/skills/seat-library/SKILL.md"; skill.parent.mkdir(parents=True,exist_ok=True)
    skill.write_text("# Maintenance seat library\n\nRead the relevant guide before deciding or drafting. Company configuration in the Betty block and seat-config.json governs conflicts.\n\n| Trigger | Read |\n|---|---|\n| Intake, triage, dispatch, closeout | `library/occupied-unit-maintenance-workflow.md` |\n| Board fields, stages, clocks | `library/occupied-unit-maintenance-board.md` |\n| In-house vs vendor, boundaries | `library/coordinator-scope-playbook.md` and `library/maintenance-coordinator-judgment-guide.md` |\n| Invoice review | `library/invoice-review-example.md` |\n| Resident, owner, vendor messages | `library/maintenance-auto-send-message-library.md` |\n",encoding="utf-8")
def contradictions(root,a,key_report):
    old_values=[(c["key"],str(c["before"])) for c in key_report["changes"] if c.get("before") not in (None,"")]
    hits=[]
    for p in root.rglob("*"):
        if p.is_file() and p.name not in {"contradiction-report.md","seat-config.json","key-census.json","copy-exclusions.json"} and "library" not in p.parts and "seat-library" not in p.parts:
            try: lines=p.read_text(errors="ignore").splitlines()
            except OSError: continue
            for i,line in enumerate(lines,1):
                if BEGIN in line: break
                for key,value in old_values:
                    if value in line: hits.append(f"- `{p.relative_to(root)}:{i}` — before value for `{key}` (`{value}`): {line[:140]}")
    overlaps=[]
    organic_paths=[p for p in root.rglob("*.md") if "library" not in p.parts and "seat-library" not in p.parts and p.name!="contradiction-report.md"]
    organic="\n".join(p.read_text(errors="ignore") for p in organic_paths).lower()
    for p in (root/"library").glob("*.md"):
        terms=[x.lower() for x in re.findall(r"^#{1,3}\s+(.+)$",p.read_text(errors="ignore"),re.M)]
        if any(t in organic for t in terms if len(t)>10): overlaps.append(f"- `{p.relative_to(root)}` shares headings/topics with organic root prose; review, never auto-resolved.")
    d9_skipped=any(s.get("answer")=="D9" for s in key_report.get("owned_skips",[]))
    gap=("- D9 contains NEEDS-DAVID. Its destination remains non-executable in `seat-config.json`; no report cron was added." if d9_skipped else "- None.")
    return "# Contradiction review list\n\nGenerated values govern; these possible overlaps are listed, never resolved automatically.\n\n## Mapping gaps and named skips\n"+gap+"\n\n## Superseded-value candidates\n"+("\n".join(hits) if hits else "- None found.")+"\n\n## Library vs organic overlaps\n"+("\n".join(overlaps) if overlaps else "- None detected by heading comparison.")+"\n"
def run(source,answers,out,libsrc):
    if out.exists(): fail("copy",f"output already exists: {out}")
    if out==source or source in out.parents: fail("copy-boundary","output_dir must not equal or be nested inside source-agent-dir")
    cover,a,raw_cover,raw_answers=parse_answers(answers,preserve_raw=True); parent=out.parent; parent.mkdir(parents=True,exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix=f".{out.name}.betty-",dir=parent))
    try:
        work=tmp/"agent"; copy_safe(source,work); credential_scan(work)
        cfg=work/"config.json"
        if not cfg.is_file(): fail("merge","source config.json missing")
        before=json.loads(cfg.read_text()); after,skips,appends=owned_merge(before,a,cover,raw_answers); report=census(before,after,skips,appends); assert_generated_config_tag_free(after,report)
        for skip in skips: print(f"merge: named skip {skip['message']}")
        cfg.write_text(json.dumps(after,indent=2)+"\n"); (work/"key-census.json").write_text(json.dumps(report,indent=2)+"\n")
        targets=[work/"GUARDRAILS.md",work/"IDENTITY.md",work/"SOUL.md"]
        if not (work/"GUARDRAILS.md").is_file() or not (work/"IDENTITY.md").is_file(): fail("inject","required GUARDRAILS.md or IDENTITY.md missing")
        for p in targets:
            if p.is_file(): inject(p,generated(cover,a,"guardrails" if p.name=="GUARDRAILS.md" else "identity"))
            else: print(f"inject: named skip: optional {p.name} missing",file=sys.stderr)
        (work/"seat-config.json").write_text(json.dumps(seat(raw_cover,raw_answers),indent=2)+"\n")
        load_library(work,libsrc); (work/"contradiction-report.md").write_text(contradictions(work,a,report))
        credential_scan(work); os.replace(work,out); tmp.rmdir()
    except Exception:
        shutil.rmtree(tmp,ignore_errors=True); raise
def main():
    p=argparse.ArgumentParser(); p.add_argument("source_agent_dir",type=Path); p.add_argument("answers_file",type=Path); p.add_argument("output_dir",type=Path); p.add_argument("--library-source",type=Path,default=Path(__file__).with_name("library-src")); ns=p.parse_args()
    try: run(*(x.resolve() for x in (ns.source_agent_dir,ns.answers_file,ns.output_dir,ns.library_source)))
    except Exception as e: print(f"ERROR {e}",file=sys.stderr); return 1
    print(ns.output_dir); return 0
if __name__=="__main__": raise SystemExit(main())
