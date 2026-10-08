from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple


class BasePage:
    """Lớp BasePage cơ sở cho mô hình Page Object Model (POM).
    Quản lý WebDriver và cung cấp các hàm Explicit Wait an toàn.
    """

    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        """Mở trang web theo URL."""
        self.driver.get(url)

    def find(self, locator: Tuple[str, str]) -> WebElement:
        """Tìm phần tử trên trang sau khi đã hiển thị (visibilityOfElementLocated)."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_present(self, locator: Tuple[str, str]) -> WebElement:
        """Tìm phần tử có mặt trong DOM (presenceOfElementLocated), kể cả khi ẩn."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: Tuple[str, str]) -> None:
        """Chờ phần tử có thể click được rồi thực hiện click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator: Tuple[str, str], text: str) -> None:
        """Xóa nội dung cũ và nhập văn bản vào trường nhập liệu."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str]) -> str:
        """Lấy nội dung văn bản của phần tử."""
        return self.find(locator).text

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """Lấy giá trị thuộc tính của phần tử."""
        return self.find(locator).get_attribute(attribute)

    def is_displayed(self, locator: Tuple[str, str]) -> bool:
        """Kiểm tra phần tử có hiển thị trên màn hình không."""
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    def get_title(self) -> str:
        """Lấy tiêu đề trang hiện tại."""
        return self.driver.title

    def get_current_url(self) -> str:
        """Lấy URL hiện tại của trình duyệt."""
        return self.driver.current_url
