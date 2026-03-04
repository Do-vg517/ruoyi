import pytest
import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tests.page.login_page import LoginPage
from tests.page.home_page import HomePage
from tests.page.user_page import UserPage
from tests.page.reset_password_page import ResetPasswordPage
from tests.util_tools.logger import get_logger
from tests.util_tools.data_loader import DataLoader

# 公共参数定义
BASE_URL = "http://localhost:80"
USERNAME = "admin"
PASSWORD = "123456"

@pytest.mark.ui
@allure.feature("用户管理")
@allure.story("新增用户")
@allure.title("新增用户")
@pytest.mark.parametrize("data", DataLoader.load_yaml("tests/data/test_data.yaml", key="add_user_data"))
def test_add_user(driver, data):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _user_page = UserPage(driver, BASE_URL)
    _add_user_page = AddUserPage(driver, BASE_URL)
    _logger = get_logger()
    @allure.step("登录系统")
    def step1():
        _login_page.open_login_page()
        time.sleep(1)
        _login_page.login(USERNAME, PASSWORD)
        time.sleep(2)
        _logger.info("执行登录操作")

    @allure.step("进入用户管理页面")
    def step2():
        _home_page.click_system_management()
        time.sleep(1)
        _home_page.click_submenu("用户管理")
        time.sleep(2)
        
        # 显式等待并切换到用户管理iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user']"))
            )
            _logger.info("成功切换到用户管理iframe")
        except Exception as e:
            _logger.error(f"切换用户管理iframe失败: {e}")
            raise
            
        assert _user_page.is_loaded()
        _logger.info("进入用户管理页面")

    @allure.step("新增用户并提交")
    def step3():
        _user_page.click_add()
        time.sleep(2)
        _logger.info("点击新增用户按钮")
        
        _driver.switch_to.default_content()
        # 显式等待并切换到新增用户iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user/add']"))
            )
            _logger.info("成功切换到新增用户iframe")
        except Exception as e:
            _logger.error(f"切换新增用户iframe失败: {e}")
            # 截图以便调试
            raise
        
        assert _add_user_page.is_loaded()
        _logger.info("新增用户弹窗加载完成")
        
        _add_user_page.fill_user_info(data)
        time.sleep(1)
        _add_user_page.submit()
        _logger.info(f"提交新增用户表单: {data['user_name']}")

    step1()
    step2()
    step3()

@pytest.mark.ui
@allure.feature("用户管理")
@allure.story("重置密码")
@allure.title("重置密码")
@pytest.mark.parametrize("data", DataLoader.load_yaml("tests/data/test_data.yaml", key="reset_pwd_data"))
def test_reset_password(driver, data):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _user_page = UserPage(driver, BASE_URL)
    _reset_pwd_page = ResetPasswordPage(driver, BASE_URL)
    _logger = get_logger()

    @allure.step("登录并进入用户管理页面")
    def step1():
        _login_page.open_login_page()
        _login_page.login(USERNAME, PASSWORD)
        _home_page.click_system_management()
        time.sleep(1)
        _home_page.click_submenu("用户管理")
        
        # 切换到用户管理iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user']"))
            )
        except Exception as e:
            _logger.error(f"切换用户管理iframe失败: {e}")
            raise

    @allure.step("搜索用户并点击重置密码")
    def step2():
        _user_page.search_user(login_name=data["login_name"])
        time.sleep(1)
        try:
            # 1. 先定位到目标行
            row_xpath = f"//table[@id='bootstrap-table']//tbody//tr[contains(., '{data['login_name']}')]"
            row = _driver.find_element(By.XPATH, row_xpath)
            
            # 2. 定位该行内的“更多操作”按钮并点击
            # 注意：Bootstrap Table 的“更多”按钮通常是一个 a 标签或者 button，包含 '更多操作' 文字
            more_btn = row.find_element(By.XPATH, ".//a[contains(., '更多操作')]")
            _driver.execute_script("arguments[0].scrollIntoView(true);", more_btn)
            time.sleep(0.5)
            more_btn.click()
            _logger.info("点击更多操作按钮")
            
            # 弹出菜单通常在 body 下或者 row 附近，使用全局 XPath 查找可见的“重置密码”按钮
            reset_btn_xpath = "//a[contains(@onclick, 'resetPwd') and contains(text(), '重置密码')]"
            reset_btn = WebDriverWait(_driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, reset_btn_xpath))
            )
            reset_btn.click()
            _logger.info("点击重置密码按钮")
        except Exception as e:
            _logger.error(f"进入重置密码页面失败: {e}")
            raise
            
        _driver.switch_to.default_content()
        # 切换到重置密码iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user/resetPwd']"))
            )
            _logger.info("成功切换到重置密码iframe")
        except Exception as e:
            _logger.error(f"切换重置密码iframe失败: {e}")
            raise

    @allure.step("输入新密码并提交")
    def step3():
        _reset_pwd_page.input_password(data["new_password"])
        # submit会切换回default_content点击按钮
        time.sleep(1)
        _reset_pwd_page.submit()
        time.sleep(1)
        # 验证成功提示
        success_locator = (By.XPATH, "//*[contains(text(), '操作成功')]")
        try:
            WebDriverWait(_driver, 10).until(
                EC.presence_of_element_located(success_locator)
            )
            msg = _driver.find_element(*success_locator).text
            assert "操作成功" in msg
            _logger.info(f"重置密码成功: {msg}")
        except Exception as e:
             _logger.error(f"验证失败: {e}")
             raise
    step1()
    step2()
    step3()

