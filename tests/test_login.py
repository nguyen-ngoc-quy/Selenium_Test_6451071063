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
