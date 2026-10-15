import argparse
from pathlib import Path

from agents_board.baton import set_baton
from agents_board.config import AGENTS_DIR, BASE_DIR, STAGES
from agents_board.roster import sync_roster_to_agents


def init_board(base_dir: Path | None = None) -> None:
    root = base_dir if base_dir else BASE_DIR
    agents_dir = root / ".agents"

    # 1. Create pipeline stage directories
    for stage in STAGES:
        stage_path = agents_dir / stage
        stage_path.mkdir(parents=True, exist_ok=True)
        # Create a keep file if empty
        keep_file = stage_path / ".gitkeep"
        if not any(stage_path.iterdir()):
            keep_file.touch()

    # 2. Init BATON.json
    set_baton(
        holder="orchestrator",
        task_id=None,
        action="project_initialized",
        base_dir=root,
    )

    # 3. Init Roster and sync CLAUDE.md / CODEX.md / AGENTS.md
    sync_roster_to_agents(root)

    # 4. Create Task Template
    template_path = root / "template_task.md"
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
created_at: "2026-10-16T00:00:00Z"
updated_at: "2026-10-16T00:00:00Z"
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

    print(f"[INIT] Agents_Board successfully initialized at: {root}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize Agents_Board in current project")
    parser.parse_args()
    init_board()


if __name__ == "__main__":
    main()