@pytest.mark.ui
@allure.feature("用户管理")
@allure.story("删除用户")
@allure.title("删除用户")
@pytest.mark.parametrize("data", DataLoader.load_yaml("tests/data/test_data.yaml", key="delete_user_data"))
def test_delete_user(driver, data):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _user_page = UserPage(driver, BASE_URL)
    _logger = get_logger()
    SEARCH_LOGIN_NAME = data.get("login_name", "test_user_01")

    @allure.step("登录系统")
    def step1():
        _login_page.open_login_page()
        time.sleep(1)
        _login_page.login(USERNAME, PASSWORD)
        time.sleep(2)
        _logger.info("执行登录操作")

    @allure.step("进入用户管理页面")
    def step2():
        _home_page.click_system_management()
        time.sleep(1)
        _home_page.click_submenu("用户管理")
        time.sleep(2)
        
        # 显式等待并切换到用户管理iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user']"))
            )
            _logger.info("成功切换到用户管理iframe")
        except Exception as e:
            _logger.error(f"切换用户管理iframe失败: {e}")
            raise
            
        assert _user_page.is_loaded()
        _logger.info("进入用户管理页面")

    
    @allure.step("搜索并删除用户")
    def step3():
        # 1. 搜索用户
        _user_page.search_user(login_name=SEARCH_LOGIN_NAME)
        time.sleep(2)
        
        try:
            if "No records found" in _driver.page_source or "没有找到匹配的记录" in _driver.page_source:
                _logger.warning(f"用户 {SEARCH_LOGIN_NAME} 不存在，跳过删除操作")
                return

            # 尝试选中第一行复选框
            try:
                first_checkbox = _driver.find_element(By.CSS_SELECTOR, "table#bootstrap-table tbody tr:first-child input[type='checkbox']")
                if not first_checkbox.is_selected():
                    first_checkbox.click()
            except Exception:
                _logger.error("无法选中第一行，可能定位失败")
                raise

            _user_page.click_remove()
            time.sleep(1)
            _logger.info("点击删除用户按钮")
            
            # 3. 处理 Layer 确认弹窗
            # 切换到默认内容以定位 layer 弹窗
            _driver.switch_to.default_content()
            
            try:
                # 显式等待 Layer 确认按钮出现
                confirm_btn = WebDriverWait(_driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "layui-layer-btn0"))
                )
                confirm_btn.click()
                _logger.info("点击确认删除")
                
                # 断言操作成功消息
                expected_msg = "操作成功"
                # 显式等待并获取页面源码
                WebDriverWait(_driver, 5).until(lambda d: expected_msg in d.page_source)
                assert expected_msg in _driver.page_source, f"断言失败: 未找到 '{expected_msg}'"

            except Exception as e:
                _logger.error(f"删除确认弹窗处理失败或断言失败: {e}")
                raise
                
            _logger.info(f"执行删除用户操作成功: ")

        except Exception as e:
            _logger.error(f"删除用户流程失败: {e}")
            raise

    step1()
    step2()
    step3()
