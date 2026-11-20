import argparse
import sys
from pathlib import Path

# Sibling imports
import config
from baton import set_baton
from roster import sync_roster_to_agents


def init_board(
    base_dir: Path | None = None,
    orchestrator: str | None = None,
    mason: str | None = None,
    reviewer: str | None = None,
) -> Path:
    root = base_dir if base_dir else config.BASE_DIR
    agents_dir = root / ".agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    # 1. Pipeline stages (00_specs to 05_escalation)
    for stage in config.STAGES:
        stage_dir = agents_dir / stage
        stage_dir.mkdir(parents=True, exist_ok=True)
        keep_file = stage_dir / ".gitkeep"
        if not any(stage_dir.iterdir()):
            keep_file.touch()

    # 2. Project Config & Roles
    cfg = config.load_project_config(root)
    roles = cfg.get("roles", config.DEFAULT_CONFIG["roles"]).copy()
    if orchestrator:
        roles["orchestrator"] = orchestrator
    if mason:
        roles["mason"] = mason
    if reviewer:
        roles["reviewer"] = reviewer
    cfg["roles"] = roles
    config.save_project_config(cfg, root)

    # 3. Init BATON.json
    set_baton(
        holder="orchestrator",
        task_id=None,
        action="project_initialized",
        base_dir=root,
    )

    # 4. Init Roster and sync CLAUDE.md / CODEX.md / AGENTS.md
    sync_roster_to_agents(root, roles_override=roles)

    # 5. Create Task Template INSIDE .agents/
    template_path = agents_dir / "template_task.md"
    if not template_path.exists():
        template_content = """---
id: "TASK-01"
title: "Tên tiêu đề task"
stage: "01_backlog"
assignee: "mason"
reviewer: "reviewer"
spec_ref: "00_specs/SPEC-01.md"
reject_count: 0
max_rejections: 2
created_at: "2026-10-17T00:00:00Z"
updated_at: "2026-10-17T00:00:00Z"
---

# TASK-01: Tên tiêu đề task

## Mục tiêu
Mô tả rõ kết quả cần đạt được.

## Tiêu chí nghiệm thu (Acceptance Criteria)
- [ ] Chức năng A hoạt động đúng spec.
- [ ] Có unit test kiểm thử edge case.
- [ ] Chạy linter không báo lỗi.

## Tài liệu tham khảo
- Đặc tả: `.agents/00_specs/SPEC-01.md`
"""
        template_path.write_text(template_content, encoding="utf-8")

    return agents_dir


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Initialize Agents_Board Multi-Agent System")
    parser.add_argument("--dir", default=None, help="Target project root directory (default: current directory)")
    parser.add_argument("--orchestrator", choices=config.VALID_PLATFORMS, default=None, help="Assign Orchestrator (default: antigravity)")
    parser.add_argument("--mason", choices=config.VALID_PLATFORMS, default=None, help="Assign Mason/Coder (default: claude)")
    parser.add_argument("--reviewer", choices=config.VALID_PLATFORMS, default=None, help="Assign Reviewer (default: codex)")

    args = parser.parse_args(argv)
    target_path = Path(args.dir).resolve() if args.dir else None

    out = init_board(
        base_dir=target_path,
        orchestrator=args.orchestrator,
        mason=args.mason,
        reviewer=args.reviewer,
    )
    print(f"\n[INIT] ✅ Agents_Board successfully initialized at: {out}")
    print("       • Pipeline columns: 00_specs -> 05_escalation created.")
    print("       • Baton initialized to 'orchestrator'.")
    print(f"       • Role Matrix: orchestrator={args.orchestrator or 'antigravity'}, mason={args.mason or 'claude'}, reviewer={args.reviewer or 'codex'}")
    print("       • System instruction files synced: CLAUDE.md, CODEX.md, AGENTS.md.")
    print("       • Task template created: .agents/template_task.md\n")


if __name__ == "__main__":
    main()
