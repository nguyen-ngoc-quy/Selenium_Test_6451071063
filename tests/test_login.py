import pytest
from pages.login_page import LoginPage


def test_tc01_login_page_ui_components_displayed(driver):
    """TC01: Kiểm tra hiển thị đầy đủ giao diện và các thành phần chính trên trang Đăng nhập UTC."""
    login_page = LoginPage(driver)
    login_page.load()

    # 1. Kiểm tra tiêu đề trang
    assert "Đăng nhập" in login_page.get_title(), "Tiêu đề trang không chứa 'Đăng nhập'"

    # 2. Kiểm tra hiển thị các trường nhập liệu và nút đăng nhập
    assert login_page.is_displayed(login_page.USERNAME_INPUT), "Ô Tên đăng nhập không hiển thị"
    assert login_page.is_displayed(login_page.PASSWORD_INPUT), "Ô Mật khẩu không hiển thị"
    assert login_page.is_displayed(login_page.LOGIN_BUTTON), "Nút Đăng nhập không hiển thị"

    # 3. Kiểm tra các nút/liên kết hỗ trợ
    assert login_page.is_displayed(login_page.GOOGLE_LOGIN_BUTTON), "Nút Đăng nhập bằng e-mail UTC không hiển thị"
    assert login_page.is_displayed(login_page.FORGOT_PASSWORD_LINK), "Liên kết Quên mật khẩu không hiển thị"

    # 4. Kiểm tra thành phần nhận diện thương hiệu & banner
    assert login_page.is_displayed(login_page.CAPTION_TITLE), "Tiêu đề slogan không hiển thị"
    assert login_page.find_present(login_page.REMEMBER_CHECKBOX_INPUT) is not None, "Checkbox 'Giữ tôi luôn đăng nhập' không có trong DOM"


def test_tc02_login_empty_credentials(driver):
    """TC02: Kiểm tra đăng nhập khi để trống cả Tên đăng nhập và Mật khẩu."""
    login_page = LoginPage(driver)
    login_page.load()

    # Để trống cả 2 trường và bấm đăng nhập
    login_page.click_login()

    # 1. Xác minh hệ thống vẫn ở trang đăng nhập
    assert "/Login" in login_page.get_current_url(), "Hệ thống chuyển hướng sai khỏi trang đăng nhập"

    # 2. Xác minh hiển thị thông báo lỗi yêu cầu nhập tên đăng nhập
    assert login_page.is_error_displayed(), "Không hiển thị thông báo lỗi khi để trống thông tin"
    error_msg = login_page.get_error_message()
    assert "Bạn chưa nhập tên đăng nhập" in error_msg, f"Nội dung lỗi không chính xác: {error_msg}"


def test_tc03_login_empty_password(driver):
    """TC03: Kiểm tra đăng nhập khi chỉ nhập Tên đăng nhập và để trống Mật khẩu."""
    login_page = LoginPage(driver)
    login_page.load()

    # Nhập username hợp lệ, để trống password
    login_page.enter_username("sinhvien_utc")
    login_page.click_login()

    # 1. Xác minh hệ thống không cho phép đăng nhập
    assert "/Login" in login_page.get_current_url(), "Hệ thống chuyển hướng sai khỏi trang đăng nhập"

    # 2. Xác minh hiển thị thông báo lỗi yêu cầu nhập mật khẩu
    assert login_page.is_error_displayed(), "Không hiển thị thông báo lỗi khi để trống mật khẩu"
    error_msg = login_page.get_error_message()
    assert "Bạn chưa nhập mật khẩu" in error_msg, f"Nội dung lỗi không chính xác: {error_msg}"


def test_tc04_login_empty_username(driver):
    """TC04: Kiểm tra đăng nhập khi chỉ nhập Mật khẩu và để trống Tên đăng nhập."""
    login_page = LoginPage(driver)
    login_page.load()

    # Để trống username, nhập password
    login_page.enter_password("matkhau123")
    login_page.click_login()

    # 1. Xác minh hệ thống không cho phép đăng nhập
    assert "/Login" in login_page.get_current_url(), "Hệ thống chuyển hướng sai khỏi trang đăng nhập"

    # 2. Xác minh hiển thị thông báo lỗi yêu cầu nhập tên đăng nhập
    assert login_page.is_error_displayed(), "Không hiển thị thông báo lỗi khi để trống tên đăng nhập"
    error_msg = login_page.get_error_message()
    assert "Bạn chưa nhập tên đăng nhập" in error_msg, f"Nội dung lỗi không chính xác: {error_msg}"


def test_tc05_password_field_masked(driver):
    """TC05: Kiểm tra tính năng che giấu ký tự bảo mật của trường Mật khẩu."""
    login_page = LoginPage(driver)
    login_page.load()

    # 1. Xác minh ô mật khẩu có type='password'
    assert login_page.is_password_masked(), "Trường Mật khẩu không có thuộc tính type='password'"

    # 2. Nhập mật khẩu và xác minh giá trị không bị đổi sang type text
    login_page.enter_password("SecretP@ssword2026")
    field_type = login_page.get_attribute(login_page.PASSWORD_INPUT, "type")
    assert field_type == "password", f"Thuộc tính type bị thay đổi thành: {field_type}"

    # 3. Kiểm tra placeholder gợi ý đúng 'Mật khẩu'
    placeholder = login_page.get_attribute(login_page.PASSWORD_INPUT, "placeholder")
    assert placeholder == "Mật khẩu", f"Placeholder không chính xác: {placeholder}"


