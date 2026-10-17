# Sổ tay Vận hành Dành cho Human (Operator Guide)
# Human Operator Guide — Managing Your Multi-Agent Board

> **Dành riêng cho Bạn (Human / Developer):** Tài liệu này giúp bạn hiểu chuyện gì đang diễn ra trong dự án và cách làm chủ cỗ máy đa tác tử mà không cần tốn công copy-paste.
> **Bilingual convention:** Tiếng Việt ở trên, English version below.

---

# [VI] HƯỚNG DẪN DÀNH CHO CON NGƯỜI (HUMAN)

Chào bạn, người chủ dự án! Khi bạn kéo `Agent Board` về máy, thư mục dự án của bạn đã trở thành một **xưởng làm việc tự động của 3 trợ lý AI**.

---

## 1. Chuyện gì đang diễn ra trong thư mục của bạn?

Thay vì bạn phải làm "shipper" copy từng đoạn code giữa các tab trình duyệt, 3 trợ lý AI của bạn (Claude Code, OpenAI Codex, Antigravity/Gemini) sẽ **tự nhìn vào thư mục `.agents/` để nói chuyện, giao việc và nghiệm thu code với nhau**.

### Bản đồ 6 ngăn tủ lạnh trên máy bạn:
*   📁 `.agents/00_specs/`: Nơi chứa tài liệu kiến trúc, đặc tả tính năng do AI lập kế hoạch viết.
*   📁 `.agents/01_backlog/`: Hàng chờ các việc cần làm (mỗi việc là 1 file `.md`).
*   📁 `.agents/02_in_progress/`: Việc mà Thợ Code (Claude Code) đang nhận làm.
*   📁 `.agents/03_review/`: Code đã viết xong, đang nộp cho Thợ Soi (Codex) kiểm tra.
*   📁 `.agents/04_done/`: Việc đã kiểm thử đạt 100%, chính thức hoàn tất.
*   📁 `.agents/05_escalation/`: Nơi chứa việc bị cãi nhau quá 2 lần, chờ bạn vào đập bàn phân xử.

### Cây gậy tiếp sức (`BATON.json`):
Trong thư mục `.agents/` có file `BATON.json`. Đây là **cây gậy chuyền tay**. AI nào cầm gậy mới được làm việc, đứa khác phải ngồi chờ. Cơ chế này đảm bảo **không bao giờ có chuyện 2 con AI cùng nhảy vào sửa một file gây đè code nhau**.

---

## 2. Vai trò của Bạn (Human) là gì?

Bạn là **Tổng Giám đốc / Trọng tài Tối cao (Supreme Arbiter)**.

### ❌ Những việc bạn KHÔNG CẦN LÀM nữa:
*   Không cần copy code từ Claude sang ChatGPT hỏi "code này ổn không?".
*   Không cần tự tay chia nhỏ từng dòng lệnh bash.
*   Không cần nhớ hết cú pháp API hay token tốn bao nhiêu tiền.

### ✅ Những việc bạn CẦN LÀM:
1. **Ra lệnh mở màn:** Bảo AI lập kế hoạch (Antigravity/Gemini) chốt yêu cầu bài toán.
2. **Mở cửa cho thợ làm việc:** Mở terminal chạy `claude` (Claude Code) khi đến lượt nó code, hoặc mở Codex khi đến lượt review.
3. **Phân xử khi chuông réo:** Nếu 2 con AI cãi cùn quá 2 hiệp, chuông sẽ réo, bạn chỉ cần mở file trong `05_escalation/` ra gõ phán quyết.

---

## 3. Bảng điều khiển 4 nút bấm hàng ngày (CLI Cheat-Sheet)

Bạn chỉ cần đứng ở thư mục gốc dự án và gõ qua `python .agents/board.py`:

```bash
# 1. Xem toàn cảnh tiến độ (Ai đang làm gì, việc nào xong rồi):
python .agents/board.py task list

# 2. Xem cây gậy tiếp sức đang ở tay ai:
python .agents/board.py baton status

# 3. Bật trọng tài giám sát (Nên mở ở 1 tab terminal riêng, nó sẽ kêu Beep khi có biến):
python .agents/board.py watch

# 4. Giành lại gậy khẩn cấp (Nếu 1 con AI bị đơ, hết quota, hoặc bạn muốn tự code):
python .agents/board.py baton recover
```

---

## 4. Bộ câu lệnh mẫu (Prompts) để nói chuyện với từng AI

