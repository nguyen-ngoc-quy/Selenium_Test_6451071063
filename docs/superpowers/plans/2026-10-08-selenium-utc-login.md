# Kế hoạch Kiểm thử Tự động Trang Đăng nhập UTC bằng Selenium WebDriver 4

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng bộ kiểm thử Web UI tự động hoàn chỉnh cho trang Đăng nhập Văn phòng điện tử UTC (`https://vanphongdientu.utc.edu.vn/Login?`) bằng Python & Selenium WebDriver 4 theo mô hình Page Object Model (POM), thực hiện commit riêng từng test case bằng tiếng Việt và đẩy lên GitHub.

**Architecture:** Áp dụng mô hình Page Object Model (POM) tách biệt tầng Page (`BasePage`, `LoginPage`) và tầng Test Script (`test_login.py`). Dùng `pytest` kết hợp `pytest fixture` để quản lý vòng đời WebDriver (khởi tạo Chrome headless mode, Explicit Wait an toàn, đóng trình duyệt sau mỗi test).

**Tech Stack:** Python 3.11+, Selenium WebDriver 4.50+, Pytest 9+, Git / GitHub.

## Global Constraints

- Chạy hoàn toàn trên Selenium WebDriver 4 với Selenium Manager tự động quản lý ChromeDriver.
- Sử dụng Explicit Wait (`WebDriverWait` + `expected_conditions`), tuyệt đối không dùng `time.sleep()`.
- Chạy mặc định ở chế độ `--headless=new` để tương thích máy chủ CI và dòng lệnh.
- Mỗi test case khi hoàn thành phải tạo 1 git commit riêng biệt bằng tiếng Việt.
- Không yêu cầu tài khoản thật của UTC (chỉ kiểm thử tính năng, validation và hành vi trang Login).

## Review Focus

1. **Bẫy checkbox ẩn của jQuery trên trang UTC**: Thẻ `<input type="checkbox" id="persistent">` bị `$(this).hide()` (display: none). Selenium click trực tiếp sẽ ném lỗi `ElementNotInteractableException`. Phải click qua `<label class="check">` hoặc JavaScript click.
2. **Xử lý popup Alert "Thông tin đang cập nhật"**: Khi click vào các thẻ `a.update`, trang hiển thị alert modal, cần bắt hoặc tránh xung đột.
3. **Form validation phía client vs server**: Trang UTC submit POST về `/Login` nếu nhập sai tài khoản sẽ hiển thị thông báo lỗi hoặc giữ nguyên trang login. Cần assert không chuyển hướng sai và thông báo phản hồi phù hợp.
4. **Thời gian tải trang và Explicit Wait timeout**: Máy chủ trường đại học có thể phản hồi chậm hoặc timeout, cần đặt timeout hợp lý (10s - 15s) trên `WebDriverWait`.
5. **Độc lập dữ liệu giữa các test**: Mỗi ca kiểm thử chạy độc lập hoàn toàn với một phiên WebDriver mới, không lưu session cũ.

---

