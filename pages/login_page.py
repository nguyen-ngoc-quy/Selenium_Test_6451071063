from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object cho trang Đăng nhập Văn phòng điện tử UTC (https://vanphongdientu.utc.edu.vn/Login?)."""

    URL = "https://vanphongdientu.utc.edu.vn/Login?"

    # --- Locators ---
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "userpwd")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input.submit_login")

    # Checkbox "Giữ tôi luôn đăng nhập" và Label thay thế (xử lý bẫy checkbox ẩn của jQuery)
    REMEMBER_CHECKBOX_INPUT = (By.ID, "persistent")
    REMEMBER_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='persistent']")

    # Các liên kết & nút khác trên trang
    GOOGLE_LOGIN_BUTTON = (By.XPATH, "//a[contains(text(), 'Đăng nhập bằng e-mail UTC')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(@href, '/Login/GetPass')]")

    # Banner & Caption
    CAPTION_TITLE = (By.CSS_SELECTOR, ".caption h1")
    CAPTION_SUBTITLE = (By.CSS_SELECTOR, ".caption span")
    BANNER_IMAGE = (By.CSS_SELECTOR, ".left img")

    # Footer
    HELP_CENTER_LINK = (By.XPATH, "//a[contains(@href, 'hotrokythuat.utc.edu.vn')]")
    FEEDBACK_LINK = (By.XPATH, "//a[contains(@href, 'mailto:hotrokythuat@utc.edu.vn')]")

    # Thông báo lỗi từ hệ thống
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.error")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def load(self) -> None:
        """Truy cập trang đăng nhập."""
        self.open(self.URL)

    def enter_username(self, username: str) -> None:
        """Nhập tên đăng nhập."""
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Nhập mật khẩu."""
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """Bấm nút Đăng nhập."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Hành động nghiệp vụ: Điền thông tin và bấm đăng nhập."""
        if username:
            self.enter_username(username)
        if password:
            self.enter_password(password)
        self.click_login()

    def submit_with_enter(self, username: str = "", password: str = "") -> None:
        """Nhập thông tin và submit form bằng phím Enter tại ô password."""
        if username:
            self.enter_username(username)
        pwd_elem = self.find(self.PASSWORD_INPUT)
        pwd_elem.clear()
        if password:
            pwd_elem.send_keys(password)
        pwd_elem.send_keys(Keys.ENTER)

    def is_remember_me_checked(self) -> bool:
        """Kiểm tra trạng thái checkbox 'Giữ tôi luôn đăng nhập' trong DOM."""
        checkbox = self.find_present(self.REMEMBER_CHECKBOX_INPUT)
        return checkbox.is_selected()

    def toggle_remember_me(self) -> None:
        """Click nhãn của checkbox để chuyển đổi trạng thái (tránh lỗi ẩn jQuery)."""
        label = self.find(self.REMEMBER_CHECKBOX_LABEL)
        label.click()

    def click_forgot_password(self) -> None:
        """Bấm vào link 'Bạn quên mật khẩu đăng nhập ?'."""
        self.click(self.FORGOT_PASSWORD_LINK)

    def is_password_masked(self) -> bool:
        """Kiểm tra ô mật khẩu có thuộc tính type='password' bảo mật hay không."""
        field_type = self.get_attribute(self.PASSWORD_INPUT, "type")
        return field_type == "password"

    def get_error_message(self) -> str:
        """Lấy nội dung thông báo lỗi hiển thị trên form."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Kiểm tra có hiển thị thông báo lỗi hay không."""
        return self.is_displayed(self.ERROR_MESSAGE)
