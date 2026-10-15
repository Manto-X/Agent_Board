import argparse
import json
import os
import sys
import time
from pathlib import Path

from agents_board.baton import get_baton
from agents_board.config import AGENTS_DIR, BASE_DIR, STAGES
from agents_board.task import list_tasks

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RED = "\033[31m"
MAGENTA = "\033[35m"


def ring_bell() -> None:
    try:
        if sys.platform == "win32":
            import winsound

            winsound.Beep(1000, 250)
        else:
            sys.stdout.write("\a")
            sys.stdout.flush()
    except Exception:
        pass


def scan_state(base_dir: Path | None = None) -> tuple[dict, dict[str, list[str]]]:
    baton = get_baton(base_dir=base_dir)
    tasks = list_tasks(base_dir=base_dir)
    task_map = {}
    for stage, tlist in tasks.items():
        task_map[stage] = [f"{t.get('id')}:{t.get('reject_count', 0)}" for t in tlist]
    return baton, task_map


def print_banner() -> None:
    banner = f"""{BOLD}{CYAN}
============================================================
              AGENTS_BOARD EVENT WATCHER DAEMON             
============================================================{RESET}
Listening for Baton transitions & Task movements...
Press Ctrl+C to stop.
"""
    print(banner)


def run_watcher(poll_interval: float = 1.0, once: bool = False, base_dir: Path | None = None) -> None:
    print_banner()
    last_baton, last_tasks = scan_state(base_dir=base_dir)

    print(
        f"[{time.strftime('%H:%M:%S')}] {BOLD}Current Baton:{RESET} {GREEN}{last_baton.get('holder')}{RESET} | Action: {last_baton.get('action')}"
    )

    if once:
        return

    try:
        while True:
            time.sleep(poll_interval)
            current_baton, current_tasks = scan_state(base_dir=base_dir)

            # Check Baton transition
            if (
                current_baton.get("holder") != last_baton.get("holder")
                or current_baton.get("task_id") != last_baton.get("task_id")
                or current_baton.get("action") != last_baton.get("action")
            ):
                ring_bell()
                print(
                    f"\n[{time.strftime('%H:%M:%S')}] 🔔 {BOLD}BATON TRANSFERRED:{RESET} "
                    f"{YELLOW}{last_baton.get('holder')}{RESET} ➔ {GREEN}{BOLD}{current_baton.get('holder')}{RESET}"
                )
                print(
                    f"           Task: {CYAN}{current_baton.get('task_id')}{RESET} | Action: {current_baton.get('action')}"
                )
                last_baton = current_baton

            # Check Task movements
            for stage in STAGES:
                cur_list = current_tasks.get(stage, [])
                old_list = last_tasks.get(stage, [])

                # Tasks added to this stage
                added = set(cur_list) - set(old_list)
                if added:
                    ring_bell()
                    color = RED if "escalation" in stage else (GREEN if "done" in stage else CYAN)
                    for item in added:
                        task_id, rejs = item.split(":")
                        print(
                            f"[{time.strftime('%H:%M:%S')}] 📦 Task {BOLD}{task_id}{RESET} moved to {color}[{stage.upper()}]{RESET} (Rejects: {rejs})"
                        )
                        if "escalation" in stage:
                            print(
                                f"           {RED}{BOLD}⚠️ CIRCUIT BREAKER TRIPPED! Review threshold exceeded.{RESET}"
                            )

            last_tasks = current_tasks

    except KeyboardInterrupt:
        print(f"\n{YELLOW}Watcher stopped by user.{RESET}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agents_Board Event Watcher")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds")
    parser.add_argument("--once", action="store_true", help="Scan once and exit")
    args = parser.parse_args()

    run_watcher(poll_interval=args.interval, once=args.once)


if __name__ == "__main__":
    main()
