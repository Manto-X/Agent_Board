import argparse
from pathlib import Path

from agents_board.config import AGENTS_DIR, BASE_DIR, ROSTER_DIR

DEFAULT_ROSTERS = {
    "orchestrator.md": """# Role: Orchestrator & System Auditor (Antigravity / Gemini)

## Core Responsibilities
- Phỏng vấn và chốt yêu cầu (Spec) với Sếp qua /grill-me.
- Phân rã dự án thành các task nhỏ, viết vào `.agents/01_backlog/`.
- Trao quyền giữ gậy tiếp sức (`BATON.json`) cho Mason hoặc Reviewer.
- Đóng vai Tòa Phúc Thẩm (Supreme Court) phân xử các tranh chấp tại `05_escalation/`.

## Boundaries & Permissions
- **CAN_WRITE:** `.agents/00_specs/`, `.agents/01_backlog/`, `.agents/BATON.json`, `.agents/05_escalation/`.
- **CAN_READ:** Toàn bộ repository.
- **FORBIDDEN:** Không trực tiếp viết mã tính năng khi Mason đang active (trừ khi hotfix khẩn cấp được Sếp duyệt).
""",
    "mason.md": """# Role: Mason & Implementation Engine (Claude Code)

## Core Responsibilities
- Đọc spec từ `.agents/00_specs/` và task được giao tại `.agents/02_in_progress/`.
- Viết mã nguồn, bổ sung unit tests đầy đủ.
- Chạy kiểm thử cục bộ trên máy, đảm bảo 100% pass trước khi nộp review.
- Chuyển task sang `.agents/03_review/` và pass `BATON` cho Reviewer.

## Boundaries & Permissions
- **CAN_WRITE:** `src/`, `tests/`, `agents_board/`, `.agents/02_in_progress/`, `.agents/03_review/`.
- **CAN_READ:** Toàn bộ repository.
- **FORBIDDEN:** 
  - Không tự ý duyệt task sang `04_done/`.
  - Không sửa file đặc tả `00_specs/`.
  - Không bắt đầu code nếu chưa giữ `BATON` (`holder != "mason"`).
""",
    "reviewer.md": """# Role: Reviewer & Quality Gate (Codex / GPT)

## Core Responsibilities
- Đọc code diff và task ticket trong `.agents/03_review/`.
- Kiểm tra tính đúng đắn về thuật toán, bảo mật, và khả năng mở rộng.
- Phê duyệt: Di chuyển task sang `.agents/04_done/` và chuyển `BATON` về cho Orchestrator.
- Từ chối: Gọi lệnh `python -m agents_board.task reject <id> --reason <lý_do> --severity <BLOCKER|MAJOR|NITPICK>`.

## Boundaries & Permissions
- **CAN_WRITE:** `.agents/03_review/`, `.agents/04_done/`, `.agents/05_escalation/`.
- **CAN_READ:** Toàn bộ repository.
- **FORBIDDEN:**
  - Không tự tay sửa mã nguồn tính năng.
  - Không từ chối vì lý do `NITPICK` (tiểu tiết/format).
  - Bắt buộc phải cung cấp test case tái hiện lỗi nếu đánh giá `BLOCKER`.
""",
}


def init_roster_files(base_dir: Path | None = None) -> None:
    roster_dir = (base_dir / ".agents" / "roster") if base_dir else ROSTER_DIR
    roster_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in DEFAULT_ROSTERS.items():
        file_path = roster_dir / filename
        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")


def sync_roster_to_agents(base_dir: Path | None = None) -> dict[str, Path]:
    root_dir = base_dir if base_dir else BASE_DIR
    init_roster_files(root_dir)
    roster_dir = root_dir / ".agents" / "roster"

    mason_content = (roster_dir / "mason.md").read_text(encoding="utf-8")
    reviewer_content = (roster_dir / "reviewer.md").read_text(encoding="utf-8")
    orchestrator_content = (roster_dir / "orchestrator.md").read_text(encoding="utf-8")

    # 1. Sync CLAUDE.md for Claude Code
    claude_md = root_dir / "CLAUDE.md"
    claude_header = (
        "# CLAUDE.md — Agent Instruction for Claude Code\n\n"
        "> Tệp này được đồng bộ tự động từ `.agents/roster/mason.md`.\n"
        "> Bạn đang đảm nhiệm vai trò **MASON** trong hệ thống Agents_Board.\n\n"
        "## QUY TẮC BẮT BUỘC:\n"
        "1. Trước khi làm việc: Luôn kiểm tra `.agents/BATON.json`. Chỉ thực hiện task khi `holder == 'mason'`.\n"
        "2. Khi làm xong: Đổi trạng thái task sang `03_review` bằng lệnh:\n"
        "   `python -m agents_board.task move <TASK_ID> review`\n"
        "   `python -m agents_board.baton pass reviewer --task-id <TASK_ID>`\n\n"
    )
    claude_md.write_text(claude_header + mason_content, encoding="utf-8")

    # 2. Sync CODEX.md for OpenAI Codex
    codex_md = root_dir / "CODEX.md"
    codex_header = (
        "# CODEX.md — Agent Instruction for Codex\n\n"
        "> Tệp này được đồng bộ tự động từ `.agents/roster/reviewer.md`.\n"
        "> Bạn đang đảm nhiệm vai trò **REVIEWER** trong hệ thống Agents_Board.\n\n"
        "## QUY TẮC BẮT BUỘC:\n"
        "1. Chỉ review khi nhận được `BATON` (`holder == 'reviewer'`).\n"
        "2. Đạt yêu cầu: Chuyển task sang `04_done`:\n"
        "   `python -m agents_board.task move <TASK_ID> done`\n"
        "   `python -m agents_board.baton pass orchestrator`\n"
        "3. Từ chối: Phải có test case và dùng lệnh:\n"
        "   `python -m agents_board.task reject <TASK_ID> --reason '<lý_do>' --severity BLOCKER`\n\n"
    )
    codex_md.write_text(codex_header + reviewer_content, encoding="utf-8")

    # 3. Sync AGENTS.md for Antigravity / Gemini
    agents_md = root_dir / "AGENTS.md"
    agents_header = (
        "# AGENTS.md — Global Multi-Agent Blackboard Protocol\n\n"
        "> Tệp này định nghĩa giao thức phối hợp giữa Antigravity, Claude Code và Codex.\n\n"
    )
    agents_md.write_text(
        agents_header + orchestrator_content + "\n\n---\n\n" + mason_content + "\n\n---\n\n" + reviewer_content,
        encoding="utf-8",
    )

    return {
        "CLAUDE.md": claude_md,
        "CODEX.md": codex_md,
        "AGENTS.md": agents_md,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Agents_Board Roster Manager")
    parser.add_argument("--sync", action="store_true", help="Sync roster cards to CLAUDE.md, CODEX.md, AGENTS.md")
    parser.add_argument("--init", action="store_true", help="Initialize default role cards in .agents/roster/")

    args = parser.parse_args()

    if args.init:
        init_roster_files()
        print("[ROSTER] Initialized default roles in .agents/roster/")

    if args.sync or not (args.init):
        synced = sync_roster_to_agents()
        print("[ROSTER] Synced role configurations:")
        for name, p in synced.items():
            print(f"  • {name} -> {p}")


if __name__ == "__main__":
    main()
