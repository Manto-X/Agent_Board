# Sổ tay Vận hành Dành cho Human (Operator Guide)
# Human Operator Guide — Managing Your Multi-Agent Board

> **Dành riêng cho Bạn (Human / Developer):** Tài liệu này giúp bạn nắm quyền kiểm soát cỗ máy đa tác tử trong dự án, hiểu vai trò các file ngoài root và biết phải làm gì tiếp theo.
> **Bilingual convention:** Tiếng Việt ở trên, English version below.

---

# [VI] HƯỚNG DẪN DÀNH CHO CON NGƯỜI (HUMAN)

Chào bạn! Khi bạn chạy lệnh cài đặt Agent Board vào dự án, bạn sẽ thấy xuất hiện:
*   **4 tệp chỉ dẫn ngoài thư mục gốc (Root):**
    *   `MANUAL.md` *(Tệp bạn đang đọc)*: Chỉ dẫn riêng cho **Con người (Human)**.
    *   `AGENTS.md`: Chỉ dẫn luật chơi cho **Antigravity / Gemini** (Đóng vai Orchestrator).
    *   `CLAUDE.md`: Chỉ dẫn luật chơi cho **Claude Code** (Đóng vai Mason - Thợ code).
    *   `CODEX.md`: Chỉ dẫn luật chơi cho **OpenAI Codex** (Đóng vai Reviewer - Thợ soi).
*   **1 thư mục duy nhất `.agents/`:**
    *   Toàn bộ mã nguồn, cỗ máy điều phối, gậy tiếp sức và các ngăn việc đều giấu kín trong `.agents/` để **giữ cho dự án của bạn sạch sẽ 100%**.

---

## 1. Chuyện gì đang diễn ra ở đây?

Dự án của bạn vừa có thêm một **dây chuyền làm việc tự động của 3 trợ lý AI**. Chúng sẽ tự đọc task, tự chuyền gậy và tự nghiệm thu code với nhau qua thư mục `.agents/`.

### Bản đồ 6 ngăn việc trong `.agents/`:
*   📁 `.agents/00_specs/`: Tài liệu đặc tả kỹ thuật do AI lập kế hoạch viết.
*   📁 `.agents/01_backlog/`: Việc đang chờ làm (file markdown).
*   📁 `.agents/02_in_progress/`: Việc Thợ Code (Claude Code) đang viết.
*   📁 `.agents/03_review/`: Code đang chờ Thợ Soi (Codex) thẩm định.
*   📁 `.agents/04_done/`: Việc đã xong, test pass 100%.
*   📁 `.agents/05_escalation/`: Nơi chứa việc cãi nhau quá 2 lần, chờ bạn vào phân xử.

### Cây gậy tiếp sức (`BATON.json`):
Cả xưởng chỉ có đúng **một cây gậy duy nhất** (`.agents/BATON.json`). AI nào cầm gậy mới được thao tác, đứa khác phải ngồi chờ. Cơ chế này đảm bảo **không bao giờ có chuyện 2 con AI cùng nhảy vào sửa một file gây đè code nhau**.

---

## 2. Bước tiếp theo: Bạn cần làm gì?

Bạn chỉ cần thực hiện đúng **3 bước đơn giản** sau:

### 👉 Bước 1: Ra lệnh cho AI Lập kế hoạch (Antigravity / Gemini)
Mở Antigravity hoặc Gemini lên, chat với nó một câu:
> *"Tao muốn làm tính năng [Mô tả tính năng, ví dụ: Authentication bằng JWT]. Mày hãy lên spec chi tiết vào `.agents/00_specs/`, tạo task vào `.agents/` và trao gậy cho Mason đi."*

*Nhờ file `AGENTS.md`, AI sẽ tự động tạo task và chuyền gậy cho Claude Code.*

---

### 👉 Bước 2: Bật Thợ Code (Claude Code)
Mở một tab terminal khác, gõ:
```bash
claude
```
Và chat: *"Kiểm tra bảng việc và thực hiện task được giao."*

*Claude Code đọc `CLAUDE.md`, thấy gậy đang ở tay mình, sẽ tự nhận việc sang `in_progress`, viết code + tests, rồi tự nộp sang `review` và chuyền gậy cho Codex.*

---

### 👉 Bước 3: Kiểm tra tiến độ (Khi bạn muốn xem)
Bất cứ lúc nào, bạn chỉ cần gõ:
```bash
# Xem ai đang làm gì, việc nào xong rồi:
python .agents/board.py task list

# Xem gậy đang ở tay ai:
python .agents/board.py baton status

# (Tùy chọn) Bật chuông theo dõi ở 1 tab riêng:
python .agents/board.py watch
```

---

## 3. Khi nào bạn cần can thiệp?

Chỉ khi **chuông réo báo động** (Task bị Reviewer từ chối 2 lần vì lỗi nghiêm trọng):
*   Task sẽ tự động văng vào `.agents/05_escalation/`.
*   Bạn mở file task đó ra xem lý do cãi nhau và quyết định:
    *   **Ép duyệt (nếu thấy bắt bẻ quá đà):** `python .agents/board.py task move <ID> done`
    *   **Giành lại gậy để tự code:** `python .agents/board.py baton recover`

---
---

# [EN] HUMAN OPERATOR GUIDE

Welcome! When you install Agent Board into your repository, you will find:
*   **4 Instruction files in the project root:**
    *   `MANUAL.md` *(The file you are reading)*: Dedicated guide for **Human Developers**.
    *   `AGENTS.md`: Instruction manual for **Antigravity / Gemini** (Orchestrator).
    *   `CLAUDE.md`: Instruction manual for **Claude Code** (Mason - Coder).
    *   `CODEX.md`: Instruction manual for **OpenAI Codex** (Reviewer - Auditor).
*   **1 Isolated engine folder `.agents/`:**
    *   All runtime code, task queues, and baton tokens live inside `.agents/` to **keep your project root clean**.

---

## 1. What Is Happening Here?

Your project now has an **autonomous assembly line of 3 AI assistants**. They communicate, coordinate, and review code via `.agents/`.

### The 6 Kanban Columns inside `.agents/`:
*   📁 `.agents/00_specs/`: Technical blueprints drafted by the Planner.
*   📁 `.agents/01_backlog/`: Queued tasks waiting for implementation.
*   📁 `.agents/02_in_progress/`: Active tasks claimed by Claude Code.
*   📁 `.agents/03_review/`: Code awaiting audit by Codex.
*   📁 `.agents/04_done/`: Fully verified, completed tasks.
*   📁 `.agents/05_escalation/`: Deadlocked tasks awaiting human arbitration.

### The Relay Baton (`BATON.json`):
Located at `.agents/BATON.json`, this is a **turn-based lock**. Only the active token holder may edit files, completely preventing race conditions.

---

## 2. Next Steps: What Should You Do?

Just follow these **3 simple steps**:

### 👉 Step 1: Instruct the Planner (Antigravity / Gemini)
Open Antigravity or Gemini and say:
> *"I want to build [Feature Description, e.g. JWT Authentication]. Draft the spec in `.agents/00_specs/`, decompose it into tasks via `board.py task create`, and pass the baton to Mason."*

---

### 👉 Step 2: Launch the Coder (Claude Code)
Open a new terminal tab, run:
```bash
claude
```
And say: *"Check the board and implement your assigned task."*

---

### 👉 Step 3: Monitor Progress
At any time from your project root:
```bash
# View Kanban board:
python .agents/board.py task list

# Check who holds the baton:
python .agents/board.py baton status

# Run background audible watcher:
python .agents/board.py watch
```
