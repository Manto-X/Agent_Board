# Agent Board — CLI Command Reference
# Bảng Tra Cứu Toàn Bộ Lệnh CLI

> **Quy ước song ngữ:** Phần Tiếng Việt ở trên, phần English version ở dưới.
> **Bilingual convention:** Vietnamese version first, English version below.

---

# [VI] TRA CỨU LỆNH CLI (`python .agents/board.py`)

Toàn bộ thao tác với Agent Board đều qua một điểm vào duy nhất: `python .agents/board.py <lệnh>`:

## 1. Nhóm lệnh Quản lý Task (`task`)

| Lệnh | Cú pháp | Mô tả |
| :--- | :--- | :--- |
| **Xem bảng việc** | `python .agents/board.py task list` | In toàn cảnh bảng Kanban qua 6 cột trạng thái. |
| **Tạo việc mới** | `python .agents/board.py task create --id <ID> --title "<TIÊU_ĐỀ>" [--assignee mason] [--reviewer reviewer] [--spec <ĐƯỜNG_DẪN>]` | Tạo task markdown với YAML frontmatter trong `01_backlog`. |
| **Chuyển trạng thái** | `python .agents/board.py task move <ID> <CỘT>` | Di chuyển task nguyên tử (`in_progress`, `review`, `done`, `escalation`). |
| **Từ chối task** | `python .agents/board.py task reject <ID> --reason "<LÝ_DO>" [--severity BLOCKER\|MAJOR\|NITPICK] [--test-file <PATH>]` | Từ chối task. `NITPICK` không từ chối; `BLOCKER` tăng reject_count; chạm ngưỡng 2 lần tự ngắt cầu chì sang `05_escalation`. |
| **Xem chi tiết task** | `python .agents/board.py task show <ID>` | In toàn bộ metadata và nội dung task. |

---

## 2. Nhóm lệnh Cây gậy tiếp sức (`baton`)

| Lệnh | Cú pháp | Mô tả |
| :--- | :--- | :--- |
| **Xem ai giữ gậy** | `python .agents/board.py baton status` | Hiển thị agent đang giữ quyền hành động, task liên quan và thời gian. |
| **Chuyền gậy** | `python .agents/board.py baton pass <AGENT> [--task-id <ID>] [--action <HÀNH_ĐỘNG>]` | Chuyển quyền hành động cho agent khác (`mason`, `reviewer`, `orchestrator`). |
| **Nhận gậy** | `python .agents/board.py baton acquire <AGENT> [--task-id <ID>]` | Tự nhận gậy vào phiên làm việc. |
| **Cứu hộ gậy** | `python .agents/board.py baton recover` | Khôi phục quyền kiểm soát về cho `orchestrator` khi có agent bị kẹt. |

---

## 3. Nhóm lệnh Phân vai & Trọng tài (`roster`, `watch`)

| Lệnh | Cú pháp | Mô tả |
| :--- | :--- | :--- |
| **Đổi ma trận vai** | `python .agents/board.py roster --orchestrator <A> --mason <B> --reviewer <C>` | Tráo đổi vai trò giữa các AI và tự động nạp vào file cấu hình. |
| **Đồng bộ vai trò** | `python .agents/board.py roster --sync` | Đọc `.agents/roster/` và cập nhật lại `CLAUDE.md`, `CODEX.md`, `AGENTS.md`. |
| **Bật trọng tài** | `python .agents/board.py watch [--interval 1.0] [--once]` | Chạy daemon giám sát bảng tin nền, phát chuông báo khi có sự kiện. |

---
---

# [EN] CLI COMMAND REFERENCE (`python .agents/board.py`)

All interactions with Agent Board run through a single entry point: `python .agents/board.py <subcommand>`:

## 1. Task Management (`task`)

| Subcommand | Syntax | Description |
| :--- | :--- | :--- |
| **List Board** | `python .agents/board.py task list` | Displays Kanban board across all 6 columns. |
| **Create Task** | `python .agents/board.py task create --id <ID> --title "<TITLE>" [--assignee mason] [--reviewer reviewer] [--spec <PATH>]` | Generates a new task ticket with YAML frontmatter in `01_backlog`. |
| **Transition Task** | `python .agents/board.py task move <ID> <STAGE>` | Atomically moves ticket (`in_progress`, `review`, `done`, `escalation`). |
| **Reject Task** | `python .agents/board.py task reject <ID> --reason "<REASON>" [--severity BLOCKER\|MAJOR\|NITPICK] [--test-file <PATH>]` | Submits structured critique. `NITPICK` is advisory; `BLOCKER` increments strikes; 2 strikes trips circuit breaker to `05_escalation`. |
| **Show Task** | `python .agents/board.py task show <ID>` | Prints task metadata and audit history. |

---

## 2. Relay Baton Management (`baton`)

| Subcommand | Syntax | Description |
| :--- | :--- | :--- |
| **Check Status** | `python .agents/board.py baton status` | Inspects current active token holder, task association, and timestamp. |
| **Pass Baton** | `python .agents/board.py baton pass <AGENT> [--task-id <ID>] [--action <ACTION>]` | Transfers active execution token (`mason`, `reviewer`, `orchestrator`). |
| **Acquire Baton** | `python .agents/board.py baton acquire <AGENT> [--task-id <ID>]` | Claims baton token for current agent session. |
| **Emergency Recovery** | `python .agents/board.py baton recover` | Resets token possession to `orchestrator` if an agent deadlocks. |

---

## 3. Roster & Monitoring (`roster`, `watch`)

| Subcommand | Syntax | Description |
| :--- | :--- | :--- |
| **Reassign Roles** | `python .agents/board.py roster --orchestrator <A> --mason <B> --reviewer <C>` | Dynamically swaps roles across models and refreshes agent instructions. |
| **Sync Instructions** | `python .agents/board.py roster --sync` | Compiles `.agents/roster/` into `CLAUDE.md`, `CODEX.md`, and `AGENTS.md`. |
| **Event Watcher** | `python .agents/board.py watch [--interval 1.0] [--once]` | Lightweight background listener sounding audible alerts on transitions. |
