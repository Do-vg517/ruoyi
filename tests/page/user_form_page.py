from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.page.base_page import BasePage
from tests.page.dept_select_page import DeptSelectPage

class UserFormPage(BasePage):
    """用户表单页面基类，封装新增和编辑用户的公共元素与操作"""
    
    # 基本信息
    user_name_input = (By.NAME, "userName")
    login_name_input = (By.ID, "loginName")
    password_input = (By.ID, "password")
    email_input = (By.ID, "email")
    phonenumber_input = (By.ID, "phonenumber")
    
    # 部门选择
    dept_input = (By.ID, "treeId")
    dept_name_input = (By.ID, "treeName")
    
    # 状态
    status_switch = (By.CLASS_NAME, "toggle-switch")
    
    # 底部按钮
    submit_btn = (By.XPATH, "//button[contains(@onclick, 'submitHandler')]")
    close_btn = (By.XPATH, "//button[contains(@onclick, 'closeItem')]")

    # 定义当前页面的 iframe src 特征，子类需覆盖
    IFRAME_SRC_PATTERN = ""

    def is_loaded(self, timeout=10):
        """验证页面是否加载完成"""
        try:
            return self.find(*self.user_name_input, timeout=timeout) is not None
        except Exception:
            return False

    def set_user_name(self, name):
        self.type(*self.user_name_input, text=name)
        return self

    def set_login_name(self, name):
        # 登录账号在编辑页面可能是只读的，视具体情况而定
        self.type(*self.login_name_input, text=name)
        return self

    def set_password(self, password):
        self.type(*self.password_input, text=password)
        return self

    def set_email(self, email):
        self.type(*self.email_input, text=email)
        return self

    def set_phonenumber(self, number):
        self.type(*self.phonenumber_input, text=number)
        return self

    def select_dept(self, dept_name):
        """选择部门"""
        # 点击部门输入框
        self.click(*self.dept_name_input)
        
        # 切换到默认内容以定位 layer iframe (若依通常在顶层弹出)
        self.driver.switch_to.default_content()

        try:
            # 显式等待并切换到部门选择 iframe
            # URL 包含 selectDeptTree
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='selectDeptTree']"))
            )
            
            # 操作部门选择
            dept_page = DeptSelectPage(self.driver, self.base_url)
            dept_page.select_dept_by_name(dept_name)
            
            # 切回默认内容以点击 layer 确定按钮
            self.driver.switch_to.default_content()
            
            # 点击确定按钮 (layui-layer-btn0)
            confirm_btn = (By.CLASS_NAME, "layui-layer-btn0")
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(confirm_btn)
            ).click()
            
            # 切回原页面所在的 iframe
            if self.IFRAME_SRC_PATTERN:
                WebDriverWait(self.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe[src*='{self.IFRAME_SRC_PATTERN}']"))
                )
            
        except Exception as e:
            self.logger.error(f"Select dept failed: {e}")
            raise
            
        return self

    def select_role(self, role_value):
        """选择角色"""
        try:
            # 直接点击 Label 元素
            xpath = f"//label[.//input[@name='role' and @value='{role_value}']]"
            self.click(By.XPATH, xpath)
        except Exception as e:
            self.logger.error(f"Select role {role_value} failed: {e}")
            raise
        return self

    def fill_user_info(self, data):
        """
        一键填写用户信息
        :param data: 字典
        """
        if "user_name" in data:
            self.set_user_name(data["user_name"])
        if "login_name" in data:
            self.set_login_name(data["login_name"])
        if "password" in data:
            self.set_password(data["password"])
        if "email" in data:
            self.set_email(data["email"])
        if "phonenumber" in data:
            self.set_phonenumber(data["phonenumber"])
        if "dept" in data:
            self.select_dept(data["dept"])
        if "role" in data:
            self.select_role(data["role"])
        return self

    def submit(self):
        """提交表单"""
        try:
            self.click(*self.submit_btn)
        except Exception as e:
            self.logger.error(f"Submit form failed: {e}")
            raise
        return self
