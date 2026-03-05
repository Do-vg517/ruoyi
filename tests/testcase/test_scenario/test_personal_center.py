
import time
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tests.page.login_page import LoginPage
from tests.page.home_page import HomePage
from tests.page.personal_center_page import PersonalCenterPage
from tests.util_tools.logger import get_logger
from tests.util_tools.data_loader import DataLoader

# 公共参数定义
BASE_URL = "http://localhost:80"
USERNAME = "ry"
PASSWORD = "admin123"

@pytest.mark.ui
@allure.feature("个人中心")
@allure.story("修改基本资料")
@allure.title("修改基本资料")
def test_update_user_info(driver):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _personal_page = PersonalCenterPage(driver, BASE_URL)
    _logger = get_logger()
    
    @allure.step("登录系统")
    def step1():
        _logger.info("step1: 开始登录")
        _login_page.open_login_page()
        # time.sleep(1)
        _login_page.login(USERNAME, PASSWORD)
        # time.sleep(2)
        _logger.info("执行登录操作")

    @allure.step("进入个人中心")
    def step2():
        _logger.info("step2: 进入个人中心")
        _home_page.go_to_profile()
        time.sleep(2)
        
        # 显式等待并切换到个人中心iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user/profile']"))
            )
            _logger.info("成功切换到个人中心iframe")
        except Exception as e:
            _logger.error(f"切换个人中心iframe失败: {e}")
            raise

    @allure.step("修改基本资料并保存")
    def step3():
        try:
            _personal_page.update_user_info(
                "若依",
                "15888887777",
                "ruoyi@163.com",
                "1"
            )
            _logger.info("点击保存按钮")
            _personal_page.verify_operation_success()
            _logger.info("修改基本资料成功")
        except Exception as e:
            _logger.error(f"修改基本资料失败: {e}")
            raise

    @allure.step("修改密码")
    def step4():
        _logger.info("step4: 修改密码")
        try:
            # 切换回个人中心iframe (因为step3切回了主文档)
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user/profile']"))
            )
            
            # 修改密码: 旧密码(PASSWORD), 新密码("12345678")
            _personal_page.change_password(PASSWORD, "admin121", "admin121")
            _personal_page.verify_operation_success()
            _logger.info("修改密码成功")
        except Exception as e:
            _logger.error(f"修改密码失败: {e}")
            raise
    try:
        step1()
        step2()
        step3()
        step4()
    except Exception as e:
        _logger.error(f"test_update_user_info 执行异常: {e}")
        raise

@pytest.mark.ui
@allure.feature("个人中心")
@allure.story("新密码登录")
@allure.title("使用新密码登录")
def test_login_new_pwd(driver):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _personal_page = PersonalCenterPage(driver, BASE_URL)
    _logger = get_logger()
    
    @allure.step("使用新密码登录系统")
    def step1():
        _logger.info("step1: 开始登录 (新密码)")
        _login_page.open_login_page()
        _login_page.login(USERNAME, "admin121")
        _logger.info("执行登录操作")
        
        # 验证登录成功 (例如检查首页元素)
        try:
            WebDriverWait(_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "navbar-static-side"))
            )
            _logger.info("验证登录成功")
        except Exception as e:
            _logger.error(f"登录验证失败: {e}")
            raise

    try:
        step1()
    except Exception as e:
        _logger.error(f"test_login_new_pwd 执行异常: {e}")
        raise
    @allure.step("进入个人中心")
    def step2():
        _logger.info("step2: 进入个人中心")
        _home_page.go_to_profile()
        time.sleep(2)
        
        # 显式等待并切换到个人中心iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user/profile']"))
            )
            _logger.info("成功切换到个人中心iframe")
        except Exception as e:
            _logger.error(f"切换个人中心iframe失败: {e}")
            raise
    @allure.step("修改密码")
    def step3():
        try:
            _personal_page.change_password("admin121",PASSWORD ,PASSWORD)
            _personal_page.verify_operation_success()
            _logger.info("修改密码成功")
        except Exception as e:
            _logger.error(f"修改密码失败: {e}")
            raise
    try:
        step2()
        step3()
    except Exception as e:
        _logger.error(f"验证新密码登录异常: {e}")
        raise
