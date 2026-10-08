import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    """Khởi tạo Chrome WebDriver 4 ở chế độ Headless và đóng sạch sẽ sau mỗi test."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")

    # Selenium 4 tự động quản lý ChromeDriver thông qua Selenium Manager
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)  # Tuyệt đối dùng Explicit Wait, không dùng implicit wait lẫn lộn

    yield browser

    browser.quit()
