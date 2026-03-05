from selenium.webdriver.common.by import By
from tests.page.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PersonalCenterPage(BasePage):
    """个人中心页面"""
    
    # 选项卡
    user_info_tab = (By.CSS_SELECTOR, "a[href*='#user_info']")
    change_password_tab = (By.CSS_SELECTOR, "a[href*='#modify_password']")
    
    # 基本资料表单
    user_name_input = (By.NAME, "userName")
    phone_input = (By.NAME, "phonenumber")
    email_input = (By.NAME, "email")
    sex_male_radio = (By.CSS_SELECTOR, "input[name='sex'][value='0']")
    sex_female_radio = (By.CSS_SELECTOR, "input[name='sex'][value='1']")
    save_info_btn = (By.XPATH, "//button[contains(@onclick, 'submitUserInfo')]")
    
    # 修改密码表单
    old_password_input = (By.NAME, "oldPassword")
    new_password_input = (By.NAME, "newPassword")
    confirm_password_input = (By.NAME, "confirmPassword")
    save_pwd_btn = (By.XPATH, "//button[contains(@onclick, 'submitChangPassword')]")
    
    # 头像
    avatar_img = (By.CSS_SELECTOR, ".user-info-head img")
    
    def is_loaded(self, timeout=10):
        """验证页面是否加载完成"""
        try:
            return self.find(*self.user_info_tab, timeout=timeout) is not None
        except Exception:
            return False

    def switch_to_user_info(self):
        """切换到基本资料选项卡"""
        self.click(*self.user_info_tab)
        return self

    def switch_to_change_password(self):
        """切换到修改密码选项卡"""
        self.click(*self.change_password_tab)
        return self

    def update_user_info(self, user_name=None, phone=None, email=None, sex=None):
        """
        修改基本资料
        :param user_name: 用户名称
        :param phone: 手机号码
        :param email: 邮箱
        :param sex: 性别 (0:男, 1:女)
        """
        self.switch_to_user_info()
        
        if user_name:
            self.type(*self.user_name_input, text=user_name)
        if phone:
            self.type(*self.phone_input, text=phone)
        if email:
            self.type(*self.email_input, text=email)
        if sex:
            if str(sex) == '0':
                # 处理iCheck或直接点击radio
                self._click_radio(self.sex_male_radio)
            elif str(sex) == '1':
                self._click_radio(self.sex_female_radio)
                
        self.click(*self.save_info_btn)
        return self

    def change_password(self, old_pwd, new_pwd, confirm_pwd):
        """
        修改密码
        :param old_pwd: 旧密码
        :param new_pwd: 新密码
        :param confirm_pwd: 确认密码
        """
        self.switch_to_change_password()
        
        self.type(*self.old_password_input, text=old_pwd)
        self.type(*self.new_password_input, text=new_pwd)
        self.type(*self.confirm_password_input, text=confirm_pwd)
        
        self.click(*self.save_pwd_btn)
        return self

    def verify_operation_success(self):
        """验证操作成功弹窗并关闭"""
        # 切回主文档查找全局提示
        self.driver.switch_to.default_content() 
        
        # 使用更精确的定位器定位 Layui 弹窗内容
        layer_content_loc = (By.CSS_SELECTOR, ".layui-layer-content")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(layer_content_loc)
        )
        
        content_element = self.driver.find_element(*layer_content_loc)
        if "操作成功" not in content_element.text:
            raise AssertionError(f"Expected '操作成功' in popup content, but got '{content_element.text}'")
        
        # 点击关闭弹窗
        close_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "layui-layer-btn0"))
        )
        close_btn.click()
        return self

    def _click_radio(self, locator):
        """点击单选按钮 (适配iCheck)"""
        element = self.find(*locator)
        # 尝试点击父级 div.iradio-blue 或者 label，或者直接点击 input (如果不可见可能需要用JS)
        try:
            # 尝试查找紧邻的 ins 元素 (iCheck helper)
            parent = element.find_element(By.XPATH, "./..")
            ins = parent.find_element(By.TAG_NAME, "ins")
            ins.click()
        except Exception:
            # 回退到JS点击
            self.driver.execute_script("arguments[0].click();", element)
