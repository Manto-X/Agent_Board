# Kế hoạch triển khai: Tái cấu trúc Agents_Board thành Zero-Install Starter Kit

## Background & Problem Statement (Bối cảnh & Vấn đề)
- **Bối cảnh:** Agents_Board hiện tại để mã nguồn core tại thư mục `agents_board/` ở root và gán cứng Antigravity làm Orchestrator, Claude làm Mason, Codex làm Reviewer. Ngoài ra root bị lẫn lộn giữa file kế hoạch, template và mã nguồn.
- **Vấn đề:**
  - Người dùng mới muốn dùng repo làm Starter Kit cho dự án riêng sẽ bị đụng độ không gian nếu dự án của họ cần thư mục `scripts/` hoặc `agents_board/`.
  - Không thể hoán đổi vai trò AI (ví dụ muốn Claude làm Orchestrator, Antigravity làm Mason).
  - Chưa có lệnh gọi ngắn (short command) để khởi tạo và thao tác bảng tin nhanh chóng.
- **Mục tiêu:**
  - Gom toàn bộ mã nguồn điều phối vào `.agents/scripts/` và dispatcher `.agents/board.py`.
  - Chuẩn hóa root chỉ chứa đúng 4 file markdown (`README.md`, `AGENTS.md`, `CLAUDE.md`, `CODEX.md`).
  - Hỗ trợ Role Matrix động qua `.agents/project_config.json` và CLI flags.
  - Cung cấp script cài đặt nhanh `get_board.py` để kéo kit vào dự án bất kỳ.

## Design Principles (Nguyên tắc thiết kế / Ranh giới bảo mật)
- **Zero-Install & Zero-Dependency:** Chỉ dùng Python Standard Library (3.10+), không yêu cầu `pip install`, không cài thêm bất kỳ package ngoài nào.
- **Complete Isolation:** 100% mã nguồn và dữ liệu điều phối của AI nằm trong `.agents/`. Dự án người dùng tự do sử dụng `src/`, `tests/`, `scripts/`, `docs/`.
- **Short Command First:** Cung cấp bộ lệnh ngắn thông qua dispatcher `.agents/board.py` hoặc `.agents/scripts/*.py`.
- **Decoupled Roles & Platforms:** Tách bạch 3 vai trò (`orchestrator`, `mason`, `reviewer`) khỏi 3 nền tảng AI (`antigravity`, `claude`, `codex`).
- **Atomic Operations & Circuit Breaker:** Giữ nguyên tính nguyên tử khi di chuyển task và ngắt cầu chì tối đa 2 lần từ chối.

## Data Models (Mô hình dữ liệu & Cấu trúc Schema)

### 1. Project Config Schema (`.agents/project_config.json`)
```json
{
  "project_name": "My Project",
  "version": "1.0.0",
  "roles": {
    "orchestrator": "antigravity",
    "mason": "claude",
    "reviewer": "codex"
  },
  "max_rejections": 2
}
```

### 2. Baton Schema (`.agents/BATON.json`)
```json
{
  "holder": "orchestrator",
  "task_id": null,
  "action": "project_initialized",
  "acquired_at": "2026-10-17T06:00:00Z",
  "expires_at": null
}
```

## Algorithm (Thuật toán đồng bộ vai trò động & Dispatcher)

```text
FUNCTION sync_roles(config_path):
    config = load_json(config_path)
    roles_map = config["roles"]  # e.g. orchestrator -> claude, mason -> antigravity
    
    FOR role_name, platform IN roles_map.items():
        role_content = read_file(".agents/roster/" + role_name + ".md")
        target_file = get_platform_file(platform) # claude -> CLAUDE.md, codex -> CODEX.md, antigravity -> AGENTS.md
        write_agent_instruction(target_file, role_name, role_content)

FUNCTION dispatch_command(args):
    subcommand = args[0] # task | baton | watch | roster | init
    EXECUTE script in ".agents/scripts/" + subcommand + ".py" passing args[1:]
```

## Edge Cases (Xử lý trường hợp biên)
- **Thiếu file config hoặc config hỏng:** Tự động fallback về cấu hình mặc định (Antigravity = Orchestrator, Claude = Mason, Codex = Reviewer).
- **Trùng lặp nền tảng AI:** Cảnh báo nếu gán 1 nền tảng AI cho 2 vai trò đối kháng nhau (ví dụ vừa làm Mason code vừa làm Reviewer tự duyệt code).
- **Đường dẫn chứa khoảng trắng:** Xử lý toàn bộ path bằng `pathlib.Path` an toàn trên Windows và Linux.

