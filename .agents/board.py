#!/usr/bin/env python3
"""
Agents_Board Unified CLI Dispatcher
Provides short, memorable commands for all agents and users:
  python .agents/board.py task <cmd>
  python .agents/board.py baton <cmd>
  python .agents/board.py watch
  python .agents/board.py roster <cmd>
  python .agents/board.py init
"""

import sys
from pathlib import Path

# Add scripts directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import baton
import config
import init
import roster
import task
import watcher


def print_help() -> None:
    print("""
🧭 AGENTS_BOARD CLI (Zero-Install Multi-Agent Blackboard)

Usage:
  python .agents/board.py <subcommand> [args...]

Subcommands:
  task      Manage Kanban tasks (list, create, move, reject, show)
            • list:                   python .agents/board.py task list
            • move to review:         python .agents/board.py task move TASK-01 review
            • move to done:           python .agents/board.py task move TASK-01 done
            • reject (blocker):       python .agents/board.py task reject TASK-01 --reason "Bug" --severity BLOCKER

  baton     Manage the Baton semaphore (status, pass, acquire, recover)
            • check who holds baton:  python .agents/board.py baton status
            • pass to mason:          python .agents/board.py baton pass mason --task-id TASK-01
            • pass to reviewer:       python .agents/board.py baton pass reviewer --task-id TASK-01
            • reset to orchestrator:  python .agents/board.py baton recover

  watch     Start real-time sound & event watcher daemon
            • run watcher:            python .agents/board.py watch

  roster    Manage & sync role assignments
            • sync prompts:           python .agents/board.py roster --sync
            • assign custom roles:    python .agents/board.py roster --orchestrator claude --mason antigravity

  init      Initialize a new workspace
            • bootstrap board:        python .agents/board.py init
""")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "help"]:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    sub_args = sys.argv[2:]

    if cmd == "task":
        task.main(sub_args)
    elif cmd == "baton":
        baton.main(sub_args)
    elif cmd in ["watch", "watcher"]:
        watcher.main(sub_args)
    elif cmd == "roster":
        roster.main(sub_args)
    elif cmd == "init":
        init.main(sub_args)
    else:
        print(f"Unknown subcommand '{cmd}'. Run 'python .agents/board.py help' for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
