# Kiểm thử Tự động Web UI Trang Đăng nhập UTC với Selenium WebDriver 4 & POM

Dự án kiểm thử tự động Web UI cho trang **Đăng nhập Văn phòng điện tử - Trường Đại học Giao thông Vận tải (UTC)**  
URL: [https://vanphongdientu.utc.edu.vn/Login?](https://vanphongdientu.utc.edu.vn/Login?)



---

## 1. Công nghệ & Thư viện sử dụng

- **Ngôn ngữ**: Python 3.11+
- **Framework kiểm thử UI**: Selenium WebDriver 4 (tích hợp sẵn Selenium Manager tự động quản lý ChromeDriver)
- **Test Runner & Framework**: Pytest 9+
- **Mô hình thiết kế**: Page Object Model (POM) tách biệt tầng Page (`BasePage`, `LoginPage`) và tầng Test Script (`test_login.py`)
- **Cơ chế đồng bộ**: Explicit Wait (`WebDriverWait` + `expected_conditions`), tuyệt đối không dùng `time.sleep()`
- **Chế độ chạy**: Hỗ trợ chế độ Headless (`--headless=new`) thích hợp chạy trên dòng lệnh và hệ thống CI/CD (GitHub Actions)

---

## 2. Cấu trúc thư mục

```text
Selenium_Test/
├── pages/
│   ├── __init__.py
│   ├── base_page.py          # Lớp BasePage cung cấp các hàm Explicit Wait an toàn
│   └── login_page.py         # Locators và các hàm nghiệp vụ trên trang Login UTC
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Quản lý vòng đời WebDriver (Chrome headless fixture)
│   └── test_login.py         # 10 test case kiểm thử tự động
├── docs/                     # Kế hoạch và tài liệu kiểm thử
├── requirements.txt          # Danh sách thư viện phụ thuộc
├── .gitignore                # Cấu hình bỏ qua file tạm, môi trường ảo
└── README.md                 # Hướng dẫn chi tiết
```

---

## 3. Danh sách 10 Test Cases

| Mã TC | Tên Test Case | Mô tả & Thao tác | Kết quả mong đợi |
| :--- | :--- | :--- | :--- |
| **TC01** | Kiểm tra hiển thị giao diện và các thành phần chính | Truy cập `https://vanphongdientu.utc.edu.vn/Login?` | Trang tải thành công, tiêu đề "Đăng nhập", đầy đủ input username, password, nút Đăng nhập, checkbox ghi nhớ, link quên mật khẩu, nút đăng nhập email UTC và slogan. |
| **TC02** | Kiểm tra đăng nhập khi để trống cả username và password | Bỏ trống 2 ô, nhấn "Đăng nhập" | Không đăng nhập được, giữ nguyên tại trang Login, hiển thị thông báo: `Bạn chưa nhập tên đăng nhập`. |
| **TC03** | Kiểm tra đăng nhập khi chỉ nhập username | Nhập username hợp lệ, để trống ô mật khẩu, nhấn "Đăng nhập" | Không đăng nhập được, hiển thị thông báo lỗi: `Bạn chưa nhập mật khẩu`. |
| **TC04** | Kiểm tra đăng nhập khi chỉ nhập password | Để trống username, nhập password, nhấn "Đăng nhập" | Không đăng nhập được, hiển thị thông báo lỗi: `Bạn chưa nhập tên đăng nhập`. |
| **TC05** | Kiểm tra tính năng che giấu ký tự mật khẩu | Kiểm tra thuộc tính thẻ input password và nhập dữ liệu | Ô mật khẩu có `type="password"`, ký tự nhập vào được mã hóa dấu chấm bảo mật, placeholder hiển thị `"Mật khẩu"`. |
| **TC06** | Kiểm tra đăng nhập thông tin không hợp lệ | Nhập username/password giả định sai, nhấn "Đăng nhập" | Hệ thống từ chối đăng nhập, hiển thị thông báo: `Tài khoản hoặc mật khẩu không đúng`. |
| **TC07** | Kiểm tra đăng nhập với toàn khoảng trắng (whitespace) | Nhập chuỗi toàn dấu cách `"     "` vào cả 2 trường, nhấn "Đăng nhập" | Hệ thống không cho phép đăng nhập và hiển thị thông báo lỗi. |
| **TC08** | Kiểm tra tương tác checkbox "Giữ tôi luôn đăng nhập" (Xử lý bẫy checkbox ẩn của jQuery) | Click qua nhãn `label` đại diện của checkbox ẩn | Trạng thái checkbox chuyển từ `False` (uncheck) sang `True` (checked) và ngược lại khi click lần 2. |
| **TC09** | Kiểm tra gửi form đăng nhập bằng phím Enter | Nhập thông tin và nhấn phím `Enter` tại ô password thay vì click chuột | Form được submit bình thường lên server, nhận phản hồi từ chối hợp lệ. |
| **TC10** | Kiểm tra điều hướng liên kết "Bạn quên mật khẩu đăng nhập ?" | Click vào liên kết Quên mật khẩu | Chuyển hướng thành công sang trang `/Login/GetPass` với tiêu đề `"Lấy lại mật khẩu"`. |

---

## 4. Kỹ thuật nâng cao đã áp dụng (Theo bài giảng Buổi 8)

1. **Xử lý bẫy checkbox ẩn của jQuery trên trang UTC**:
   - Trang UTC sử dụng đoạn script jQuery: `$(this).hide().attr('id', id).after("<label class='check' for='" + id + "'><span></span></label>");` làm cho thẻ `<input type="checkbox">` bị ẩn (`display: none`).
   - Nếu dùng Selenium click trực tiếp vào input sẽ bị lỗi `ElementNotInteractableException`.
   - Giải pháp: Định vị và click thông qua thẻ nhãn đại diện `label[for='persistent']` hoặc `label.check`, sau đó kiểm tra trạng thái trong DOM qua `is_selected()`.

2. **Explicit Wait thay vì Thread.sleep()**:
   - Sử dụng `WebDriverWait` kết hợp `expected_conditions.visibility_of_element_located` và `element_to_be_clickable`.
   - Giúp test script chạy nhanh, ổn định và tránh lỗi bất đồng bộ.

3. **Page Object Model (POM)**:
   - Toàn bộ locators và hành động nghiệp vụ được đóng gói trong `LoginPage`. Khi trang web thay đổi giao diện, chỉ cần sửa đổi class này mà không ảnh hưởng đến kịch bản kiểm thử trong `test_login.py`.

---

## 5. Hướng dẫn cài đặt và Chạy kiểm thử

### Bước 1: Kích hoạt môi trường ảo Python
```bash
# Trên Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Hoặc kích hoạt qua Command Prompt:
.\.venv\Scripts\activate.bat
```

### Bước 2: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy kiểm thử

- **Chạy toàn bộ 10 test case**:
  ```bash
  pytest tests/test_login.py -v
  ```

- **Chạy 1 test case cụ thể (ví dụ TC08)**:
  ```bash
  pytest tests/test_login.py -k "tc08" -v
  ```

- **Xuất báo cáo chi tiết**:
  ```bash
  pytest tests/test_login.py -v --tb=short
  ```
