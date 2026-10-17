# AgentRelay 🧭

> **Có bao giờ anh em bực mình vì đã bỏ tiền túi mua đủ món đồ chơi xịn (ChatGPT, Claude, Gemini) về làm việc, nhưng rốt cuộc cả ngày mình vẫn phải làm shipper: cặm cụi copy từng đoạn chữ từ tab này đem sang dán vào tab kia? Đã thế, hễ để mấy đứa cùng mó tay vào một chỗ là đứa này tiện tay xóa sạch bài của đứa khác!**

Cái tool này đẻ ra để trị dứt điểm cái cảnh lắt nhắt đó cho anh em.

---

### 💡 Nó chạy kiểu gì? (Giải thích dễ hiểu như chuyện con nít)

Tưởng tượng trong nhà anh em có một **Cái bảng dán giấy nhớ trên cánh tủ lạnh**, kèm thêm **Một cây gậy chuyền tay**:

1. **Cái bảng dán giấy nhớ:** Trên cánh tủ lạnh chia sẵn 4 ngăn:
   - *Việc cần làm* ➔ *Đang làm* ➔ *Chờ soi lỗi* ➔ *Xong xuôi*.
2. **Cây gậy chuyền tay:** Cả nhà chỉ có đúng **một cây gậy duy nhất**. Đứa nào ôm gậy thì đứa đó mới được ngồi vào bàn làm việc. Làm xong phần mình thì tự tay bóc tờ giấy dán sang ngăn kế bên, rồi chuyền gậy cho đứa tiếp theo. Tuyệt đối không có chuyện hai ba đứa xông vào tranh nhau một mẩu giấy hay giẫm chân lên nhau.
3. **Chuông réo phụ huynh:** Nếu đứa soi lỗi bắt đứa làm bài sửa đi sửa lại quá 2 lần, chuông sẽ réo ầm lên để mời anh em (chủ nhà) vào đập bàn phân xử, dẹp ngay trò cãi cùn lòng vòng.

Đơn giản vậy thôi: Mấy đứa đệ tự nhìn bảng tủ lạnh, tự chuyền gậy cho nhau cày việc từ đầu đến đuôi. Anh em rảnh tay đi pha cốc cà phê uống, khỏi cần nhấc tay copy-paste lấy một lần!

---

## 💎 Điểm độc đáo của AgentRelay (So với các repo khác trên mạng)

Nếu anh em từng tìm hiểu các công cụ đa tác tử (Multi-Agent) trên GitHub (như `Kanbots`, `Kandev`, `Blackboard`, hay `CrewAI`), anh em sẽ thấy **AgentRelay** giải quyết bài toán theo cách thực dụng và nhẹ đầu hơn hẳn:

| Tiêu chí | Các công cụ khác trên GitHub (`Kanbots`, `Kandev`, `CrewAI`) | **AgentRelay** 🧭 |
| :--- | :--- | :--- |
| **Cài đặt** | Bắt cài đủ thứ: Node.js, Electron, Docker, Rust, hoặc cả chục thư viện pip nặng nề. | **Zero-Install:** 100% Python có sẵn trong máy. Tải về là chạy ngay, không cần `pip install`. |
| **Chi phí dùng AI** | Bắt mua API key trả tiền theo lượt (đốt tiền rất xót ruột). | **0 đồng phí phát sinh:** Tận dụng 100% tài khoản ChatGPT, Claude, Gemini anh em đã mua hàng tháng. |
| **Chống đè code** | Dùng Git worktrees phức tạp hoặc dễ bị xung đột khi nhiều đứa cùng sửa. | **Gậy tiếp sức (`BATON.json`):** Đứa nào cầm gậy đứa đó mới được làm. Tuyệt đối không giẫm chân nhau. |
| **Chống kẹt vòng lặp** | Thợ code và người kiểm tra dễ cãi nhau lòng vòng vô tận (Ping-Pong loop). | **Cầu chì tự ngắt:** Bị từ chối 2 lần là tự ngắt ngay, réo chuông mời anh em vào phân xử. |
| **Đổi vai trò** | Gắn chết vai hoặc phải sửa code nguồn lằng nhằng. | **1 dòng lệnh đổi vai:** Thích cho Claude lập kế hoạch hay Gemini viết code chỉ mất 3 giây. |
| **Sạch sẽ thư mục** | Xâm lấn bừa bãi ra thư mục gốc dự án. | **Nhà ai nấy ở:** 100% đồ nghề AI giấu kín trong `.agents/`, trả lại không gian sạch bóng cho dự án của anh em. |

