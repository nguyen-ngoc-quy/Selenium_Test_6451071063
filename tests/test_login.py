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
