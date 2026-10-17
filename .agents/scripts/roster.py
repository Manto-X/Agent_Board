import argparse
import json
from pathlib import Path

# Sibling import from config
import config

DEFAULT_ROSTERS = {
    "orchestrator.md": """# Role: Orchestrator & System Auditor

## Core Responsibilities
- Phỏng vấn và chốt yêu cầu (Spec) với Sếp qua /grill-me.
- Phân rã dự án thành các task nhỏ, viết vào `.agents/01_backlog/`.
- Trao quyền giữ gậy tiếp sức (`BATON.json`) cho Mason hoặc Reviewer.
- Đóng vai Tòa Phúc Thẩm (Supreme Court) phân xử các tranh chấp tại `05_escalation/`.

## Boundaries & Permissions
- **CAN_WRITE:** `.agents/00_specs/`, `.agents/01_backlog/`, `.agents/BATON.json`, `.agents/05_escalation/`.
- **CAN_READ:** Toàn bộ repository.
- **FORBIDDEN:** Không trực tiếp viết mã tính năng khi Mason đang active (trừ khi hotfix khẩn cấp được Sếp duyệt).

## CLI Quick Reference
- Tạo task: `python .agents/board.py task create --id TASK-01 --title "Tiêu đề" --assignee mason --reviewer reviewer`
- Chuyển gậy: `python .agents/board.py baton pass mason --task-id TASK-01`
- Xem trạng thái: `python .agents/board.py baton status`
""",
    "mason.md": """# Role: Mason & Implementation Engine

## Core Responsibilities
- Đọc spec từ `.agents/00_specs/` và task được giao tại `.agents/02_in_progress/`.
- Viết mã nguồn, bổ sung unit tests đầy đủ.
- Chạy kiểm thử cục bộ trên máy, đảm bảo 100% pass trước khi nộp review.
- Chuyển task sang `.agents/03_review/` và pass `BATON` cho Reviewer.

## Boundaries & Permissions
- **CAN_WRITE:** `src/`, `tests/`, `scripts/`, `.agents/02_in_progress/`, `.agents/03_review/`.
- **CAN_READ:** Toàn bộ repository.
- **FORBIDDEN:** 
  - Không tự ý duyệt task sang `04_done/`.
  - Không sửa file đặc tả `00_specs/`.
  - Không bắt đầu code nếu chưa giữ `BATON` (`holder != "mason"`).

## CLI Quick Reference
- Nhận task & nộp review:
  `python .agents/board.py task move <TASK_ID> review`
  `python .agents/board.py baton pass reviewer --task-id <TASK_ID>`
""",
    "reviewer.md": """# Role: Reviewer & Quality Gate

## Core Responsibilities
- Đọc code diff và task ticket trong `.agents/03_review/`.
- Kiểm tra tính đúng đắn về thuật toán, bảo mật, và khả năng mở rộng.
- Phê duyệt: Di chuyển task sang `.agents/04_done/` và chuyển `BATON` về cho Orchestrator.
- Từ chối: Gọi lệnh `python .agents/board.py task reject <id> --reason <lý_do> --severity <BLOCKER|MAJOR|NITPICK>`.

## Boundaries & Permissions
- **CAN_WRITE:** `.agents/03_review/`, `.agents/04_done/`, `.agents/05_escalation/`.
- **CAN_READ:** Toàn bộ repository.
- **FORBIDDEN:**
  - Không tự tay sửa mã nguồn tính năng.
  - Không từ chối vì lý do `NITPICK` (tiểu tiết/format).
  - Bắt buộc phải cung cấp test case tái hiện lỗi nếu đánh giá `BLOCKER`.

## CLI Quick Reference
- Duyệt hoàn thành:
  `python .agents/board.py task move <TASK_ID> done`
  `python .agents/board.py baton pass orchestrator`
- Từ chối:
  `python .agents/board.py task reject <TASK_ID> --reason "<lý_do>" --severity BLOCKER`
""",
}


def init_roster_files(base_dir: Path | None = None) -> None:
    agents_dir = (base_dir / ".agents") if base_dir else config.AGENTS_DIR
    roster_dir = agents_dir / "roster"
    roster_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in DEFAULT_ROSTERS.items():
        file_path = roster_dir / filename
        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")


