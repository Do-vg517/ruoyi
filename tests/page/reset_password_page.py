from selenium.webdriver.common.by import By
from tests.page.base_page import BasePage

class ResetPasswordPage(BasePage):
    """重置密码页面"""
    
    # 假设密码输入框 name 为 password
    password_input = (By.NAME, "password")
    
    # 提交按钮通常是 Layer 弹窗的确定按钮
    submit_btn = (By.CLASS_NAME, "layui-layer-btn0")
    
    def input_password(self, password):
        """输入新密码"""
        self.type(*self.password_input, text=password)
        
    def submit(self):
        """点击确定按钮"""
        # 按钮在主文档中，需要切换回 default_content
        self.driver.switch_to.default_content()
        self.click(*self.submit_btn)
