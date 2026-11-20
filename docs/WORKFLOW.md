# Agent Board — Practical Multi-Agent Workflow Guide
# Hướng dẫn Quy trình Phối hợp Thực chiến

> **Quy ước song ngữ:** Phần Tiếng Việt ở trên, phần English version ở dưới.
> **Bilingual convention:** Vietnamese version first, English version below.

---

# [VI] QUY TRÌNH PHỐI HỢP THỰC CHIẾN (4 GIAI ĐOẠN)

Quy trình chuẩn để Sếp điều phối 3 trợ lý AI (Antigravity, Claude Code, Codex) trong một dự án thực tế:

```text
[Sếp + Antigravity] ➔ Tạo Spec & Task ➔ Trao Baton
                              │
                              ▼
                      [Claude Code: Mason]
                   Viết Code + Chạy Test 100%
                              │
                              ▼
                      [Codex: Reviewer]
                    Thẩm định diff & Logic
                   ╱                      ╲
             [ĐẠT]                          [TẠCH]
              ▼                               ▼
          04_done                   Lần 1: Trả lại Mason sửa
     (Chuyền Baton về)              Lần 2: 05_escalation (Sếp phân xử)
```

---

## Giai đoạn 1: Lấy Spec & Khởi tạo Task (Sếp + Antigravity)

1. **Phỏng vấn yêu cầu:** Sếp mở Antigravity (hoặc Gemini), gõ `/grill-me` để chốt tài liệu đặc tả kiến trúc.
2. **Lưu Spec:** Antigravity viết tài liệu vào `.agents/00_specs/SPEC-01-auth.md`.
3. **Phân rã task:**
   ```bash
   python .agents/board.py task create \
     --id TASK-01 \
     --title "Xây dựng module JWT Authentication" \
     --assignee mason \
     --reviewer reviewer \
     --spec "00_specs/SPEC-01-auth.md"
   ```
4. **Trao gậy cho Mason (Claude Code):**
   ```bash
   python .agents/board.py baton pass mason --task-id TASK-01 --action "implementing"
   ```

---

## Giai đoạn 2: Viết mã nguồn & Kiểm thử (Claude Code - Mason)

1. **Mở Claude Code:** Chạy `claude` tại terminal. Claude tự đọc `CLAUDE.md` và kiểm tra `.agents/BATON.json`.
2. **Nhận task:**
   ```bash
   python .agents/board.py task move TASK-01 in_progress
   ```
3. **Code & Unit Test:** Claude viết mã nguồn trong `src/` và bổ sung unit tests trong `tests/`.
4. **Kiểm tra trước khi nộp:** Chạy test trên máy đảm bảo 100% pass.
5. **Nộp bài & Chuyền gậy:**
   ```bash
   python .agents/board.py task move TASK-01 review
   python .agents/board.py baton pass reviewer --task-id TASK-01 --action "reviewing"
   ```

---

## Giai đoạn 3: Thẩm định & Duyệt code (Codex - Reviewer)

1. **Mở Codex / ChatGPT:** Đọc diff giữa code mới và spec.
2. **Kịch bản A — Đạt yêu cầu (PASS):**
   ```bash
   python .agents/board.py task move TASK-01 done
   python .agents/board.py baton pass orchestrator --action "idle"
   ```
   *Task đã xong xuôi, gậy quay về cho Orchestrator để nhận task tiếp theo.*

3. **Kịch bản B — Không đạt (REJECT):**
   Reviewer bắt buộc phải chỉ rõ lý do và đường dẫn file test tái hiện lỗi:
   ```bash
   python .agents/board.py task reject TASK-01 \
     --reason "Thiếu kiểm tra hết hạn của Refresh Token" \
     --severity BLOCKER \
     --test-file "tests/test_token_expiry.py"
   ```
   *Lệnh này sẽ tự động chuyển task về lại `02_in_progress` và trả gậy cho Mason fix.*

---

## Giai đoạn 4: Phân xử Tranh chấp (05_escalation)

Nếu Reviewer từ chối lần thứ 2 (`reject_count == 2`):
- Hệ thống tự ngắt cầu chì, chuyển task sang `.agents/05_escalation/`.
- Chuông watcher réo thông báo.
- Antigravity hoặc Sếp mở file task ra phân xử:
  - **Ép duyệt:** `python .agents/board.py task move TASK-01 done`
  - **Chia nhỏ:** Hủy task cũ, tạo 2 sub-task nhỏ hơn giao lại cho Mason.

---
---

# [EN] PRACTICAL MULTI-AGENT WORKFLOW GUIDE

A step-by-step operational guide for coordinating 3 AI agents (Antigravity, Claude Code, Codex) on real-world codebases:

---

## Phase 1: Specification & Task Dispatch (Human + Antigravity)

1. **Requirement Alignment:** Use Antigravity/Gemini (`/grill-me`) to define specifications and acceptance criteria.
2. **Commit Spec:** Save document to `.agents/00_specs/SPEC-01-auth.md`.
3. **Decompose into Tasks:**
   ```bash
   python .agents/board.py task create \
     --id TASK-01 \
     --title "Implement JWT Authentication module" \
     --assignee mason \
     --reviewer reviewer \
     --spec "00_specs/SPEC-01-auth.md"
   ```
4. **Hand Baton to Mason (Claude Code):**
   ```bash
   python .agents/board.py baton pass mason --task-id TASK-01 --action "implementing"
   ```

---

## Phase 2: Implementation & Verification (Claude Code - Mason)

1. **Launch Claude Code:** Start `claude`. It automatically inspects `CLAUDE.md` and verifies `BATON.json`.
2. **Claim Task:**
   ```bash
   python .agents/board.py task move TASK-01 in_progress
   ```
3. **Implement & Test:** Claude writes code in `src/` and unit tests in `tests/`.
4. **Local Audit:** Ensure 100% of tests pass cleanly.
5. **Submit for Review & Pass Baton:**
   ```bash
   python .agents/board.py task move TASK-01 review
   python .agents/board.py baton pass reviewer --task-id TASK-01 --action "reviewing"
   ```

---

## Phase 3: Quality Audit & Approval (Codex - Reviewer)

1. **Inspect Code Diff:** Reviewer evaluates architectural soundness and edge cases.
2. **Scenario A — Approval (PASS):**
   ```bash
   python .agents/board.py task move TASK-01 done
   python .agents/board.py baton pass orchestrator --action "idle"
   ```
   *Task is completed; baton returns to Orchestrator for the next backlog item.*

3. **Scenario B — Rejection (REJECT):**
   Reviewer must supply an actionable reason and a reproduction test case:
   ```bash
   python .agents/board.py task reject TASK-01 \
     --reason "Refresh token expiry is not invalidated on logout" \
     --severity BLOCKER \
     --test-file "tests/test_token_expiry.py"
   ```
   *The task reverts to `02_in_progress`, and the baton returns to Mason for bug fixing.*

---

## Phase 4: Dispute Escalation (05_escalation)

Upon a second rejection (`reject_count == 2`):
- The circuit breaker triggers automatically, isolating the ticket in `.agents/05_escalation/`.
- Watcher sounds an alert.
- The Orchestrator or human developer reviews the deadlock:
  - **Force Approval:** `python .agents/board.py task move TASK-01 done`
  - **Task Decomposition:** Split the ambiguous task into smaller, testable sub-tasks.
