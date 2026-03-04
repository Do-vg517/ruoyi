from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.util_tools.logger import get_logger


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.logger = get_logger()

    def open(self, path=""):
        if path:
            url = f"{self.base_url}/{path.lstrip('/')}"
        else:
            url = self.base_url
        self.driver.get(url)
        return self

    def find(self, by, value, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            self.logger.error(f"Failed to find element ({by}, {value}): {e}")
            raise

    def click(self, by, value, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            el = wait.until(EC.element_to_be_clickable((by, value)))
            el.click()
            return el
        except Exception as e:
            self.logger.error(f"Failed to click element ({by}, {value}): {e}")
            raise

    def type(self, by, value, text, timeout=10):
        try:
            el = self.find(by, value, timeout)
            el.clear()
            el.send_keys(text)
            return el
        except Exception as e:
            self.logger.error(f"Failed to type '{text}' into element ({by}, {value}): {e}")
            raise
