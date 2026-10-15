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
