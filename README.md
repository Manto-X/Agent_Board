# Agent Board 🧭

> **Zero-API, File-Based Multi-Agent Blackboard with Relay Baton Protocol.**  
> *Điều phối Claude Code, OpenAI Codex, và Antigravity trên một bảng tin chung — Không tốn phí API, không tranh nhau ghi file.*

[🇻🇳 Tiếng Việt](#-tiếng-việt) | [🇬🇧 English](#-english)

---

# 🇻🇳 Tiếng Việt

> **Có bao giờ anh em bực mình vì đã bỏ tiền túi mua đủ món đồ chơi xịn (ChatGPT, Claude, Gemini) về làm việc, nhưng rốt cuộc cả ngày mình vẫn phải làm shipper: cặm cụi copy từng đoạn chữ từ tab này đem sang dán vào tab kia? Đã thế, hễ để mấy đứa cùng mó tay vào một chỗ là đứa này tiện tay xóa sạch bài của đứa khác!**

**Agent Board** đẻ ra để trị dứt điểm cái cảnh lắt nhắt đó cho anh em.

---

### 💡 Nó chạy kiểu gì? (Giải thích dễ hiểu như chuyện con nít)

Tưởng tượng trong nhà anh em có một **Cái bảng dán giấy nhớ trên cánh tủ lạnh**, kèm thêm **Một cây gậy chuyền tay (Relay Baton)**:

1. **Cái bảng dán giấy nhớ:** Trên cánh tủ lạnh chia sẵn các ngăn:
   - *Việc cần làm* (`01_backlog`) ➔ *Đang làm* (`02_in_progress`) ➔ *Chờ soi lỗi* (`03_review`) ➔ *Xong xuôi* (`04_done`).
2. **Cây gậy chuyền tay (`BATON.json`):** Cả nhà chỉ có đúng **một cây gậy duy nhất**. Đứa nào ôm gậy thì đứa đó mới được ngồi vào bàn làm việc. Làm xong phần mình thì tự tay bóc tờ giấy dán sang ngăn kế bên, rồi chuyền gậy cho đứa tiếp theo. Tuyệt đối không có chuyện hai ba đứa xông vào tranh nhau một mẩu giấy hay giẫm chân lên nhau.
3. **Chuông réo phụ huynh (Cầu chì tự ngắt):** Nếu đứa soi lỗi bắt đứa làm bài sửa đi sửa lại quá 2 lần, chuông sẽ réo ầm lên để mời anh em (chủ nhà) vào đập bàn phân xử tại `05_escalation`, dẹp ngay trò cãi cùn lòng vòng.

Đơn giản vậy thôi: Mấy đứa đệ tự nhìn bảng tủ lạnh, tự chuyền gậy cho nhau cày việc từ đầu đến đuôi. Anh em rảnh tay đi pha cốc cà phê uống, khỏi cần nhấc tay copy-paste lấy một lần!

---

## 💎 Điểm độc đáo của Agent Board (So với các repo khác trên mạng)

| Tiêu chí | Các công cụ khác | **Agent Board** 🧭 |
| :--- | :--- | :--- |
| **Cài đặt** | Cài Node.js, Docker, Electron, hoặc cả chục thư viện pip nặng nề. | **Zero-Install:** 100% Python Standard Library có sẵn trong máy. Tải về là chạy ngay. |
| **Chi phí dùng AI** | Bắt mua API key trả tiền theo lượt (đốt token cực xót ruột). | **0 đồng phí phát sinh:** Tận dụng 100% tài khoản ChatGPT, Claude, Gemini đã mua hàng tháng. |
| **Cầm trịch chống đè code** | Dùng Git worktrees phức tạp hoặc dễ xung đột ghi đè. | **Gậy tiếp sức (`BATON.json`):** Đứa nào cầm gậy đứa đó mới được thao tác. Triệt tiêu race condition. |
| **Chống kẹt vòng lặp** | Thợ code và người kiểm tra cãi nhau lòng vòng vô tận (Ping-Pong). | **Cầu chì 2 hiệp:** Bị từ chối 2 lần là tự ngắt ngay, réo chuông mời anh em vào phân xử. |
| **Đổi vai trò** | Gắn chết vai hoặc phải sửa mã nguồn lằng nhằng. | **1 dòng lệnh đổi vai:** Thích cho Claude lập kế hoạch hay Gemini viết code chỉ mất 3 giây. |
| **Sạch sẽ thư mục** | Xâm lấn bừa bãi ra thư mục gốc dự án. | **Gọn gàng tuyệt đối:** 100% đồ nghề AI giấu kín trong `.agents/`, trả lại không gian sạch cho dự án. |

---

## 🚀 Cài đặt trong 1 nốt nhạc (1 Dòng lệnh duy nhất)

Chạy ngay dòng lệnh này tại thư mục dự án của anh em:

* **Windows PowerShell:**
  ```powershell
  irm https://raw.githubusercontent.com/Manto-X/Agent_Board/main/get_board.py | python
  ```

* **Linux / macOS:**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Manto-X/Agent_Board/main/get_board.py | python3
  ```

---

## ⚡ Bộ lệnh thao tác nhanh (Quick Cheat Sheet)

Tất cả lệnh chạy qua **1 cửa ngõ duy nhất** `python .agents/board.py`:

```bash
# 📋 Bảng việc (Kanban)
python .agents/board.py task list                      # Xem toàn bộ bảng việc
python .agents/board.py task create --id T01 --title "X" # Tạo việc mới vào Backlog
python .agents/board.py task move T01 in_progress      # Nhận việc vào làm
python .agents/board.py task move T01 review           # Nộp bài đi soi
python .agents/board.py task move T01 done             # Nghiệm thu hoàn tất
python .agents/board.py task reject T01 --reason "Lỗi" # Bắt làm lại (kèm test case)

# 🏃 Gậy tiếp sức (Baton)
python .agents/board.py baton status                   # Xem ai đang giữ gậy
python .agents/board.py baton pass mason --task-id T01 # Chuyền cho thợ code
python .agents/board.py baton pass reviewer            # Chuyền cho thợ soi
python .agents/board.py baton recover                  # Cứu hộ giành lại gậy khẩn cấp

# 🎭 Phân vai & Trọng tài
python .agents/board.py roster --orchestrator claude --mason antigravity --reviewer codex # Đổi vai
python .agents/board.py watch                          # Bật chuông theo dõi bảng việc
```

---

## 📚 Tài liệu chi tiết (Detailed Documentation)
- 📐 [Kiến trúc & Cơ chế gậy Baton](docs/ARCHITECTURE.md)
- 🔄 [Quy trình phối hợp thực chiến 4 bước](docs/WORKFLOW.md)
- 📖 [Bảng tra cứu toàn bộ lệnh CLI](docs/CLI_REFERENCE.md)

---

> 💡 **Lời nhắn gửi:** Agent Board chủ động giữ vững triết lý kiến trúc tối giản nhất trong việc kết nối, giao tiếp và phân việc giữa các AI. Anh chị em toàn quyền tự do nâng cấp, mở rộng lên các mức độ cao hơn (custom hooks, dynamic dispatcher, automated git worktrees, web dashboard...) để phục vụ tối đa nhu cầu cá nhân của bản thân.

---
---

# 🇬🇧 English

> **Tired of paying for premium desktop AI subscriptions (ChatGPT, Claude, Gemini) only to spend your day playing digital courier—copy-pasting text between browser tabs, or watching multiple agents accidentally overwrite each other's code?**

**Agent Board** is designed to solve this once and for all.

---

### 💡 How It Works: The Fridge Note & Relay Baton Metaphor

Imagine your development workflow as a **family refrigerator bulletin board** with a single **relay baton**:

1. **The Refrigerator Bulletin Board:** The fridge door is organized into Kanban columns:
   - *Backlog* (`01_backlog`) ➔ *In Progress* (`02_in_progress`) ➔ *Under Review* (`03_review`) ➔ *Done* (`04_done`).
2. **The Relay Baton (`BATON.json`):** There is only **one baton**. Only the agent holding the baton has permission to read the task, modify code, or commit. When done, it moves the sticky note to the next column and hands the baton over. No collisions, no overwrites.
3. **The Parent's Alarm (Circuit Breaker):** If the reviewer rejects the coder's work twice, an alarm sounds (`05_escalation`). The human lead steps in to arbitrate, killing endless ping-pong debates instantly.

Your desktop AI models coordinate through the local filesystem. You sip your coffee without copy-pasting a single line.

---

## 💎 Why Agent Board Stands Out

| Feature | Typical Multi-Agent Tools | **Agent Board** 🧭 |
| :--- | :--- | :--- |
| **Installation** | Heavy setups: Node.js, Docker, Electron, or bulky pip packages. | **Zero-Install:** 100% Python Standard Library. Clone and run immediately. |
| **Token Cost** | Pay-per-token API calls (costs multiply rapidly). | **$0 Extra Cost:** Uses 100% of your flat-rate Claude Code, ChatGPT, and Gemini desktop subs. |
| **Race Condition Guard** | Complex Git worktrees or chaotic concurrent overwrites. | **Relay Baton (`BATON.json`):** Strict single-holder lock. Eliminates file conflicts. |
| **Anti-Deadlock** | Coders and reviewers get stuck in infinite ping-pong loops. | **2-Strike Circuit Breaker:** Auto-halts on 2 rejections and alerts human lead. |
| **Role Reassignment** | Hardcoded personas or messy prompt edits. | **1-Line Role Swap:** Switch planner, coder, and auditor roles in 3 seconds. |
| **Clean Workspace** | Clutters root directories with framework junk. | **Isolated Sandbox:** 100% of AI coordination logic is confined inside `.agents/`. |

---

## 🚀 1-Line Quick Installation

Run this directly inside your project directory:

* **Windows PowerShell:**
  ```powershell
  irm https://raw.githubusercontent.com/Manto-X/Agent_Board/main/get_board.py | python
  ```

* **Linux / macOS:**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Manto-X/Agent_Board/main/get_board.py | python3
  ```

---

## ⚡ Quick Cheat Sheet

All operations run through a single CLI: `python .agents/board.py`:

```bash
# 📋 Task Management
python .agents/board.py task list                      # View complete Kanban board
python .agents/board.py task create --id T01 --title "X" # Create new task in Backlog
python .agents/board.py task move T01 in_progress      # Claim task
python .agents/board.py task move T01 review           # Submit for review
python .agents/board.py task move T01 done             # Approve and complete
python .agents/board.py task reject T01 --reason "Bug" # Reject with test proof

# 🏃 Relay Baton Management
python .agents/board.py baton status                   # Inspect current baton holder
python .agents/board.py baton pass mason --task-id T01 # Pass baton to coder
python .agents/board.py baton pass reviewer            # Pass baton to reviewer
python .agents/board.py baton recover                  # Emergency token recovery

# 🎭 Roster & Watcher
python .agents/board.py roster --orchestrator claude --mason antigravity --reviewer codex # Swap roles
python .agents/board.py watch                          # Run background audible event watcher
```

---

## 📚 Deep Dive Documentation
- 📐 [Architecture & Relay Baton Protocol](docs/ARCHITECTURE.md)
- 🔄 [4-Phase Practical Collaboration Workflow](docs/WORKFLOW.md)
- 📖 [Complete CLI Command Reference](docs/CLI_REFERENCE.md)

---

> 💡 **Philosophy Note:** Agent Board deliberately embraces a minimalist architecture philosophy for inter-agent communication and task coordination. You are fully empowered to fork, extend, and level it up (custom hooks, dynamic dispatchers, web dashboards, automated git worktrees...) to best fit your personal workflows.