## Setup & Operations (Thiết lập & Vận hành)
- **Cài đặt 1 dòng:** `python get_board.py` hoặc kéo template từ GitHub.
- **Lệnh điều phối ngắn gọn:**
  - `python .agents/board.py baton status`
  - `python .agents/board.py task move TASK-01 review`
  - `python .agents/board.py watch`
- **Khởi tạo và gán vai trò linh hoạt:**
  - `python .agents/scripts/init.py --orchestrator claude --mason antigravity --reviewer codex`

## Technical Decisions (Quyết định kỹ thuật)
- **Ngôn ngữ:** Python 3.10+ (Standard Library duy nhất: `pathlib`, `json`, `argparse`, `sys`, `subprocess`, `urllib`).
- **Dispatcher Pattern:** Tệp `.agents/board.py` đóng vai trò cổng điều phối chung để người dùng và AI không cần nhớ đường dẫn sâu.
- **Roster Matrix Ingestion:** Tự động đọc cấu hình vai trò từ `.agents/project_config.json` để render nội dung chính xác vào `CLAUDE.md`, `CODEX.md`, `AGENTS.md`.

## File Change Manifest (Danh sách tệp thay đổi (Manifest))

| File Path | Action | Description |
| :--- | :--- | :--- |
| `.agents/scripts/config.py` | CREATE | Module cấu hình đường dẫn và hằng số trong `.agents/` |
| `.agents/scripts/baton.py` | CREATE | CLI quản lý gậy tiếp sức |
| `.agents/scripts/task.py` | CREATE | CLI quản lý vòng đời task và circuit breaker |
| `.agents/scripts/roster.py` | CREATE | CLI đồng bộ ma trận vai trò động |
| `.agents/scripts/watcher.py` | CREATE | Daemon giám sát bảng tin Kanban |
| `.agents/scripts/init.py` | CREATE | Script khởi tạo cấu trúc và cấu hình vai trò |
| `.agents/board.py` | CREATE | Dispatcher ngắn gọn gọi mọi tính năng (`python .agents/board.py <cmd>`) |
| `get_board.py` | CREATE | Script bootstrap 1 dòng kéo starter kit vào dự án mới |
| `.agents/template_task.md` | CREATE | Mẫu task ticket nằm trong `.agents/` |
| `.agents/00_specs/SPEC-00-architecture.md` | CREATE | Chuyển file kế hoạch cũ vào đúng thư mục specs |
| `README.md` | MODIFY | Cập nhật hướng dẫn ngắn gọn cho người dùng |
| `CLAUDE.md` | MODIFY | Đồng bộ câu lệnh mới cho Claude Code |
| `CODEX.md` | MODIFY | Đồng bộ câu lệnh mới cho Codex |
| `AGENTS.md` | MODIFY | Đồng bộ câu lệnh mới cho Orchestrator / Gemini |
| `tests/test_agents_board.py` | MODIFY | Cập nhật bộ unit test kiểm thử cấu trúc `.agents/scripts/` |
| `Agents_Board_Plan.md` | DELETE | Dọn khỏi root sau khi chuyển vào `00_specs/` |
| `template_task.md` | DELETE | Dọn khỏi root sau khi chuyển vào `.agents/` |
| `agents_board/` | DELETE | Dọn sạch mã nguồn cũ ở root sau khi dời vào `.agents/scripts/` |

## Verification Criteria (Tiêu chí nghiệm thu)

| ID | Category | Command/Test Scenario | Expected Outcome |
| :--- | :--- | :--- | :--- |
| VC-01 | Clean Root | `Get-ChildItem -File` | Chỉ còn đúng 4 file `.md` và file git ở root |
| VC-02 | Short Dispatcher | `python .agents/board.py baton status` | Hiển thị trạng thái Baton thành công |
| VC-03 | Dynamic Roles | `python .agents/scripts/init.py --orchestrator claude --mason antigravity --reviewer codex` | `CLAUDE.md` nhận vai Orchestrator, `AGENTS.md` nhận vai Mason |
| VC-04 | Task Lifecycle | `python .agents/board.py task list` | Liệt kê danh sách task chuẩn xác |
| VC-05 | Unit Tests | `python -m unittest discover -s tests` | 100% tests pass cleanly |
| VC-06 | Zero Install | Test import không phụ thuộc pip package ngoài | Thành công với Python chuẩn |
