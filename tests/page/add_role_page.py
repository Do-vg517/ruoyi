from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.page.base_page import BasePage

class AddRolePage(BasePage):
    """新增角色页面"""
    
    # 基本信息
    role_name_input = (By.ID, "roleName")
    role_key_input = (By.ID, "roleKey")
    role_sort_input = (By.ID, "roleSort")
    remark_input = (By.ID, "remark")
    
    # 状态开关
    status_switch = (By.CLASS_NAME, "toggle-switch")
    
    # 底部按钮 (Layer 弹窗按钮在父页面，此处定义仅作参考或用于非 Layer 模式)
    # submit_btn = (By.XPATH, "//button[contains(@onclick, 'submitHandler')]")
    
    def is_loaded(self, timeout=10):
        """验证页面是否加载完成"""
        try:
            return self.find(*self.role_name_input, timeout=timeout) is not None
        except Exception:
            return False

    def set_role_name(self, name):
        self.type(*self.role_name_input, text=name)
        return self

    def set_role_key(self, key):
        self.type(*self.role_key_input, text=key)
        return self

    def set_role_sort(self, sort):
        self.type(*self.role_sort_input, text=sort)
        return self

    def set_remark(self, remark):
        self.type(*self.remark_input, text=remark)
        return self

    def fill_role_info(self, data):
        """
        一键填写角色信息
        :param data: 字典，包含 role_name, role_key, role_sort, remark 等
        """
        if "role_name" in data:
            self.set_role_name(data["role_name"])
        if "role_key" in data:
            self.set_role_key(data["role_key"])
        if "role_sort" in data:
            self.set_role_sort(data["role_sort"])
        if "remark" in data:
            self.set_remark(data["remark"])
        return self

    def submit(self):
        """提交表单"""
        try:
            # 切换到主文档以点击 Layer 弹窗的确定按钮
            self.driver.switch_to.default_content()
            
            # 定位并点击确定按钮 (layui-layer-btn0 是 Layer 弹窗默认的确定按钮 class)
            # 使用显式等待确保按钮可点击
            confirm_btn = (By.CLASS_NAME, "layui-layer-btn0")
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(confirm_btn)
            ).click()
            
        except Exception as e:
            self.logger.error(f"Submit role form failed: {e}")
            raise
        return self
