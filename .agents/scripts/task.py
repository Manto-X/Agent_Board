import argparse
import datetime
import os
import re
import sys
from pathlib import Path

# Sibling imports from config & baton
import config
from baton import set_baton


def _get_agents_dir(base_dir: Path | None = None) -> Path:
    return (base_dir / ".agents") if base_dir else config.AGENTS_DIR


def parse_task_file(path: Path) -> tuple[dict, str]:
    content = path.read_text(encoding="utf-8")
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not frontmatter_match:
        return {}, content

    yaml_block = frontmatter_match.group(1)
    body = frontmatter_match.group(2)

    metadata = {}
    for line in yaml_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.isdigit():
                metadata[key] = int(val)
            else:
                metadata[key] = val
    return metadata, body


def write_task_file(path: Path, metadata: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".tmp")

    lines = ["---"]
    for k, v in metadata.items():
        if isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f'{k}: "{v}"')
    lines.append("---")
    lines.append(body.lstrip("\n"))

    content = "\n".join(lines)
    temp_path.write_text(content, encoding="utf-8")
    os.replace(temp_path, path)


def find_task(task_id: str, base_dir: Path | None = None) -> tuple[Path, dict, str] | None:
    agents_dir = _get_agents_dir(base_dir)
    filename = f"{task_id}.md"

    for stage in config.STAGES:
        stage_dir = agents_dir / stage
        task_path = stage_dir / filename
        if task_path.exists():
            metadata, body = parse_task_file(task_path)
            return task_path, metadata, body
    return None


def create_task(
    task_id: str,
    title: str,
    assignee: str = "mason",
    reviewer: str = "reviewer",
    spec_ref: str = "",
    body: str = "",
    max_rejections: int = config.DEFAULT_MAX_REJECTIONS,
    base_dir: Path | None = None,
) -> Path:
    agents_dir = _get_agents_dir(base_dir)
    target_dir = agents_dir / config.STAGE_BACKLOG
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{task_id}.md"

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    metadata = {
        "id": task_id,
        "title": title,
        "stage": config.STAGE_BACKLOG,
        "assignee": assignee,
        "reviewer": reviewer,
        "spec_ref": spec_ref,
        "reject_count": 0,
        "max_rejections": max_rejections,
        "created_at": now,
        "updated_at": now,
    }

    if not body.strip():
        body = f"# {task_id}: {title}\n\n## Mục tiêu\n(Chưa có nội dung mô tả)\n\n## Tiêu chí nghiệm thu (Acceptance Criteria)\n- [ ] Chức năng hoạt động đúng spec\n- [ ] Unit tests pass 100%\n"

    write_task_file(target_path, metadata, body)
    return target_path


