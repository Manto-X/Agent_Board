# Kế hoạch triển khai: Agents_Board Toolkit

## Background & Problem Statement (Bối cảnh & Vấn đề)
- **Bối cảnh:** Hiện tại việc phối hợp nhiều AI độc lập (Claude Code, OpenAI Codex, Antigravity/Gemini) thường tốn kém chi phí token nếu dùng multi-agent API (AutoGen, CrewAI) hoặc đòi hỏi người dùng (Sếp) phải copy-paste ngữ cảnh thủ công giữa nhiều cửa sổ terminal.
- **Vấn đề:** 
  - Thiếu một kênh giao tiếp chung (Blackboard) lưu vết trực tiếp trong repository.
  - Nguy cơ xung đột ghi file (Race Condition) khi nhiều agent cùng thao tác.
  - Nguy cơ kẹt vòng lặp vô tận (Ping-Pong / Rejection loop) giữa Mason (người code) và Reviewer (người duyệt).
  - Thiếu cơ chế tự động nạp vai (Role Ingestion) cho từng công cụ CLI chuyên biệt.
- **Mục tiêu:** Xây dựng toolkit `Agents_Board` - hệ thống bảng tin cộng tác đa tác tử trên filesystem với cấu trúc thư mục Kanban, cơ chế cờ hiệu (Baton Pass), tự ngắt cầu chì (Circuit Breaker) và đồng bộ hóa vai trò tự nhiên.

## Design Principles (Nguyên tắc thiết kế / Ranh giới bảo mật)
- **Zero Heavy Dependencies:** Sử dụng Python chuẩn (Standard Library) để không phụ thuộc vào framework ngoài phức tạp, đảm bảo chạy ngay trên mọi máy tính Windows/Linux.
- **Atomic Operations:** Mọi thao tác chuyển trạng thái task đều sử dụng phép đổi tên nguyên tử (`atomic rename`), triệt tiêu race condition.
- **Strict Role Boundaries:**
  - `Mason` (Claude Code) chỉ được sửa đổi mã nguồn (`src/`, `tests/`), không được tự ý duyệt task.
  - `Reviewer` (Codex) chỉ được đánh giá, không được tự fix code; muốn từ chối phải cung cấp bằng chứng lỗi (`Proof-of-Failure`).
  - `Orchestrator` (Antigravity) nắm quyền điều phối tổng, phân rã task và phân xử tranh chấp.
- **Circuit Breaker (Ngắt cầu chì):** Giới hạn tối đa 2 lần từ chối (`reject_count >= 2`). Khi vượt ngưỡng, tự động chuyển về `05_escalation` để phân xử, chống cháy token.
- **Credential & Security Guard:** Không lưu trữ API key hoặc secret trong thư mục `.agents/`. Toàn bộ dữ liệu giao tiếp là markdown thuần túy.

## Data Models (Mô hình dữ liệu & Cấu trúc Schema)
### 1. Baton Schema (`.agents/BATON.json`)
```json
{
  "holder": "orchestrator",
  "task_id": "T01",
  "action": "planning",
  "acquired_at": "2026-10-16T05:55:00Z",
  "expires_at": null
}
```

### 2. Task Ticket Frontmatter (`.agents/0X_column/task_id.md`)
```yaml
---
id: "TASK-01"
title: "Xây dựng core authentication"
stage: "01_backlog"
assignee: "mason"
reviewer: "reviewer"
spec_ref: "00_specs/SPEC-01.md"
reject_count: 0
max_rejections: 2
created_at: "2026-10-16T05:55:00Z"
updated_at: "2026-10-16T05:55:00Z"
---
```

## Algorithm (Thuật toán chuyển giao trạng thái & Cầu chì)
```text
FUNCTION reject_task(task_id, reason, severity, test_file):
    task = read_task(task_id)
    IF severity == "NITPICK":
        log("Nitpicks do not reject tasks. Flagged as advisory.")
        RETURN APPROVE_WITH_ADVISORY
    
    task.reject_count += 1
    record_audit_log(task_id, reason, severity, test_file)
    
    IF task.reject_count >= task.max_rejections:
        move_file(task_path, ".agents/05_escalation/" + task_id + ".md")
        set_baton(holder="orchestrator", action="arbitrate", task_id=task_id)
        ring_alarm("CIRCUIT_BREAKER_TRIGGERED")
    ELSE:
        move_file(task_path, ".agents/02_in_progress/" + task_id + ".md")
        set_baton(holder=task.assignee, action="fix_bugs", task_id=task_id)
```

