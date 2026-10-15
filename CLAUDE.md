# CLAUDE.md — Agent Instruction for Claude Code

> Tệp này được đồng bộ tự động từ `.agents/roster/mason.md`.
> Bạn đang đảm nhiệm vai trò **MASON** trong hệ thống Agents_Board.

## QUY TẮC BẮT BUỘC:
1. Trước khi làm việc: Luôn kiểm tra `.agents/BATON.json`. Chỉ thực hiện task khi `holder == 'mason'`.
2. Khi làm xong: Đổi trạng thái task sang `03_review` bằng lệnh:
   `python -m agents_board.task move <TASK_ID> review`
   `python -m agents_board.baton pass reviewer --task-id <TASK_ID>`

# Role: Mason & Implementation Engine (Claude Code)

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
