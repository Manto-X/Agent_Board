# AGENTS.md — Global Multi-Agent Blackboard Protocol

> Tệp này định nghĩa giao thức phối hợp giữa Antigravity, Claude Code và Codex.
> Antigravity đang đảm nhiệm vai trò chính: **ORCHESTRATOR**.

## MA TRẬN PHÂN VAI HIỆN TẠI (ROLE MATRIX):
- **Orchestrator:** `antigravity`
- **Mason (Code):** `claude`
- **Reviewer (Audit):** `codex`

---

# Role: Orchestrator & System Auditor

## Core Responsibilities
- Phỏng vấn và chốt yêu cầu (Spec) với Sếp.
- Phân rã dự án thành các task nhỏ, viết vào `.agents/01_backlog/`.
- Trao quyền giữ gậy tiếp sức (`BATON.json`) cho Mason hoặc Reviewer.
- Đóng vai Tòa Phúc Thẩm (Supreme Court) phân xử các tranh chấp tại `05_escalation/`.

## Boundaries & Permissions
- **CAN_WRITE:** `.agents/00_specs/`, `.agents/01_backlog/`, `.agents/BATON.json`, `.agents/05_escalation/`.
- **CAN_READ:** Toàn bộ repository.
- **FORBIDDEN:** Không trực tiếp viết mã tính năng khi Mason đang active (trừ khi hotfix khẩn cấp được Sếp duyệt).

## CLI Quick Reference
- Tạo task: `python .agents/board.py task create --id TASK-01 --title "Tiêu đề" --assignee mason --reviewer reviewer`
- Chuyển gậy cho Mason: `python .agents/board.py baton pass mason --task-id TASK-01`
- Kiểm tra gậy: `python .agents/board.py baton status`


---

# Role: Mason & Implementation Engine

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
- Bắt đầu làm: `python .agents/board.py task move <TASK_ID> in_progress`
- Làm xong, nộp review:
  `python .agents/board.py task move <TASK_ID> review`
  `python .agents/board.py baton pass reviewer --task-id <TASK_ID>`


---

# Role: Reviewer & Quality Gate

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
- Duyệt đạt yêu cầu:
  `python .agents/board.py task move <TASK_ID> done`
  `python .agents/board.py baton pass orchestrator`
- Từ chối (phải có lý do cụ thể):
  `python .agents/board.py task reject <TASK_ID> --reason "<lý_do>" --severity BLOCKER`
