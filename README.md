# Agents_Board 🧭

> **Bảng tin điều phối đa tác tử (Multi-Agent Blackboard System) trên Filesystem.**
> Kết nối độc lập **Claude Code**, **OpenAI Codex**, và **Antigravity / Gemini** qua các cửa sổ làm việc mà không tốn phí Multi-Agent API framework.

---

## 🎯 Ý tưởng & Triết lý cốt lõi

1. **Zero Multi-Agent API Overhead:** Tận dụng 100% gói thuê bao phẳng (flat-rate sub) sẵn có của các CLI/IDE (Claude Code, ChatGPT/Codex, Antigravity) thay vì đốt token theo lượt qua CrewAI/AutoGen.
2. **Blackboard Pattern (Bảng tin chung):** Thư mục `.agents/` là nguồn sự thật duy nhất (Single Source of Truth) theo dõi tiến độ, task và spec.
3. **Gậy tiếp sức (Baton Pass / Semaphore):** File `.agents/BATON.json` kiểm soát ai là người được quyền hành động, triệt tiêu race condition.
4. **Cầu chì tự ngắt (Circuit Breaker):** Giới hạn tối đa 2 lần từ chối (`reject_count >= 2`). Chống kẹt vòng lặp bóng bàn giữa Mason và Reviewer.
5. **Đồng bộ vai trò tự nhiên (Natural Role Ingestion):** Tự sinh `CLAUDE.md`, `CODEX.md`, `AGENTS.md` từ `.agents/roster/` để mỗi agent tự động nhận vai khi khởi động.

---

## 📂 Cấu trúc thư mục `.agents/`

```text
.agents/
├── 00_specs/          # Hồ sơ yêu cầu, PRD, tài liệu kiến trúc do Orchestrator tạo
├── 01_backlog/        # Danh sách task chờ làm (dạng Markdown + Frontmatter)
├── 02_in_progress/    # Task đang được Mason thực thi
├── 03_review/         # Task đang chờ Reviewer thẩm định
├── 04_done/           # Task đã hoàn thành và nghiệm thu
├── 05_escalation/     # Task bị kẹt sau 2 lần từ chối -> chờ phán quyết
├── roster/            # Hồ sơ phân vai (orchestrator.md, mason.md, reviewer.md)
└── BATON.json         # Token gậy tiếp sức thời gian thực
```

---

## 🚀 Hướng dẫn sử dụng nhanh (Quick Start)

### 1. Khởi tạo Agents_Board
Trong thư mục dự án bất kỳ:
```bash
python -m agents_board.init
```
Lệnh này sẽ tự sinh cấu trúc `.agents/`, bộ vai trò mẫu, template task và các file `CLAUDE.md`, `CODEX.md`, `AGENTS.md`.

### 2. Bật Trọng tài giám sát (Watcher Daemon)
Chạy script này ở một tab terminal riêng (chỉ tốn 0% CPU, 0 LLM token):
```bash
python -m agents_board.watcher
```
Watcher sẽ lắng nghe sự kiện, phát chuông (beep) và in log đổi trạng thái thời gian thực.

---

## 🛠️ Bộ lệnh CLI (Cheat Sheet)

### 🏃 Quản lý Gậy tiếp sức (Baton)
```bash
# Xem ai đang cầm gậy
python -m agents_board.baton status

# Chuyển gậy cho Mason
python -m agents_board.baton pass mason --task-id TASK-01 --action "implementing"

# Chuyển gậy cho Reviewer
python -m agents_board.baton pass reviewer --task-id TASK-01 --action "reviewing"

# Khôi phục gậy về cho Orchestrator (khi khẩn cấp)
python -m agents_board.baton recover
```

### 📋 Quản lý Task & Vòng đời
```bash
# 1. Tạo task mới vào backlog
python -m agents_board.task create --id TASK-01 --title "Xây dựng Auth Module" --assignee mason --reviewer reviewer

# 2. Xem toàn cảnh bảng Kanban
python -m agents_board.task list

# 3. Chuyển task sang đang làm (in_progress)
python -m agents_board.task move TASK-01 in_progress

# 4. Mason code xong, chuyển sang review
python -m agents_board.task move TASK-01 review
python -m agents_board.baton pass reviewer --task-id TASK-01

# 5. Reviewer duyệt PASS -> chuyển sang done
python -m agents_board.task move TASK-01 done
python -m agents_board.baton pass orchestrator

# 6. Reviewer từ chối (REJECT)
# Lưu ý: Bắt buộc chỉ rõ lý do và độ nghiêm trọng
python -m agents_board.task reject TASK-01 --reason "Tạch unit test biên null" --severity BLOCKER --test-file "tests/test_auth.py"
```

> **Cơ chế Cầu chì (Circuit Breaker):**
> - Lần từ chối 1 (`reject_count = 1`): Task tự động quay về `02_in_progress`, gậy chuyển về `mason` để fix.
> - Lần từ chối 2 (`reject_count = 2`): Cầu chì ngắt, task tự động nhảy sang `05_escalation/`, gậy chuyển về `orchestrator` hoặc Sếp để phân xử!

### 🎭 Đồng bộ vai trò (Roster Sync)
Sau khi chỉnh sửa các tiêu chuẩn trong `.agents/roster/*.md`:
```bash
python -m agents_board.roster --sync
```

---

## 🧪 Chạy Kiểm thử (Unit Tests)

```bash
python -m unittest tests/test_agents_board.py
```
Kiểm thử 100% các luồng: Khởi tạo, luân chuyển task, từ chối NITPICK vs BLOCKER, và ngắt cầu chì tự động.
