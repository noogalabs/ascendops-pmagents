#!/usr/bin/env python3
"""Generic make-ready pipeline day-count, critical-path, and certification engine."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TURN_TARGET_DAYS = 10

Task = Dict[str, object]


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_date(value: object) -> Optional[dt.date]:
    text = str(value or "").strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return dt.datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def parse_int(value: object, default: int = 0) -> int:
    try:
        return int(str(value or "").strip() or default)
    except (TypeError, ValueError):
        return default


def parse_bool(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


# ---------------------------------------------------------------------------
# Dependency-ordered topological sort (Kahn's algorithm)
# ---------------------------------------------------------------------------

def topo_sort(tasks: List[Task]) -> List[Task]:
    """Return tasks in valid dependency order (raises ValueError on cycle)."""
    normalized: List[Task] = []
    for task in tasks:
        canonical = dict(task)
        canonical["id"] = str(task.get("id") or "").strip()
        canonical["depends_on"] = [
            str(dependency).strip()
            for dependency in (task.get("depends_on") or [])
        ]
        normalized.append(canonical)

    ids = [str(task["id"]) for task in normalized]
    empty = [index for index, tid in enumerate(ids) if not tid]
    if empty:
        raise ValueError(f"Task IDs must be nonempty; missing at rows {empty}")
    duplicates = sorted({tid for tid in ids if ids.count(tid) > 1})
    if duplicates:
        raise ValueError(f"Duplicate task IDs: {', '.join(duplicates)}")
    declared = set(ids)
    dangling = sorted({
        str(dep).strip()
        for task in normalized for dep in (task.get("depends_on") or [])
        if not str(dep).strip() or str(dep).strip() not in declared
    })
    if dangling:
        raise ValueError(f"Undeclared dependency task IDs: {', '.join(repr(item) for item in dangling)}")

    by_id: Dict[str, Task] = dict(zip(ids, normalized))
    in_degree: Dict[str, int] = {tid: 0 for tid in ids}
    adj: Dict[str, List[str]] = {tid: [] for tid in ids}

    for task in normalized:
        for dep in task.get("depends_on") or []:
            dep_str = str(dep)
            adj[dep_str].append(str(task["id"]))
            in_degree[str(task["id"])] += 1

    queue = [tid for tid, deg in in_degree.items() if deg == 0]
    ordered: List[Task] = []
    while queue:
        queue.sort()  # deterministic output
        tid = queue.pop(0)
        ordered.append(by_id[tid])
        for neighbor in adj[tid]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(ordered) != len(normalized):
        raise ValueError("Cycle detected in task dependencies — check your depends_on fields.")
    return ordered


# ---------------------------------------------------------------------------
# Day-count scheduling
# ---------------------------------------------------------------------------

def schedule_tasks(
    ordered: List[Task],
    possession_date: dt.date,
) -> List[Dict[str, object]]:
    """Assign start/end dates to each task based on dependency ordering."""
    earliest_start: Dict[str, dt.date] = {}

    scheduled: List[Dict[str, object]] = []
    for task in ordered:
        tid = str(task["id"])
        duration_days = parse_int(task.get("duration_days"), 1)

        # Start = max(possession_date, max finish of all dependencies)
        start = possession_date
        for dep in task.get("depends_on") or []:
            dep_str = str(dep)
            dep_end = earliest_start.get(dep_str + "_end")
            if dep_end is not None and dep_end > start:
                start = dep_end

        end = start + dt.timedelta(days=duration_days)
        earliest_start[tid] = start
        earliest_start[tid + "_end"] = end

        scheduled.append({
            "id": tid,
            "name": task.get("name", ""),
            "trade": task.get("trade", ""),
            "stage": task.get("stage", ""),
            "stage_entered_date": str(task.get("stage_entered_date") or ""),
            "last_progress_date": str(task.get("last_progress_date") or ""),
            "is_rekey": parse_bool(task.get("is_rekey")),
            "is_critical_path": False,
            "is_dry_cure_block": parse_bool(task.get("is_dry_cure_block")),
            "must_fix": parse_bool(task.get("must_fix")),
            "verified_done": parse_bool(task.get("verified_done")),
            "evidence": str(task.get("evidence") or ""),
            "duration_days": duration_days,
            "depends_on": list(task.get("depends_on") or []),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "wear_vs_damage": str(task.get("wear_vs_damage") or "normal_wear"),
            "classification": str(task.get("classification") or "must_fix"),
        })

    return scheduled


# ---------------------------------------------------------------------------
# Critical-path analysis
# ---------------------------------------------------------------------------

def find_critical_path(scheduled: List[Dict[str, object]]) -> Tuple[List[str], dt.date]:
    """Return zero-slack task IDs and project finish via a real backward pass."""
    if not scheduled:
        return [], dt.date.today()
    by_id = {str(task["id"]): task for task in scheduled}
    starts = {tid: parse_date(task["start_date"]) for tid, task in by_id.items()}
    ends = {tid: parse_date(task["end_date"]) for tid, task in by_id.items()}
    if any(value is None for value in [*starts.values(), *ends.values()]):
        raise ValueError("Scheduled task dates must be valid before critical-path analysis")
    project_finish = max(ends.values())
    dependents: Dict[str, List[str]] = {tid: [] for tid in by_id}
    for tid, task in by_id.items():
        for dependency in task.get("depends_on") or []:
            dependents[str(dependency)].append(tid)

    latest_start: Dict[str, dt.date] = {}
    for task in reversed(scheduled):
        tid = str(task["id"])
        duration = dt.timedelta(days=parse_int(task.get("duration_days"), 1))
        latest_finish = (
            min(latest_start[child] for child in dependents[tid])
            if dependents[tid] else project_finish
        )
        latest_start[tid] = latest_finish - duration

    cp_ids = [tid for tid in by_id if starts[tid] == latest_start[tid]]

    # Mark in scheduled
    for s in scheduled:
        s["is_critical_path"] = s["id"] in cp_ids

    return cp_ids, project_finish


# ---------------------------------------------------------------------------
# Certify gate
# ---------------------------------------------------------------------------

def certify_gate(scheduled: List[Dict[str, object]]) -> Tuple[bool, List[str]]:
    """
    Returns (CERTIFIABLE, open_items).
    CERTIFIABLE: all must_fix verified_done + at least one is_rekey verified_done.
    """
    open_items: List[str] = []

    must_fixes = [s for s in scheduled if s["must_fix"]]
    rekeyed = [s for s in scheduled if s["is_rekey"]]

    for s in must_fixes:
        if not s["verified_done"]:
            open_items.append(f"UNVERIFIED must-fix: {s['name']} (trade: {s['trade']})")
        elif not str(s.get("evidence") or "").strip():
            open_items.append(f"MISSING EVIDENCE must-fix: {s['name']} (id: {s['id']})")

    if not rekeyed:
        open_items.append("MISSING: re-key task not found in punch list — re-key is mandatory")
    else:
        for r in rekeyed:
            if not r["verified_done"]:
                open_items.append(f"UNVERIFIED re-key: {r['name']}")
            elif not str(r.get("evidence") or "").strip():
                open_items.append(f"MISSING EVIDENCE re-key: {r['name']} (id: {r['id']})")
            for required in scheduled:
                if required["id"] == r["id"] or required.get("is_rekey"):
                    continue
                required_end = parse_date(required["end_date"])
                rekey_start = parse_date(r["start_date"])
                if required_end and rekey_start and required_end > rekey_start:
                    open_items.append(
                        f"RE-KEY NOT LAST: {r['name']} starts {r['start_date']} before "
                        f"required task {required['name']} ends {required['end_date']}"
                    )

    return len(open_items) == 0, open_items


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

def demo_tasks() -> Tuple[List[Task], dt.date]:
    """
    Two synthetic units: one CERTIFIABLE, one UNVERIFIED/AT_RISK.
    No real property names, addresses, or resident data.
    """
    possession_date = dt.date(2026, 7, 1)

    # Unit A: smooth turn — all must-fix verified, re-key last and verified
    unit_a: List[Task] = [
        {"id": "A1", "name": "Trash-out", "trade": "labor", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 1, "depends_on": [], "verified_done": True, "evidence": "photo-A1.jpg", "is_rekey": False, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
        {"id": "A2", "name": "Drywall repair (hole, hallway)", "trade": "handyman", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 1, "depends_on": ["A1"], "verified_done": True, "evidence": "photo-A2.jpg", "is_rekey": False, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "tenant_damage"},
        {"id": "A3", "name": "Paint — full unit", "trade": "paint", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 2, "depends_on": ["A2"], "verified_done": True, "evidence": "photo-A3.jpg", "is_rekey": False, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
        {"id": "A3d", "name": "Paint dry time", "trade": "none", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": False, "duration_days": 1, "depends_on": ["A3"], "verified_done": True, "evidence": "", "is_rekey": False, "is_dry_cure_block": True, "classification": "cosmetic", "wear_vs_damage": "normal_wear"},
        {"id": "A4", "name": "LVP flooring — living + bedrooms", "trade": "flooring", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 2, "depends_on": ["A3d"], "verified_done": True, "evidence": "photo-A4.jpg", "is_rekey": False, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
        {"id": "A5", "name": "Deep clean", "trade": "cleaning", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 1, "depends_on": ["A4"], "verified_done": True, "evidence": "photo-A5.jpg", "is_rekey": False, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
        {"id": "A6", "name": "Re-key all entry locks", "trade": "locksmith", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 1, "depends_on": ["A5"], "verified_done": True, "evidence": "photo-A6.jpg", "is_rekey": True, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
    ]

    # Unit B: at-risk turn — one must-fix unverified, re-key not yet done
    unit_b: List[Task] = [
        {"id": "B1", "name": "Trash-out", "trade": "labor", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 1, "depends_on": [], "verified_done": True, "evidence": "photo-B1.jpg", "is_rekey": False, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
        {"id": "B2", "name": "HVAC filter + coil clean (AC not cooling)", "trade": "hvac", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 1, "depends_on": ["B1"], "verified_done": False, "evidence": "", "is_rekey": False, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
        {"id": "B3", "name": "Paint — touch-up", "trade": "paint", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": False, "duration_days": 1, "depends_on": ["B2"], "verified_done": True, "evidence": "photo-B3.jpg", "is_rekey": False, "is_dry_cure_block": False, "classification": "cosmetic", "wear_vs_damage": "normal_wear"},
        {"id": "B4", "name": "Deep clean", "trade": "cleaning", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 1, "depends_on": ["B3"], "verified_done": True, "evidence": "photo-B4.jpg", "is_rekey": False, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
        {"id": "B5", "name": "Re-key all entry locks", "trade": "locksmith", "stage": "3", "stage_entered_date": "2026-07-01", "must_fix": True, "duration_days": 1, "depends_on": ["B4"], "verified_done": False, "evidence": "", "is_rekey": True, "is_dry_cure_block": False, "classification": "must_fix", "wear_vs_damage": "normal_wear"},
    ]

    return [
        {"unit": "Unit-A (synthetic)", "tasks": unit_a},
        {"unit": "Unit-B (synthetic)", "tasks": unit_b},
    ], possession_date


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def analyze_turn(
    tasks: List[Task],
    possession_date: dt.date,
    target_days: int,
    stale_stage_alert_days: int,
    unit_label: str = "unit",
    as_of_date: Optional[dt.date] = None,
) -> Dict[str, object]:
    if stale_stage_alert_days < 1:
        raise ValueError("stale_stage_alert_days must be at least 1")
    ordered = topo_sort(tasks)
    scheduled = schedule_tasks(ordered, possession_date)
    cp_ids, ready_date = find_critical_path(scheduled)
    certifiable, open_items = certify_gate(scheduled)

    target_date = possession_date + dt.timedelta(days=target_days)
    day_count = (ready_date - possession_date).days
    on_track = ready_date <= target_date
    slack_or_gap = (target_date - ready_date).days  # positive = slack, negative = gap

    stale_flags = []
    today = as_of_date or dt.date.today()
    for s in scheduled:
        stage_num = str(s.get("stage", ""))
        if not s["verified_done"] and s["must_fix"]:
            stage_entered = parse_date(s.get("stage_entered_date"))
            if stage_entered is None:
                raise ValueError(f"Task {s['id']} ({s['name']}) is missing stage_entered_date")
            last_progress = parse_date(s.get("last_progress_date"))
            if stage_entered > today:
                raise ValueError(
                    f"Task {s['id']} ({s['name']}) has future stage_entered_date "
                    f"{stage_entered.isoformat()}"
                )
            if last_progress is not None and last_progress > today:
                raise ValueError(
                    f"Task {s['id']} ({s['name']}) has future last_progress_date "
                    f"{last_progress.isoformat()}"
                )
            if last_progress is not None and last_progress < stage_entered:
                raise ValueError(
                    f"Task {s['id']} ({s['name']}) has last_progress_date "
                    f"{last_progress.isoformat()} before stage_entered_date "
                    f"{stage_entered.isoformat()}"
                )
            anchor = last_progress or stage_entered
            age = (today - anchor).days
            if age >= stale_stage_alert_days:
                state = "last progress" if last_progress else "no progress recorded; stage entry"
                stale_flags.append(
                    f"Stage {stage_num} task '{s['name']}' stale: {state} {anchor.isoformat()} "
                    f"is {age} days old (configured threshold {stale_stage_alert_days})"
                )

    return {
        "unit": unit_label,
        "possession_date": possession_date.isoformat(),
        "target_date": target_date.isoformat(),
        "ready_date": ready_date.isoformat(),
        "day_count": day_count,
        "target_days": target_days,
        "stale_stage_alert_days": stale_stage_alert_days,
        "on_track": on_track,
        "slack_or_gap_days": slack_or_gap,
        "verdict": "on_track_with_slack" if (on_track and slack_or_gap > 0) else ("on_track" if on_track else "at_risk_with_gap"),
        "critical_path_ids": cp_ids,
        "certifiable": certifiable,
        "certify_verdict": "CERTIFIABLE" if certifiable else "UNVERIFIED/AT_RISK",
        "open_items": open_items,
        "stale_flags": stale_flags,
        "scheduled_tasks": scheduled,
    }


# ---------------------------------------------------------------------------
# Table printer
# ---------------------------------------------------------------------------

def print_summary(result: Dict[str, object]) -> None:
    print(f"\n=== {result['unit']} ===")
    print(f"  Possession: {result['possession_date']}  |  Target: {result['target_date']} ({result['target_days']}d)")
    print(f"  Ready date: {result['ready_date']}  |  Day count: {result['day_count']}d")
    print(f"  Track status: {result['verdict'].upper()}", end="")
    gap = result['slack_or_gap_days']
    if gap > 0:
        print(f" (+{gap}d slack)")
    elif gap < 0:
        print(f" ({gap}d gap — {-gap} days late)")
    else:
        print(" (exactly on target)")
    print(f"  Certify gate: {result['certify_verdict']}")
    if result["open_items"]:
        for item in result["open_items"]:
            print(f"    - {item}")
    if result["stale_flags"]:
        print("  STALE ALERTS:")
        for flag in result["stale_flags"]:
            print(f"    ! {flag}")

    # Task table
    fields = ["id", "name", "trade", "start_date", "end_date", "must_fix", "verified_done", "is_rekey"]
    tasks: List[Dict[str, object]] = result["scheduled_tasks"]
    widths = {f: max(len(f), *(len(str(t.get(f, ""))) for t in tasks)) for f in fields}
    print()
    print("  " + " | ".join(f.ljust(widths[f]) for f in fields))
    print("  " + "-+-".join("-" * widths[f] for f in fields))
    for t in tasks:
        cp_marker = " *" if t.get("is_critical_path") else "  "
        print(cp_marker + " | ".join(str(t.get(f, "")).ljust(widths[f]) for f in fields))
    print("  (* = critical path)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Make-ready pipeline day-count, critical-path, and certification engine."
    )
    parser.add_argument("--demo", action="store_true", help="Use built-in synthetic demo data.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--tasks", help="JSON file with list of task objects.")
    parser.add_argument("--possession-date", help="Possession date as YYYY-MM-DD.")
    parser.add_argument("--target-days", type=int, default=TURN_TARGET_DAYS, help=f"Target days to rent-ready (default {TURN_TARGET_DAYS}).")
    parser.add_argument("--stale-stage-alert-days", type=int, help="No-progress threshold; defaults to the configured agent value.")
    args = parser.parse_args(argv)

    stale_days = args.stale_stage_alert_days
    if stale_days is None:
        config_path = Path(__file__).resolve().parents[3] / "config.json"
        try:
            stale_days = int(json.loads(config_path.read_text())["stale_stage_alert_days"])
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            parser.error(f"configured stale_stage_alert_days is unavailable: {exc}")

    if args.demo:
        turns, possession_date = demo_tasks()
        results = []
        for turn in turns:
            results.append(analyze_turn(
                tasks=turn["tasks"],
                possession_date=possession_date,
                target_days=args.target_days,
                stale_stage_alert_days=stale_days,
                unit_label=turn["unit"],
            ))
    elif args.tasks:
        possession_date = parse_date(args.possession_date) if args.possession_date else dt.date.today()
        if possession_date is None:
            parser.error("--possession-date must be YYYY-MM-DD")
        with open(args.tasks, encoding="utf-8") as fh:
            raw = json.load(fh)
        # Support either a flat list of tasks or a list of {unit, tasks} dicts
        if raw and isinstance(raw[0], dict) and "tasks" in raw[0]:
            results = [
                analyze_turn(r["tasks"], possession_date, args.target_days, stale_days, r.get("unit", f"unit-{i}"))
                for i, r in enumerate(raw)
            ]
        else:
            results = [analyze_turn(raw, possession_date, args.target_days, stale_days)]
    else:
        parser.error("Either --demo or --tasks is required.")

    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for r in results:
            print_summary(r)

    return 0


if __name__ == "__main__":
    sys.exit(main())