def sync_roster_to_agents(base_dir: Path | None = None, roles_override: dict | None = None) -> dict[str, Path]:
    root_dir = base_dir if base_dir else config.BASE_DIR
    agents_dir = root_dir / ".agents"
    init_roster_files(root_dir)

    cfg = config.load_project_config(root_dir)
    roles = roles_override or cfg.get("roles", config.DEFAULT_CONFIG["roles"])

    # Map platform -> assigned role
    platform_role_map = {}
    for role_name, platform in roles.items():
        platform_role_map[platform] = role_name

    roster_dir = agents_dir / "roster"
    orchestrator_md = (roster_dir / "orchestrator.md").read_text(encoding="utf-8")
    mason_md = (roster_dir / "mason.md").read_text(encoding="utf-8")
    reviewer_md = (roster_dir / "reviewer.md").read_text(encoding="utf-8")

    role_content_map = {
        "orchestrator": orchestrator_md,
        "mason": mason_md,
        "reviewer": reviewer_md,
    }

    # 1. Sync CLAUDE.md for Claude Code
    claude_role = platform_role_map.get("claude", "mason")
    claude_md = root_dir / "CLAUDE.md"
    claude_header = (
        f"# CLAUDE.md — Agent Instruction for Claude Code\n\n"
        f"> Tệp này được đồng bộ tự động từ `.agents/roster/{claude_role}.md`.\n"
        f"> Bạn đang đảm nhiệm vai trò **{claude_role.upper()}** trong hệ thống Agents_Board.\n\n"
    )
    claude_md.write_text(claude_header + role_content_map.get(claude_role, mason_md), encoding="utf-8")

    # 2. Sync CODEX.md for OpenAI Codex
    codex_role = platform_role_map.get("codex", "reviewer")
    codex_md = root_dir / "CODEX.md"
    codex_header = (
        f"# CODEX.md — Agent Instruction for Codex\n\n"
        f"> Tệp này được đồng bộ tự động từ `.agents/roster/{codex_role}.md`.\n"
        f"> Bạn đang đảm nhiệm vai trò **{codex_role.upper()}** trong hệ thống Agents_Board.\n\n"
    )
    codex_md.write_text(codex_header + role_content_map.get(codex_role, reviewer_md), encoding="utf-8")

    # 3. Sync AGENTS.md for Antigravity / Gemini
    antigravity_role = platform_role_map.get("antigravity", "orchestrator")
    agents_md = root_dir / "AGENTS.md"
    agents_header = (
        f"# AGENTS.md — Global Multi-Agent Blackboard Protocol\n\n"
        f"> Tệp này định nghĩa giao thức phối hợp giữa Antigravity, Claude Code và Codex.\n"
        f"> Antigravity đang đảm nhiệm vai trò chính: **{antigravity_role.upper()}**.\n\n"
        f"## MA TRẬN PHÂN VAI HIỆN TẠI (ROLE MATRIX):\n"
        f"- **Orchestrator:** `{roles.get('orchestrator', 'antigravity')}`\n"
        f"- **Mason (Code):** `{roles.get('mason', 'claude')}`\n"
        f"- **Reviewer (Audit):** `{roles.get('reviewer', 'codex')}`\n\n"
        f"---\n\n"
    )
    agents_md.write_text(
        agents_header + orchestrator_md + "\n\n---\n\n" + mason_md + "\n\n---\n\n" + reviewer_md,
        encoding="utf-8",
    )

    return {
        "CLAUDE.md": claude_md,
        "CODEX.md": codex_md,
        "AGENTS.md": agents_md,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Agents_Board Roster Manager")
    parser.add_argument("--sync", action="store_true", help="Sync roster cards to CLAUDE.md, CODEX.md, AGENTS.md")
    parser.add_argument("--init", action="store_true", help="Initialize default role cards in .agents/roster/")
    parser.add_argument("--orchestrator", choices=config.VALID_PLATFORMS, help="Assign Orchestrator platform")
    parser.add_argument("--mason", choices=config.VALID_PLATFORMS, help="Assign Mason platform")
    parser.add_argument("--reviewer", choices=config.VALID_PLATFORMS, help="Assign Reviewer platform")

    args = parser.parse_args(argv)

    if args.init:
        init_roster_files()
        print("[ROSTER] Initialized default roles in .agents/roster/")

    cfg = config.load_project_config()
    roles = cfg.get("roles", config.DEFAULT_CONFIG["roles"]).copy()

    updated = False
    if args.orchestrator:
        roles["orchestrator"] = args.orchestrator
        updated = True
    if args.mason:
        roles["mason"] = args.mason
        updated = True
    if args.reviewer:
        roles["reviewer"] = args.reviewer
        updated = True

    if updated:
        cfg["roles"] = roles
        config.save_project_config(cfg)
        print(f"[ROSTER] Updated role assignments in project_config.json: {roles}")

    synced = sync_roster_to_agents(roles_override=roles)
    print("[ROSTER] Synced role configurations to agent instruction files:")
    for name, p in synced.items():
        print(f"  • {name} -> {p}")


if __name__ == "__main__":
    main()
