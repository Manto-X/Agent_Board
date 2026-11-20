# Agent Board — Architecture & Core Protocols
# Kiến trúc & Giao thức cốt lõi của Agent Board

> **Quy ước song ngữ:** Phần Tiếng Việt ở trên, phần English version ở dưới.
> **Bilingual convention:** Vietnamese version first, English version below.

---

# [VI] KIẾN TRÚC & GIAO THỨC CỐT LÕI

## 1. Triết lý Thiết kế: Blackboard Pattern không dùng API
Agent Board hoạt động dựa trên mô hình **Blackboard (Bảng tin chung trên Filesystem)** kết hợp với **Turn-Based Semaphore (Gậy tiếp sức)**:
- **Không tốn phí API:** Không dùng API framework (CrewAI/AutoGen). Tận dụng trực tiếp các gói thuê bao phẳng (flat-rate sub) của Claude Code, Codex, Antigravity.
- **Single Source of Truth:** Thư mục `.agents/` là nơi lưu trữ toàn bộ trạng thái, spec, task và lịch sử review.
- **Zero Heavy Dependencies:** Chạy 100% bằng Python Standard Library có sẵn trong hệ điều hành (`pathlib`, `json`, `argparse`, `os`).

```text
+-------------------------------------------------------------------------+
|                              AGENT BOARD                                |
|                                                                         |
|  [00_specs]       [01_backlog]      [02_in_progress]     [03_review]    |
|   (Spec PRD)    (Task Markdown)     (Thợ code làm)     (Thợ soi duyệt)  |
|                                                                         |
|        [04_done] (Hoàn thành)  <---  [05_escalation] (Trọng tài xử)     |
+-------------------------------------------------------------------------+
                                    ▲
                                    │
                         [BATON.json] (Gậy tiếp sức)
             "Chỉ ai cầm gậy mới được đọc task và ghi code"
```

---

## 2. Giao thức Cây gậy tiếp sức (The Relay Baton Protocol)

File `.agents/BATON.json` đóng vai trò là một **Distributed Semaphore / Mutex Lock**:

```json
{
  "holder": "mason",
  "task_id": "TASK-01",
  "action": "implementing",
  "acquired_at": "2026-10-17T12:00:00Z",
  "expires_at": null
}
```

### Luật cầm gậy:
1. **Ai cầm gậy mới được chạy:** Nếu `holder != "mason"`, Claude Code phải ở trạng thái nghỉ (IDLE), không được tự ý sửa file hay commit.
2. **Chuyển giao nguyên tử:** Khi Mason làm xong, Mason gọi `python .agents/board.py baton pass reviewer --task-id TASK-01`. Gậy được chuyển sang Reviewer.
3. **Cứu hộ khẩn cấp (`recover`):** Nếu một agent bị crash hoặc hết token, Sếp hoặc Orchestrator gọi `python .agents/board.py baton recover` để kéo gậy về quyền điều phối.

---

## 3. Thao tác tập tin nguyên tử (Atomic File Operations)

Để triệt tiêu tình trạng đọc dở dang (Race Condition khi AI đang stream ghi file):
- Mọi thao tác ghi task hoặc cập nhật baton đều ghi vào file tạm `.tmp`.
- Sau khi ghi trọn vẹn, gọi `os.replace()` để đổi tên đè lên file chính thức.
- Hệ điều hành đảm bảo thao tác rename là nguyên tử (Atomic): Agent khác chỉ đọc được file khi nó đã hoàn chỉnh 100%.

---

## 4. Cầu chì tự ngắt chống cãi cùn (Circuit Breaker & Rejection Contract)

Vấn đề lớn nhất của multi-agent là vòng lặp **Ping-Pong vô tận** (Reviewer bắt bẻ -> Mason sửa -> Reviewer lại chê -> lặp mãi):

### 4.1. Hợp đồng thẩm định (Rejection Contract):
- **CẤM bắt bẻ văn xuôi:** Reviewer không được nhận xét cảm tính ("Code chưa đẹp", "Nên viết lại").
- **Phân loại độ nghiêm trọng:**
  - `NITPICK`: Góp ý nhỏ, style code -> **KHÔNG ĐƯỢC từ chối**. Tự động gắn nhãn Advisory và cho Pass.
  - `MAJOR` / `BLOCKER`: Lỗi logic, hổng bảo mật, tạch test -> Bắt buộc cung cấp đường dẫn test case chứng minh lỗi (`--test-file`).

### 4.2. Cầu chì 2 hiệp:
Mỗi task có trường `reject_count`:
- **Hiệp 1 (`reject_count = 1`):** Trả về `02_in_progress`, gậy chuyển lại cho Mason sửa.
- **Hiệp 2 (`reject_count = 2`):** Cầu chì **tự động ngắt ngay lập tức**:
  - Task bị đẩy thẳng vào `05_escalation/`.
  - Gậy chuyển về cho **Orchestrator** (Antigravity) hoặc Sếp để phán quyết tối hậu (Ép duyệt hoặc Chia nhỏ task).

