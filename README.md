# AgentRelay 🧭

> **Có bao giờ bạn bực mình vì đã trả tiền thuê mấy "trợ lý thông minh" (như ChatGPT, Claude, Gemini) về làm việc, nhưng suốt ngày bạn vẫn phải đóng vai shipper: cặm cụi copy từng dòng chữ từ cửa sổ này đem sang dán vào cửa sổ kia? Còn nếu để chúng cùng làm một lúc thì đứa này lại xóa mất bài của đứa khác?**

Dự án này sinh ra để chấm dứt hoàn toàn sự phiền toái đó.

---

### 💡 Nó hoạt động thế nào? (Giải thích cho một đứa trẻ 10 tuổi)

Hãy tưởng tượng bạn đang dán một **Chiếc bảng phân công việc trên cánh tủ lạnh**, kèm theo **Một chiếc gậy đồ chơi**:

1. **Chiếc bảng dán giấy nhớ:** Trên cánh tủ lạnh có kẻ sẵn 4 ô:
   - *Việc cần làm* ➔ *Đang làm* ➔ *Chờ kiểm tra* ➔ *Đã làm xong*.
2. **Chiếc gậy chuyền tay:** Trong nhà lúc nào cũng chỉ có duy nhất **một chiếc gậy**. Ai cầm gậy thì người đó mới được chạy lại bàn làm việc. Làm xong việc của mình, bạn đó bóc tờ giấy dán sang ô tiếp theo rồi chuyền gậy cho bạn khác. Nhờ vậy, không bao giờ có chuyện hai bạn lao vào tranh nhau một mẩu giấy hay xóa đè bài của nhau.
3. **Chuông nhờ người lớn can thiệp:** Nếu bạn kiểm tra bắt bạn làm bài sửa đi sửa lại quá 2 lần, chuông sẽ reo lên để mời bạn (chủ nhà) đứng ra phân xử, tránh cho hai bạn giận dỗi và cãi nhau lòng vòng.

Chỉ đơn giản như vậy: Mọi trợ lý tự nhìn bảng tủ lạnh, tự chuyền gậy cho nhau để hoàn thành trọn vẹn việc của bạn từ đầu đến cuối mà bạn không cần phải copy-paste lấy một lần!

---

## 🚀 Cài đặt trong 1 nốt nhạc (1 Dòng lệnh duy nhất)

Chạy trực tiếp dòng lệnh này tại thư mục dự án của bạn (không cần cài thêm bất kỳ phần mềm hay thư viện lạ nào):

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

## 🎭 Phân vai theo ý bạn (Dynamic Role Matrix)

Mặc định: **Gemini / Antigravity** lập kế hoạch, **Claude** viết mã nguồn, **Codex** kiểm tra chất lượng.  
Bạn thích tráo đổi vai trò thế nào cũng được bằng 1 câu lệnh ngắn:

```bash
# Đổi: Cho Claude lập kế hoạch, Gemini viết mã, Codex kiểm tra:
python .agents/board.py roster --orchestrator claude --mason antigravity --reviewer codex
```

Hệ thống sẽ tự động gửi luật chơi chuẩn xác đến từng trợ lý!

---

## 🛠️ Bảng lệnh cầm tay (Cheat Sheet)

Mọi thao tác hàng ngày đều thông qua chiếc điều khiển ngắn gọn `python .agents/board.py`:

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
