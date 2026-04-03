# 🚀 HƯỚNG DẪN CÀI ĐẶT & CHẠY HỆ THỐNG LMS (DÀNH CHO NGƯỜI MỚI)

Tài liệu này hướng dẫn bạn từ một máy tính trống trơn cho đến khi chạy được hệ thống **WEB AI HACKATHON 2026**.

---

## 🛑 PHẦN 1: Chuẩn bị máy ảo Ubuntu
Nếu bạn chưa có Linux, hãy cài đặt Ubuntu (khuyên dùng bản **22.04 LTS** hoặc **24.04 LTS**):
1. Tải [VirtualBox](https://www.virtualbox.org/) và tệp [ISO Ubuntu](https://ubuntu.com/download/desktop).
2. Tạo máy ảo mới: CPU >= 2 Core, RAM >= 4GB, Disk >= 40GB.
3. Cài đặt Ubuntu với các thiết lập mặc định.

---

## 🛠️ PHẦN 2: Cài đặt Môi trường (Docker & Công cụ)
Mở Terminal (Ctrl + Alt + T) và copy-paste từng dòng lệnh sau:

### 1. Cập nhật hệ thống
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Cài đặt Docker (Trái tim của hệ thống)
```bash
# Cài đặt docker
sudo apt install docker.io docker-compose -y

# Cho phép user chạy docker không cần sudo (Cần Log out và Log in lại để có hiệu lực)
sudo usermod -aG docker $USER
```

### 3. Cài đặt Git & Python (Công cụ hỗ trợ)
```bash
sudo apt install git python3 python3-pip -y
```

---

## 📦 PHẦN 3: Tải mã nguồn & Khởi chạy hệ thống

### 1. Tải hệ thống (Clone dự án)
Nếu bạn đang ở trên máy chủ mới hoặc máy ảo Ubuntu, hãy chạy lệnh sau:
```bash
# Tải toàn bộ mã nguồn từ GitHub
git clone https://github.com/Phan-Thanh-Danh/LMS_AET.git

# Di chuyển vào thư mục cấu hình Docker của dự án
cd LMS_AET/docker
```

### 2. Khởi chạy Docker (Bật máy chủ)
```bash
# Lệnh này sẽ tải MariaDB, Redis và Frappe tự động
docker compose up -d
```
*Đợi khoảng 2-5 phút trong lần chạy đầu tiên để hệ thống khởi tạo cơ sở dữ liệu.*

---

## 🌐 PHẦN 4: Truy cập Hệ thống & Tài khoản Demo

| Vai trò | URL Truy cập | Tài khoản | Mật khẩu |
| :--- | :--- | :--- | :--- |
| **Admin (Ban Tổ Chức)** | `http://<IP-MÁY-CHỦ>:8000/app` | `Administrator` | `admin` |
| **Student (Thí sinh)** | `http://<IP-MÁY-CHỦ>:8000/lms` | `student_hackathon_test@example.com` | `StrongPass@2026` |

> [!TIP]
> Nếu bạn chạy trên máy chủ (VPS/Cloud), hãy thay `localhost` bằng **địa chỉ IP công khai** của máy chủ. Đừng quên mở cổng **8000** trong phần thiết lập Firewall/Security Group của nhà cung cấp Cloud.

---

## 🤖 PHẦN 5: Chạy luồng Hackathon Tự Động (Automation)
Tôi đã viết sẵn một script để bạn không phải thao tác tay cho demo lần đầu. Hệ thống sẽ tự động:
1. Tạo bài tập Hackathon.
2. Tự nộp bài với nội dung AI Resume Screener.
3. Tự chấm điểm 85/100.

**Lệnh chạy script (Chạy khi Docker đang bật):**
```bash
docker compose exec -T frappe bash -c "cd /home/frappe/frappe-bench && bench --site lms.localhost console < /workspace/lms_automated_flow.py"
```

---

## 📝 PHẦN 6: Cấu trúc thư mục quan trọng
- `/docker`: Chứa cấu hình máy chủ (docker-compose.yml, init.sh).
- `/lms`: Chứa mã nguồn logic xử lý bài học, bài tập.
- `/frontend`: Giao diện người dùng (React/Vue).

## 🆘 Khắc phục lỗi thường gặp
- **Lỗi Port 8000 already in use**: Chạy `docker compose down` trước khi `up` lại.
- **Lỗi kết nối MariaDB**: Đợi thêm 30 giây để Database khởi động hoàn toàn rồi mới truy cập web.

---

## 💾 PHẦN 7: Cách lưu lại thay đổi (Git Commit)
Để lưu lại và gửi code lên GitHub, hãy dùng bộ lệnh:

```bash
# 1. Thêm thay đổi
git add .

# 2. Ghi chú (Thay tin nhắn bên trong ngoặc kép)
git commit -m "Mô tả việc bạn đã làm"

# 3. Đẩy lên GitHub
git push
```

*Nếu Git hỏi tên/email, hãy chạy:*
- `git config --global user.email "your@email.com"`
- `git config --global user.name "Your Name"`

---
**Chúc bạn có một buổi Demo Hackathon thành công!** 🎯
