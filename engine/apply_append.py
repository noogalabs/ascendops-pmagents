#!/usr/bin/env python3
"""Apply one persisted cross-seat append plan to its owner seat atomically."""
import argparse
import json
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
    appender_mapping = (json.loads(args.appender_mapping.read_text())
                        if args.appender_mapping else None)
    owner_mapping = (json.loads(args.owner_mapping.read_text())
                     if args.owner_mapping else None)
    try:
        changed = engine.apply_persisted_append(
            args.appender_agent_dir.resolve(), args.owner_agent_dir.resolve(), args.plan_id,
            appender_mapping=appender_mapping, owner_mapping=owner_mapping,
        )
    except engine.IntakeRejected as exc:
        print(exc.render())
        return 2
    print("applied" if changed else "already-applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
