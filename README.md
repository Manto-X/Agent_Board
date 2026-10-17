# Agents_Board 🧭

> **Bảng tin điều phối đa tác tử (Multi-Agent Blackboard System) cho Filesystem.**  
> Kết nối độc lập **Claude Code**, **OpenAI Codex**, và **Antigravity / Gemini** qua các cửa sổ làm việc mà không tốn phí Multi-Agent API framework.

---

## 🎯 Triết lý & Thiết kế cốt lõi

1. **Zero-Install & Zero-Dependency:** 100% Python Standard Library (3.10+). Không cần `pip install`, không tốn chi phí framework (AutoGen/CrewAI).
2. **Cách ly tuyệt đối (Workspace Isolation):** Toàn bộ bộ máy của AIs nằm trọn trong thư mục `.agents/`. Root project hoàn toàn sạch bóng để dành cho mã nguồn (`src/`), bài test (`tests/`) và kịch bản (`scripts/`) của người dùng.
3. **Lệnh ngắn dễ nhớ (Short Dispatcher):** Thao tác nhanh qua `python .agents/board.py <cmd>`.
4. **Ma trận phân vai linh hoạt (Dynamic Role Matrix):** Tự do tráo đổi vai trò giữa các AI (ví dụ: Claude làm Orchestrator, Antigravity làm Mason, Codex làm Reviewer).
5. **Gậy tiếp sức (Baton Pass) & Cầu chì (Circuit Breaker):** Kiểm soát chống race condition và tự ngắt sang `05_escalation` khi task bị reject quá 2 lần.

---

## 🚀 Khởi động nhanh (Quick Start)

### Kịch bản 1: Kéo Starter Kit vào dự án có sẵn (1 Dòng lệnh)

Chạy trực tiếp từ terminal tại thư mục dự án của bạn:

* **Windows PowerShell:**
  ```powershell
  irm https://raw.githubusercontent.com/tomyxo/Agents_Board/main/get_board.py | python
  ```
* **Linux / macOS:**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/tomyxo/Agents_Board/main/get_board.py | python3
  ```

### Kịch bản 2: Dự án mới từ đầu
Dùng tính năng **"Use this template"** trên GitHub repo hoặc clone về máy:
```bash
git clone https://github.com/tomyxo/Agents_Board.git my-project
cd my-project
python .agents/board.py init
```

---

## 🎭 Tùy biến Vai trò (Dynamic Roles)

Mặc định: `Antigravity` = Orchestrator, `Claude` = Mason, `Codex` = Reviewer.  
Bạn có thể tráo đổi bất kỳ lúc nào:

```bash
# Cho Claude lập kế hoạch, Antigravity viết code, Codex review:
python .agents/board.py roster --orchestrator claude --mason antigravity --reviewer codex
```
Lệnh trên sẽ tự động nạp vai trò tương ứng vào [CLAUDE.md](file:///e:/gDrive/03_Lab/Agents_Board/CLAUDE.md), [AGENTS.md](file:///e:/gDrive/03_Lab/Agents_Board/AGENTS.md), [CODEX.md](file:///e:/gDrive/03_Lab/Agents_Board/CODEX.md).

---

## 🛠️ Bộ lệnh điều phối (Cheat Sheet)

### 🏃 Quản lý Gậy tiếp sức (Baton)
```bash
# Xem ai đang cầm gậy
python .agents/board.py baton status

# Chuyển gậy cho Mason làm việc
python .agents/board.py baton pass mason --task-id TASK-01

# Chuyển gậy cho Reviewer thẩm định
python .agents/board.py baton pass reviewer --task-id TASK-01

# Khôi phục gậy về cho Orchestrator (khẩn cấp)
python .agents/board.py baton recover
```

### 📋 Quản lý Task & Vòng đời
```bash
# 1. Xem danh sách bảng Kanban
python .agents/board.py task list

# 2. Tạo task mới
python .agents/board.py task create --id TASK-01 --title "Xây dựng Auth Module" --assignee mason --reviewer reviewer

# 3. Chuyển trạng thái task
python .agents/board.py task move TASK-01 in_progress
python .agents/board.py task move TASK-01 review
python .agents/board.py task move TASK-01 done

# 4. Reviewer từ chối (REJECT) kèm lý do
python .agents/board.py task reject TASK-01 --reason "Tạch unit test biên null" --severity BLOCKER --test-file "tests/test_auth.py"
```

### 🔔 Bật Trọng tài giám sát (Watcher Daemon)
Chạy ở 1 tab terminal riêng (0% CPU, 0 token LLM):
```bash
python .agents/board.py watch
```

---

## 🧪 Kiểm thử (Unit Tests)

```bash
python -m unittest tests/test_agents_board.py
```
100% tests pass bằng Python Standard Library.