---

## 5. Ma trận Phân vai động (Dynamic Role Matrix)

Thay vì gắn cứng một model vào một việc, Agent Board hỗ trợ tráo đổi linh hoạt:
- **Orchestrator (Cầm trịch):** Lên spec, chia task, phân xử tranh chấp.
- **Mason (Thợ xây):** Viết code tính năng, chạy unit tests cục bộ.
- **Reviewer (Thợ soi):** Kiểm tra tính đúng đắn, bảo mật, viết test bắt lỗi.

Lệnh `python .agents/board.py roster --orchestrator <A> --mason <B> --reviewer <C>` tự động đồng bộ vai trò vào các file cấu hình tự nhiên:
- `CLAUDE.md` (cho Claude Code)
- `CODEX.md` (cho OpenAI Codex)
- `AGENTS.md` (cho Antigravity / Gemini)

---
---

# [EN] ARCHITECTURE & CORE PROTOCOLS

## 1. Design Philosophy: Zero-API Blackboard Pattern
Agent Board is built on the **Blackboard Architectural Pattern** on the local filesystem, reinforced by a **Turn-Based Semaphore (The Relay Baton)**:
- **Zero API Fees:** Eliminates expensive API token overhead (CrewAI/AutoGen). Fully utilizes your flat-rate subscriptions for Claude Code, Codex, and Antigravity.
- **Single Source of Truth:** The `.agents/` folder maintains all project state, specifications, task tickets, and audit trails.
- **Zero Heavy Dependencies:** Runs entirely on the built-in Python Standard Library (`pathlib`, `json`, `argparse`, `os`).

---

## 2. The Relay Baton Protocol (Distributed Semaphore)

The file `.agents/BATON.json` acts as a distributed mutex lock:

```json
{
  "holder": "mason",
  "task_id": "TASK-01",
  "action": "implementing",
  "acquired_at": "2026-10-17T12:00:00Z",
  "expires_at": null
}
```

### Baton Rules:
1. **Holder-Only Execution:** If `holder != "mason"`, Claude Code stays idle and cannot modify source files or commit.
2. **Atomic Hand-off:** Upon task completion, Mason executes `python .agents/board.py baton pass reviewer --task-id TASK-01`, delegating execution to Reviewer.
3. **Emergency Recovery (`recover`):** If an agent crashes or exhausts its hourly quota, the Orchestrator or human lead runs `python .agents/board.py baton recover` to reclaim governance.

---

## 3. Atomic File Operations

To eliminate partial reads during agent streaming writes:
- All task updates and baton transfers write first to temporary `.tmp` files.
- Once completely serialized, `os.replace()` performs an atomic rename.
- Other agents never encounter truncated or corrupt JSON/Markdown files.

---

## 4. Anti-Ping-Pong Circuit Breaker & Rejection Contract

A common failure in multi-agent workflows is the **infinite rejection loop** (Reviewer nitpicks -> Mason adjusts -> Reviewer rejects again):

### 4.1. Structured Rejection Contract:
- **No Vague Critiques:** Reviewers cannot reject based on subjective prose.
- **Severity Classification:**
  - `NITPICK`: Code styling, variable naming -> **CANNOT reject**. Treated as non-blocking advisory; task passes.
  - `MAJOR` / `BLOCKER`: Broken logic, security flaws, failing tests -> Rejection requires a concrete reproduction test file (`--test-file`).

### 4.2. Two-Strike Circuit Breaker:
Tracked via `reject_count` in task frontmatter:
- **Strike 1 (`reject_count = 1`):** Task reverts to `02_in_progress`; baton returns to Mason for bug fixing.
- **Strike 2 (`reject_count = 2`):** **Circuit breaker trips immediately**:
  - Task escalates to `05_escalation/`.
  - Baton returns to **Orchestrator** or the human developer for final arbitration (Force Pass or Split Task).

---

## 5. Dynamic Role Matrix & Natural Role Ingestion

Roles are modular and interchangeable at runtime:
- **Orchestrator:** Spec refinement, task decomposition, dispute arbitration.
- **Mason:** Core feature development, local test verification.
- **Reviewer:** Rigorous audit, algorithmic correctness, regression prevention.

Running `python .agents/board.py roster --orchestrator <A> --mason <B> --reviewer <C>` automatically compiles tailored instructions into native agent configs:
- `CLAUDE.md` (Claude Code)
- `CODEX.md` (OpenAI Codex)
- `AGENTS.md` (Antigravity / Gemini)