def move_task(task_id: str, target_stage: str, base_dir: Path | None = None) -> Path:
    agents_dir = _get_agents_dir(base_dir)
    matched_stage = None
    for stage in config.STAGES:
        if target_stage == stage or target_stage in stage:
            matched_stage = stage
            break
    if not matched_stage:
        raise ValueError(f"Invalid target stage: '{target_stage}'. Valid stages: {config.STAGES}")

    found = find_task(task_id, base_dir=base_dir)
    if not found:
        raise FileNotFoundError(f"Task '{task_id}' not found in any stage.")

    current_path, metadata, body = found
    destination_dir = agents_dir / matched_stage
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_path = destination_dir / f"{task_id}.md"

    metadata["stage"] = matched_stage
    metadata["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    write_task_file(destination_path, metadata, body)
    if current_path != destination_path and current_path.exists():
        current_path.unlink()

    return destination_path


def reject_task(
    task_id: str,
    reason: str,
    severity: str = config.SEVERITY_BLOCKER,
    test_file: str | None = None,
    base_dir: Path | None = None,
) -> dict:
    severity = severity.upper()
    if severity not in config.VALID_SEVERITIES:
        raise ValueError(f"Invalid severity '{severity}'. Choose from: {config.VALID_SEVERITIES}")

    found = find_task(task_id, base_dir=base_dir)
    if not found:
        raise FileNotFoundError(f"Task '{task_id}' not found.")

    current_path, metadata, body = found

    if severity == config.SEVERITY_NITPICK:
        advisory_entry = (
            f"\n\n> [!NOTE] Advisory (NITPICK) - {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n"
            f"> Lý do: {reason}\n"
        )
        body += advisory_entry
        write_task_file(current_path, metadata, body)
        return {
            "status": "ADVISORY_ONLY",
            "message": "Nitpick noted. Task NOT rejected.",
            "reject_count": metadata.get("reject_count", 0),
            "stage": metadata.get("stage"),
        }

    reject_count = int(metadata.get("reject_count", 0)) + 1
    max_rejections = int(metadata.get("max_rejections", config.DEFAULT_MAX_REJECTIONS))
    metadata["reject_count"] = reject_count

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rejection_entry = (
        f"\n\n> [!WARNING] Rejection #{reject_count} [{severity}] - {now_iso}\n"
        f"> **Lý do:** {reason}\n"
    )
    if test_file:
        rejection_entry += f"> **Bằng chứng (Test file):** `{test_file}`\n"
    body += rejection_entry

    if reject_count >= max_rejections:
        metadata["stage"] = config.STAGE_ESCALATION
        target_path = move_task(task_id, config.STAGE_ESCALATION, base_dir=base_dir)
        write_task_file(target_path, metadata, body)
        set_baton(
            holder="orchestrator",
            task_id=task_id,
            action="arbitrate_dispute",
            base_dir=base_dir,
        )
        return {
            "status": "CIRCUIT_BREAKER_TRIGGERED",
            "message": f"Circuit breaker tripped! Rejection count reached {reject_count}/{max_rejections}. Escalated to orchestrator.",
            "reject_count": reject_count,
            "stage": config.STAGE_ESCALATION,
        }
    else:
        metadata["stage"] = config.STAGE_IN_PROGRESS
        target_path = move_task(task_id, config.STAGE_IN_PROGRESS, base_dir=base_dir)
        write_task_file(target_path, metadata, body)
        assignee = metadata.get("assignee", "mason")
        set_baton(
            holder=assignee,
            task_id=task_id,
            action="fix_rejection",
            base_dir=base_dir,
        )
        return {
            "status": "REJECTED",
            "message": f"Task rejected ({reject_count}/{max_rejections}). Returned to assignee '{assignee}' for fixing.",
            "reject_count": reject_count,
            "stage": config.STAGE_IN_PROGRESS,
        }


def list_tasks(base_dir: Path | None = None) -> dict[str, list[dict]]:
    agents_dir = _get_agents_dir(base_dir)
    board = {}
    # Kanban task columns: 01_backlog to 05_escalation
    task_stages = [s for s in config.STAGES if s != config.STAGE_SPECS]
    for stage in task_stages:
        board[stage] = []
        stage_dir = agents_dir / stage
        if stage_dir.exists():
            for p in sorted(stage_dir.glob("*.md")):
                meta, _ = parse_task_file(p)
                if meta.get("id"):
                    board[stage].append(meta)
    return board


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Agents_Board Task Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # create
    create_p = subparsers.add_parser("create", help="Create new task")
    create_p.add_argument("--id", required=True, help="Task ID (e.g. TASK-01)")
    create_p.add_argument("--title", required=True, help="Task Title")
    create_p.add_argument("--assignee", default="mason", help="Assigned Agent")
    create_p.add_argument("--reviewer", default="reviewer", help="Reviewing Agent")
    create_p.add_argument("--spec", default="", help="Spec reference path")
    create_p.add_argument("--max-rejections", type=int, default=config.DEFAULT_MAX_REJECTIONS)

    # move
    move_p = subparsers.add_parser("move", help="Move task to stage")
    move_p.add_argument("id", help="Task ID")
    move_p.add_argument("stage", help="Target stage (backlog, in_progress, review, done, escalation)")

    # reject
    reject_p = subparsers.add_parser("reject", help="Reject task with structured reason")
    reject_p.add_argument("id", help="Task ID")
    reject_p.add_argument("--reason", required=True, help="Failure explanation")
    reject_p.add_argument("--severity", choices=config.VALID_SEVERITIES, default=config.SEVERITY_BLOCKER)
    reject_p.add_argument("--test-file", default=None, help="Reproduction test file path")

    # list
    subparsers.add_parser("list", help="List all tasks across Kanban columns")

    # show
    show_p = subparsers.add_parser("show", help="Show task details")
    show_p.add_argument("id", help="Task ID")

    args = parser.parse_args(argv)

    if args.command == "create":
        p = create_task(
            task_id=args.id,
            title=args.title,
            assignee=args.assignee,
            reviewer=args.reviewer,
            spec_ref=args.spec,
            max_rejections=args.max_rejections,
        )
        print(f"[TASK] Created '{args.id}' at {p}")
    elif args.command == "move":
        p = move_task(task_id=args.id, target_stage=args.stage)
        print(f"[TASK] Moved '{args.id}' to {p.parent.name}")
    elif args.command == "reject":
        res = reject_task(
            task_id=args.id,
            reason=args.reason,
            severity=args.severity,
            test_file=args.test_file,
        )
        print(f"[TASK] Reject Result: {res['status']} | {res['message']}")
    elif args.command == "list" or not args.command:
        board = list_tasks()
        print("\n=================== AGENTS_BOARD KANBAN ===================")
        for stage, tasks in board.items():
            print(f"\n📂 [{stage.upper()}] ({len(tasks)} tasks):")
            for t in tasks:
                rejs = t.get("reject_count", 0)
                max_r = t.get("max_rejections", 2)
                print(f"  • {t.get('id')}: {t.get('title')} (Assignee: {t.get('assignee')} | Rejects: {rejs}/{max_r})")
        print("\n===========================================================")
    elif args.command == "show":
        found = find_task(args.id)
        if not found:
            print(f"Task '{args.id}' not found.")
            return
        p, meta, body = found
        print(f"Location: {p}")
        print("Metadata:", meta)
        print("\n--- BODY ---")
        print(body)


if __name__ == "__main__":
    main()
