#!/usr/bin/env python3
"""Apply one persisted cross-seat append plan to its owner seat atomically."""
import argparse
import sys
from pathlib import Path

import engine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("appender_agent_dir", type=Path)
    parser.add_argument("owner_agent_dir", type=Path)
    parser.add_argument("plan_id")
    parser.add_argument("--appender-mapping", type=Path)
    parser.add_argument("--owner-mapping", type=Path)
    args = parser.parse_args()
    try:
        appender_mapping = (engine.read_member_json(
            args.appender_mapping, f"appender_mapping.{args.appender_mapping.name}"
        ) if args.appender_mapping else None)
        owner_mapping = (engine.read_member_json(
            args.owner_mapping, f"owner_mapping.{args.owner_mapping.name}"
        ) if args.owner_mapping else None)
        changed = engine.apply_persisted_append(
            args.appender_agent_dir.resolve(), args.owner_agent_dir.resolve(), args.plan_id,
            appender_mapping=appender_mapping, owner_mapping=owner_mapping,
        )
    except engine.IntakeRejected as exc:
        print(exc.render())
        return 2
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print("applied" if changed else "already-applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