### Khi nói với AI Lập kế hoạch (Antigravity / Gemini):
> *"Tao muốn làm tính năng [Mô tả tính năng, ví dụ: Quên mật khẩu gửi OTP qua Email]. Mày hãy lên spec chi tiết vào `.agents/00_specs/`, sau đó tạo các task vào `.agents/` và trao gậy Baton cho Mason nhé."*

### Khi mở terminal Thợ Code (Claude Code):
> *"Kiểm tra `.agents/BATON.json` xem có gậy chưa. Nếu có task giao cho mày, hãy nhận việc sang `in_progress`, viết code + unit tests đầy đủ rồi nộp sang `review` và chuyền gậy cho Reviewer."*

### Khi mở Thợ Soi (Codex / ChatGPT):
> *"Kiểm tra task trong `03_review/`. Soi diff và chạy test kiểm tra. Nếu pass thì move sang `done` và trả gậy về `orchestrator`. Nếu lỗi nghiêm trọng thì dùng lệnh reject kèm test case chứng minh lỗi."*

---
---

# [EN] HUMAN OPERATOR GUIDE

Welcome, developer! When you install `Agent Board`, your project directory transforms into an **autonomous workspace for 3 AI assistants**.

---

## 1. What Is Happening in Your Repository?

Instead of playing the digital courier copy-pasting code snippets across browser windows, your 3 AI agents (Claude Code, OpenAI Codex, Antigravity/Gemini) **read and write to `.agents/` to communicate, delegate, and audit code autonomously**.

### The 6 Kanban Folders inside `.agents/`:
*   📁 `.agents/00_specs/`: Architecture blueprints and specs created by the Orchestrator.
*   📁 `.agents/01_backlog/`: Queued tasks waiting to be implemented (Markdown files).
*   📁 `.agents/02_in_progress/`: Active tasks currently claimed by the Coder (Mason).
*   📁 `.agents/03_review/`: Completed code awaiting independent audit by the Reviewer.
*   📁 `.agents/04_done/`: Fully verified, tested, and approved tasks.
*   📁 `.agents/05_escalation/`: Deadlocked tickets rejected 2+ times, awaiting your final arbitration.

### The Relay Baton (`BATON.json`):
Located inside `.agents/BATON.json`, this is a **turn-based distributed lock**. Only the active baton holder is permitted to touch code. Other agents remain idle, completely eliminating race conditions and file collisions.

---

## 2. What Is Your Role as the Human?

You are the **Lead Architect & Supreme Arbiter**.

### ❌ What you DO NOT need to do:
*   Do NOT copy-paste code back and forth between AI chat boxes.
*   Do NOT manually orchestrate CLI commands between agents.
*   Do NOT worry about runaway pay-per-token API fees.

### ✅ What you DO:
1. **Kick off the vision:** Give high-level requirements to the Planner (Antigravity/Gemini).
2. **Authorize execution:** Open a terminal running `claude` (Claude Code) or launch Codex when their turn arrives.
3. **Arbitrate deadlocks:** When the circuit breaker trips into `05_escalation/`, make the executive decision.

---

## 3. Daily 4-Button Dashboard (CLI Cheat-Sheet)

All actions run directly from your project root:

```bash
# 1. View overall board status (Kanban overview):
python .agents/board.py task list

# 2. Check who currently holds the baton:
python .agents/board.py baton status

# 3. Run event watcher (Keep this open in a tab; it emits audio beeps on transitions):
python .agents/board.py watch

# 4. Emergency baton recovery (Reset token to Orchestrator if an agent crashes):
python .agents/board.py baton recover
```

---

## 4. Prompt Templates for Each Agent

### For the Planner / Orchestrator (Antigravity / Gemini):
> *"I want to build [Feature Description]. Please draft the specification in `.agents/00_specs/`, decompose it into backlog tasks via `board.py task create`, and hand the baton over to Mason."*

### For the Coder / Mason (Claude Code):
> *"Check `.agents/BATON.json`. If you hold the baton, claim your task to `in_progress`, implement the code with unit tests, ensure 100% test pass, move the task to `review`, and pass the baton to Reviewer."*

### For the Reviewer (Codex / ChatGPT):
> *"Inspect the task under `03_review/`. Verify the git diff and run tests. If clean, approve to `done` and pass baton to orchestrator. If broken, execute `task reject` with a concrete reproduction test file."*
