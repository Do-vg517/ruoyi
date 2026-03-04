from pathlib import Path
from selenium.webdriver.common.by import By
from tests.page.base_page import BasePage


class LoginPage(BasePage):
    username_input = (By.NAME, "username")
    password_input = (By.NAME, "password")
    remember_checkbox = (By.ID, "rememberme")
    submit_button = (By.ID, "btnSubmit")
    form = (By.ID, "signupForm")

    def open_local_html(self, html_path):
        uri = Path(html_path).resolve().as_uri()
        self.driver.get(uri)
        return self

    def open_login_page(self, url="http://localhost/index"):
        """打开登录页面"""
        self.logger.info(f"正在打开登录页面: {url}")
        self.driver.get(url)
        self.driver.maximize_window()

    def is_loaded(self, timeout=10):
        try:
            el = self.find(*self.form, timeout=timeout)
            return el is not None
        except Exception:
            return False

    def set_username(self, username, timeout=10):
        """输入用户名"""
        try:
            self.type(*self.username_input, text=username, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Set username failed: {e}")
            raise
        return self

    def set_password(self, password, timeout=10):
        """输入密码"""
        try:
            self.type(*self.password_input, text=password, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Set password failed: {e}")
            raise
        return self

    def set_remember(self, remember=True, timeout=10):
        """设置记住我"""
        try:
            cb = self.find(*self.remember_checkbox, timeout=timeout)
            if cb.is_selected() != bool(remember):
                cb.click()
        except Exception as e:
            self.logger.error(f"Set remember me failed: {e}")
            raise
        return self

    def submit(self, timeout=10):
        """提交登录"""
        try:
            self.click(*self.submit_button, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Submit login failed: {e}")
            raise
        return self

    def login(self, username, password, remember=False, timeout=10):
        self.set_username(username, timeout=timeout)
        self.set_password(password, timeout=timeout)
        self.set_remember(remember, timeout=timeout)
        self.submit(timeout=timeout)
        return self