def test_tc06_login_invalid_credentials(driver):
    """TC06: Kiểm tra đăng nhập với tài khoản hoặc mật khẩu không hợp lệ."""
    login_page = LoginPage(driver)
    login_page.load()

    # Nhập thông tin tài khoản sai quy cách / không tồn tại
    login_page.login("user_khong_ton_tai_utc", "matkhau_sai_9999")

    # 1. Xác minh hệ thống từ chối đăng nhập và giữ nguyên tại trang đăng nhập
    assert "/Login" in login_page.get_current_url(), "Hệ thống chuyển hướng sai khi đăng nhập thất bại"

    # 2. Xác minh hiển thị thông báo lỗi từ chối đăng nhập
    assert login_page.is_error_displayed(), "Không hiển thị thông báo lỗi khi thông tin đăng nhập sai"
    error_msg = login_page.get_error_message()
    assert "Tài khoản hoặc mật khẩu không đúng" in error_msg, f"Nội dung lỗi không chính xác: {error_msg}"


def test_tc07_login_whitespace_credentials(driver):
    """TC07: Kiểm tra đăng nhập khi nhập toàn bộ ký tự khoảng trắng."""
    login_page = LoginPage(driver)
    login_page.load()

    # Nhập khoảng trắng vào username và password
    login_page.login("     ", "     ")

    # 1. Xác minh hệ thống không cho phép đăng nhập
    assert "/Login" in login_page.get_current_url(), "Hệ thống chuyển hướng sai khi nhập khoảng trắng"

    # 2. Xác minh hệ thống hiển thị thông báo lỗi
    assert login_page.is_error_displayed(), "Không có thông báo lỗi khi nhập dữ liệu toàn khoảng trắng"
    error_msg = login_page.get_error_message()
    assert len(error_msg.strip()) > 0, "Thông báo lỗi bị rỗng"


def test_tc08_remember_me_checkbox_interaction(driver):
    """TC08: Kiểm tra tương tác với Checkbox 'Giữ tôi luôn đăng nhập' (Xử lý bẫy checkbox ẩn của jQuery)."""
    login_page = LoginPage(driver)
    login_page.load()

    # 1. Kiểm tra trạng thái mặc định ban đầu là uncheck (False)
    assert not login_page.is_remember_me_checked(), "Checkbox mặc định không phải trạng thái uncheck"

    # 2. Click lần 1 qua label đại diện (xử lý bẫy input bị ẩn), trạng thái chuyển sang checked (True)
    login_page.toggle_remember_me()
    assert login_page.is_remember_me_checked(), "Checkbox không được check sau lần click đầu tiên"

    # 3. Click lần 2, trạng thái chuyển lại thành uncheck (False)
    login_page.toggle_remember_me()
    assert not login_page.is_remember_me_checked(), "Checkbox không uncheck sau lần click thứ hai"


def test_tc09_login_submit_with_enter_key(driver):
    """TC09: Kiểm tra gửi form đăng nhập bằng phím Enter từ bàn phím."""
    login_page = LoginPage(driver)
    login_page.load()

    # Nhập thông tin và nhấn Enter thay vì click nút Đăng nhập
    login_page.submit_with_enter(username="test_user_enter", password="test_password_enter")

    # 1. Xác minh form được submit và trang vẫn ở đường dẫn /Login
    assert "/Login" in login_page.get_current_url(), "Hệ thống không xử lý form khi nhấn Enter"

    # 2. Xác minh hiển thị thông báo phản hồi từ máy chủ
    assert login_page.is_error_displayed(), "Không hiển thị thông báo lỗi sau khi submit bằng phím Enter"
    error_msg = login_page.get_error_message()
    assert "Tài khoản hoặc mật khẩu không đúng" in error_msg, f"Thông báo không đúng: {error_msg}"


def test_tc10_forgot_password_navigation(driver):
    """TC10: Kiểm tra điều hướng liên kết 'Bạn quên mật khẩu đăng nhập ?'."""
    login_page = LoginPage(driver)
    login_page.load()

    # Click vào liên kết quên mật khẩu
    login_page.click_forgot_password()

    # 1. Xác minh URL chuyển hướng tới trang khôi phục mật khẩu (/Login/GetPass)
    assert "/Login/GetPass" in login_page.get_current_url(), "Không chuyển hướng đúng tới /Login/GetPass"

    # 2. Xác minh tiêu đề trang khôi phục mật khẩu
    assert "Lấy lại mật khẩu" in login_page.get_title(), "Tiêu đề trang khôi phục mật khẩu không chính xác"