## Edge Cases (Xử lý trường hợp biên)
- **Deadlock khi mất Baton:** Nếu `BATON.json` bị mất hoặc corrupt, CLI `baton recover` khôi phục quyền cho `orchestrator`.
- **Concurrent Writes:** Luôn ghi vào file tạm `.tmp` rồi gọi `os.replace()` để bảo đảm tính nguyên tử (atomic rename).
- **Thiếu file Spec:** Task tạo ra mà không có file spec hợp lệ sẽ bị từ chối ngay từ khâu tạo task.
- **Kẹt review không hồi kết:** Circuit breaker giới hạn 2 lần từ chối, tự động đẩy về trọng tài.

## Setup & Operations (Thiết lập & Vận hành)
```text
+-----------------------------------------------------------------------+
|                       AGENTS BOARD KANBAN VIEW                        |
+---------------+-------------------+---------------+-------------------+
| 01_BACKLOG    | 02_IN_PROGRESS    | 03_REVIEW     | 04_DONE           |
+---------------+-------------------+---------------+-------------------+
| [TASK-02]     | [TASK-01]         |               | [TASK-00]         |
| Spec Auth     | Mason: Claude     |               | Setup Project     |
+---------------+-------------------+---------------+-------------------+
| Current Baton: [MASON (Claude Code)] -> Action: implementing TASK-01  |
+-----------------------------------------------------------------------+
```
- Khởi tạo: `python -m agents_board.init`
- Đồng bộ vai trò: `python -m agents_board.roster --sync`
- Giám sát nền: `python -m agents_board.watcher`

## Technical Decisions (Quyết định kỹ thuật)
- **Ngôn ngữ:** Python 3.10+ (Standard Library: `pathlib`, `json`, `argparse`, `sys`, `time`, `shutil`).
- **Cấu trúc dữ liệu Task:** Markdown file với YAML frontmatter chuẩn.
- **Cơ chế Baton (Gậy tiếp sức):** Tệp `.agents/BATON.json` đóng vai trò Distributed Lock / Semaphore. Chỉ agent đang giữ Baton mới được kích hoạt hành động.
- **Đồng bộ vai trò (Roster Sync):** Đọc từ `.agents/roster/*.md` để tự động render ra `CLAUDE.md`, `CODEX.md`, `AGENTS.md` tại root project.
- **Giám sát thời gian thực (Watcher):** Script Python kiểm tra thay đổi theo chu kỳ (polling nhẹ 1s trên filesystem không tốn token LLM), phát tín hiệu âm thanh và log console.

## File Change Manifest (Danh sách tệp thay đổi (Manifest))

| File Path | Action | Description |
| :--- | :--- | :--- |
| `.agents/BATON.json` | CREATE | Trạng thái gậy tiếp sức ban đầu |
| `.agents/roster/orchestrator.md` | CREATE | Đặc tả vai trò Orchestrator (Antigravity) |
| `.agents/roster/mason.md` | CREATE | Đặc tả vai trò Mason (Claude Code) |
| `.agents/roster/reviewer.md` | CREATE | Đặc tả vai trò Reviewer (Codex) |
| `agents_board/__init__.py` | CREATE | Module init cho Agents_Board |
| `agents_board/init.py` | CREATE | Lệnh tạo cấu trúc thư mục pipeline và template ban đầu |
| `agents_board/baton.py` | CREATE | CLI quản lý cấp phát và chuyển giao Baton |
| `agents_board/task.py` | CREATE | CLI quản lý vòng đời task và ngắt cầu chì |
| `agents_board/roster.py` | CREATE | CLI đồng bộ vai trò thành file hướng dẫn cho từng agent |
| `agents_board/watcher.py` | CREATE | Daemon giám sát bảng tin và thông báo sự kiện |
| `template_task.md` | CREATE | Mẫu chuẩn cho một task ticket |
| `README.md` | CREATE | Tài liệu hướng dẫn sử dụng nhanh và quy trình vận hành |
| `tests/test_agents_board.py` | CREATE | Bộ kiểm thử tự động cho toàn bộ core module |

## Verification Criteria (Tiêu chí nghiệm thu)

| ID | Category | Command/Test Scenario | Expected Outcome |
| :--- | :--- | :--- | :--- |
| VC-01 | Initialization | `python -m agents_board.init` | Full `.agents/` structure (00 to 05) created cleanly |
| VC-02 | Baton Management | `python -m agents_board.baton pass mason` | `BATON.json` updated with holder='mason', verified via `status` |
| VC-03 | Task Lifecycle | Create task -> move to in_progress -> move to review | Task file moves atomically across columns |
| VC-04 | Circuit Breaker | Reject task 2 times with severity `BLOCKER` | Task moves to `05_escalation/`, alert triggered |
| VC-05 | Roster Sync | `python -m agents_board.roster --sync` | `CLAUDE.md`, `CODEX.md`, `AGENTS.md` generated at root |
| VC-06 | Unit Test Suite | `python -m unittest tests/test_agents_board.py` | 100% tests pass cleanly |