---

## 🚀 Cài đặt trong 1 nốt nhạc (1 Dòng lệnh duy nhất)

Chạy ngay dòng lệnh này tại thư mục dự án của anh em (khỏi cần cài thêm bất kỳ phần mềm hay thư viện lạ nào):

* **Windows PowerShell:**
  ```powershell
  irm https://raw.githubusercontent.com/tomyxo/Agents_Board/main/get_board.py | python
  ```

* **Linux / macOS:**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/tomyxo/Agents_Board/main/get_board.py | python3
  ```

*(Hoặc dùng nút **"Use this template"** trên GitHub để tạo dự án mới toanh).*

---

## 🎭 Phân vai theo ý anh em (Dynamic Role Matrix)

Mặc định: **Gemini / Antigravity** lập kế hoạch, **Claude** viết mã nguồn, **Codex** kiểm tra chất lượng.  
Thích tráo đổi vai trò thế nào cũng được bằng 1 câu lệnh ngắn:

```bash
# Đổi: Cho Claude lập kế hoạch, Gemini viết mã, Codex kiểm tra:
python .agents/board.py roster --orchestrator claude --mason antigravity --reviewer codex
```

Hệ thống sẽ tự động gửi luật chơi chuẩn xác đến từng trợ lý!

---

## ⚡ Bộ lệnh siêu ngắn (Short Command Reference)

Không cần nhớ đường dẫn thư mục sâu dòng làm gì, tất cả chỉ cần gõ qua **1 cửa ngõ duy nhất** `python .agents/board.py`:

```bash
# 📋 Bảng việc
python .agents/board.py task list                      # Xem toàn bộ bảng việc
python .agents/board.py task create --id T01 --title "X" # Tạo một việc mới
python .agents/board.py task move T01 in_progress      # Nhận việc làm
python .agents/board.py task move T01 review           # Nộp bài đi soi
python .agents/board.py task move T01 done             # Nghiệm thu xong
python .agents/board.py task reject T01 --reason "Lỗi" # Bắt làm lại

# 🏃 Gậy tiếp sức
python .agents/board.py baton status                   # Xem ai đang giữ gậy
python .agents/board.py baton pass mason --task-id T01 # Chuyền cho thợ code
python .agents/board.py baton pass reviewer            # Chuyền cho thợ soi
python .agents/board.py baton recover                  # Giành lại gậy khẩn cấp

# 🔔 Trọng tài & Phân vai
python .agents/board.py watch                          # Bật chuông theo dõi bảng việc
python .agents/board.py roster --sync                  # Nạp lại luật chơi cho các AI
```

### Chi tiết các lệnh cầm tay khi cần:

### 🏃 Chuyền gậy làm việc
```bash
# Xem ai đang giữ gậy
python .agents/board.py baton status

# Chuyền gậy cho thợ viết mã
python .agents/board.py baton pass mason --task-id TASK-01

# Chuyền gậy cho người kiểm tra
python .agents/board.py baton pass reviewer --task-id TASK-01

# Lấy lại gậy khẩn cấp
python .agents/board.py baton recover
```

### 📋 Quản lý Công việc
```bash
# Xem toàn bộ bảng việc
python .agents/board.py task list

# Tạo một việc mới
python .agents/board.py task create --id TASK-01 --title "Xây dựng trang đăng nhập"

# Chuyển việc qua các ô
python .agents/board.py task move TASK-01 in_progress
python .agents/board.py task move TASK-01 review
python .agents/board.py task move TASK-01 done

# Trả lại bài bắt sửa (kèm lý do cụ thể)
python .agents/board.py task reject TASK-01 --reason "Chưa kiểm tra trường hợp mật khẩu để trống" --severity BLOCKER
```

### 🔔 Bật Trọng tài quan sát
Mở một cửa sổ riêng và để đó (hoàn toàn miễn phí, không tốn tài nguyên):
```bash
python .agents/board.py watch
```
Mỗi khi có ai chuyền gậy hoặc chuyển việc sang ô mới, chuông báo sẽ phát tiếng kêu và thông báo ngay trên màn hình.

---

## 🧪 Kiểm thử tự động

```bash
python -m unittest tests/test_agents_board.py
```
Toàn bộ hệ thống chạy 100% bằng thư viện có sẵn của Python, không phụ thuộc bất kỳ gói cài đặt bên ngoài nào.