### Task 0: Khởi tạo cấu trúc dự án & Git Repository

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`
- Create: `pages/__init__.py`
- Create: `tests/__init__.py`
- Create: `pages/base_page.py`
- Create: `pages/login_page.py`
- Create: `tests/conftest.py`

**Interfaces:**
- `BasePage(driver: WebDriver, timeout: int = 10)`: cung cấp `open(url)`, `find(locator)`, `click(locator)`, `type_text(locator, text)`, `get_text(locator)`, `get_attribute(locator, attr)`, `is_displayed(locator)`.
- `LoginPage(BasePage)`: cung cấp locators và nghiệp vụ `login(username, password)`, `get_error_message()`, `toggle_remember_me()`, `click_forgot_password()`, `is_password_masked()`.
- Fixture `driver` trong `tests/conftest.py`: khởi tạo `webdriver.Chrome(options)` với headless mode, dọn dẹp sau test (`driver.quit()`).

- [ ] **Step 1: Khởi tạo Git repository và cấu hình .gitignore**
- [ ] **Step 2: Viết BasePage và LoginPage cơ bản**
- [ ] **Step 3: Viết conftest.py với Chrome WebDriver 4 fixture**
- [ ] **Step 4: Kiểm tra chạy thử fixture với pytest**
- [ ] **Step 5: Commit khởi tạo dự án**
  - Commit message: `chore: khởi tạo cấu trúc dự án kiểm thử Selenium WebDriver 4 theo mô hình POM`

---

### Task 1: TC01 - Kiểm tra hiển thị giao diện và các thành phần chính trang Đăng nhập

**Files:**
- Modify: `pages/login_page.py`
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc01_login_page_ui_components_displayed`**
  - Kiểm tra tiêu đề trang (title: "Đăng nhập")
  - Kiểm tra các phần tử hiển thị: ô Tên đăng nhập, ô Mật khẩu, nút Đăng nhập, checkbox Ghi nhớ, link Quên mật khẩu, nút Đăng nhập email UTC, slogan
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc01): kiểm thử hiển thị giao diện và các thành phần trang đăng nhập`

---

### Task 2: TC02 - Kiểm tra đăng nhập khi để trống cả Tên đăng nhập và Mật khẩu

**Files:**
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc02_login_empty_credentials`**
  - Để trống username và password, click nút "Đăng nhập"
  - Kiểm tra URL vẫn ở trang Login và hiển thị thông báo lỗi yêu cầu nhập thông tin
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc02): kiểm thử đăng nhập để trống cả tên đăng nhập và mật khẩu`

---

### Task 3: TC03 - Kiểm tra đăng nhập khi chỉ nhập Tên đăng nhập (để trống Mật khẩu)

**Files:**
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc03_login_empty_password`**
  - Nhập username hợp lệ (vd: `student_utc`), bỏ trống ô mật khẩu, click "Đăng nhập"
  - Xác minh hệ thống không đăng nhập thành công, cảnh báo thiếu mật khẩu
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc03): kiểm thử đăng nhập khi chỉ nhập tên đăng nhập`

---

### Task 4: TC04 - Kiểm tra đăng nhập khi chỉ nhập Mật khẩu (để trống Tên đăng nhập)

**Files:**
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc04_login_empty_username`**
  - Bỏ trống username, nhập password bất kỳ, click "Đăng nhập"
  - Xác minh hệ thống chặn đăng nhập, cảnh báo thiếu tên tài khoản
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc04): kiểm thử đăng nhập khi chỉ nhập mật khẩu`

---

### Task 5: TC05 - Kiểm tra tính năng bảo mật che giấu ký tự mật khẩu

**Files:**
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc05_password_field_masked`**
  - Kiểm tra trường mật khẩu có thuộc tính `type="password"`
  - Nhập dữ liệu và xác minh ký tự không bị lộ dưới dạng plain text
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc05): kiểm thử trường mật khẩu được che giấu bảo mật`

---

### Task 6: TC06 - Kiểm tra đăng nhập với thông tin tài khoản không hợp lệ

**Files:**
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc06_login_invalid_credentials`**
  - Nhập username và password giả định sai (vd: `invalid_user_utc` / `wrong_password_999`), click "Đăng nhập"
  - Xác minh hệ thống từ chối đăng nhập và hiển thị thông báo lỗi xác thực
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc06): kiểm thử đăng nhập với tài khoản hoặc mật khẩu không hợp lệ`

---

### Task 7: TC07 - Kiểm tra đăng nhập với dữ liệu chứa toàn khoảng trắng (whitespace)

**Files:**
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc07_login_whitespace_credentials`**
  - Nhập chuỗi toàn khoảng trắng `"    "` vào username và password, click "Đăng nhập"
  - Xác minh hệ thống xử lý khoảng trắng như trường rỗng hoặc báo lỗi dữ liệu không hợp lệ
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc07): kiểm thử đăng nhập với dữ liệu chứa toàn khoảng trắng`

---

### Task 8: TC08 - Kiểm tra tương tác với Checkbox "Giữ tôi luôn đăng nhập" (Xử lý bẫy checkbox ẩn)

**Files:**
- Modify: `pages/login_page.py`
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc08_remember_me_checkbox_interaction`**
  - Tương tác với label của checkbox bị ẩn bởi jQuery
  - Xác minh trạng thái `isSelected()` / checked được thay đổi chính xác
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc08): kiểm thử tương tác với checkbox ghi nhớ đăng nhập`

---

### Task 9: TC09 - Kiểm tra submit form đăng nhập bằng phím Enter

**Files:**
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc09_login_submit_with_enter_key`**
  - Nhập thông tin và gửi phím `Keys.ENTER` tại ô mật khẩu
  - Xác minh form được submit bình thường
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc09): kiểm thử gửi form đăng nhập bằng phím Enter`

---

### Task 10: TC10 - Kiểm tra điều hướng liên kết "Bạn quên mật khẩu đăng nhập ?"

**Files:**
- Modify: `tests/test_login.py`

- [ ] **Step 1: Viết test case `test_tc10_forgot_password_navigation`**
  - Click vào link "Bạn quên mật khẩu đăng nhập ?"
  - Xác minh URL chuyển hướng tới `/Login/GetPass` và trang hiển thị thành công
- [ ] **Step 2: Chạy kiểm thử xác minh PASS**
- [ ] **Step 3: Commit Git**
  - Commit message: `feat(tc10): kiểm thử điều hướng liên kết quên mật khẩu`

---

### Task 11: Hoàn thiện tài liệu README & Đẩy toàn bộ lên GitHub

**Files:**
- Create: `README.md`

- [ ] **Step 1: Tạo tài liệu `README.md` mô tả dự án, công nghệ, danh sách test case và hướng dẫn chạy test**
- [ ] **Step 2: Commit README.md bằng tiếng Việt**
  - Commit message: `docs: hoàn thiện tài liệu hướng dẫn chạy kiểm thử tự động trong README.md`
- [ ] **Step 3: Kết nối remote GitHub và đẩy toàn bộ lịch sử commit lên GitHub**
  - Lệnh: `git push -u origin main` (hoặc cấu hình remote theo URL của bạn)
