import argparse
import datetime
import json
import os
import sys
from pathlib import Path

# Sibling import from config
import config


def get_baton(base_dir: Path | None = None) -> dict:
    baton_path = (base_dir / ".agents" / "BATON.json") if base_dir else config.BATON_FILE
    if not baton_path.exists():
        return {
            "holder": "orchestrator",
            "task_id": None,
            "action": "idle",
            "acquired_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "expires_at": None,
        }
    with open(baton_path, "r", encoding="utf-8") as f:
        return json.load(f)


def set_baton(
    holder: str,
    task_id: str | None = None,
    action: str | None = None,
    expires_at: str | None = None,
    base_dir: Path | None = None,
) -> dict:
    agents_dir = (base_dir / ".agents") if base_dir else config.AGENTS_DIR
    agents_dir.mkdir(parents=True, exist_ok=True)
    baton_path = agents_dir / "BATON.json"
    temp_path = agents_dir / "BATON.json.tmp"

    data = {
        "holder": holder,
        "task_id": task_id,
        "action": action or "idle",
        "acquired_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "expires_at": expires_at,
    }

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    os.replace(temp_path, baton_path)
    return data


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Agents_Board Baton Manager")
    subparsers = parser.add_subparsers(dest="command")

    # Status
    subparsers.add_parser("status", help="Show current baton status")

    # Pass
    pass_parser = subparsers.add_parser("pass", help="Pass baton to an agent")
    pass_parser.add_argument("holder", help="Agent identifier (e.g. mason, reviewer, orchestrator)")
    pass_parser.add_argument("--task-id", dest="task_id", default=None, help="Associated Task ID")
    pass_parser.add_argument("--action", dest="action", default="working", help="Current intended action")

    # Acquire
    acquire_parser = subparsers.add_parser("acquire", help="Acquire baton if free or authorized")
    acquire_parser.add_argument("holder", help="Agent attempting acquisition")
    acquire_parser.add_argument("--task-id", dest="task_id", default=None, help="Task ID")

    # Recover
    subparsers.add_parser("recover", help="Force reset baton to orchestrator")

    args = parser.parse_args(argv)

    if args.command == "status" or not args.command:
        baton = get_baton()
        print(f"[BATON] Holder : {baton.get('holder')}")
        print(f"        Task   : {baton.get('task_id')}")
        print(f"        Action : {baton.get('action')}")
        print(f"        Since  : {baton.get('acquired_at')}")
    elif args.command == "pass":
        baton = set_baton(holder=args.holder, task_id=args.task_id, action=args.action)
        print(f"[BATON] Passed to '{baton['holder']}' for action '{baton['action']}'.")
    elif args.command == "acquire":
        baton = set_baton(holder=args.holder, task_id=args.task_id, action="working")
        print(f"[BATON] Acquired by '{baton['holder']}'.")
    elif args.command == "recover":
        baton = set_baton(holder="orchestrator", task_id=None, action="recovered")
        print("[BATON] Reset to 'orchestrator'.")


if __name__ == "__main__":
    main()
