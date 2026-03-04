import time
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tests.page.login_page import LoginPage
from tests.page.home_page import HomePage
from tests.page.user_page import UserPage
from tests.page.add_user_page import AddUserPage
from tests.page.edit_user_page import EditUserPage
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
@allure.feature(" 用户管理")
@allure.story("编辑用户")
@allure.title("编辑用户")
@pytest.mark.parametrize("data", DataLoader.load_yaml("tests/data/test_data.yaml", key="edit_user_data"))
def test_edit_user(driver, data):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _user_page = UserPage(driver, BASE_URL)
    _add_user_page = AddUserPage(driver, BASE_URL)
    _edit_user_page = EditUserPage(driver, BASE_URL)
    _logger = get_logger()
    
    # 确保测试数据中的登录账号用于搜索
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

    @allure.step("搜索并编辑用户")
    def step3():
        # 1. 搜索用户
        _user_page.search_user(login_name=SEARCH_LOGIN_NAME)
        time.sleep(2)
        # 2. 检查是否有数据并执行编辑
        try:
            # 检查是否有数据（简单判断页面源码）
            if "No records found" in _driver.page_source or "没有找到匹配的记录" in _driver.page_source:
                _logger.warning(f"用户 {SEARCH_LOGIN_NAME} 不存在，跳过编辑操作")
                return

            # 尝试选中第一行复选框
            try:
                first_checkbox = _driver.find_element(By.CSS_SELECTOR, "table#bootstrap-table tbody tr:first-child input[type='checkbox']")
                if not first_checkbox.is_selected():
                    first_checkbox.click()
            except Exception:
                _logger.error("无法选中第一行，可能定位失败")
                raise
            _user_page.click_edit()
            time.sleep(2)
            _logger.info("点击修改用户按钮")
            _driver.switch_to.default_content()
            
            # 显式等待并切换到编辑用户 iframe
            try:
                WebDriverWait(_driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/user/edit']"))
                )
                _logger.info("成功切换到编辑用户iframe")
            except Exception as e:
                _logger.error(f"切换编辑用户iframe失败: {e}")
                raise
            
            assert _edit_user_page.is_loaded()
            _logger.info("编辑用户弹窗加载完成")
            
            # 填写修改信息
            _edit_user_page.fill_user_info(data)
            time.sleep(1)
            _edit_user_page.submit()
            _logger.info("提交修改用户表单")
        except Exception as e:
            _logger.error(f"编辑用户流程失败: {e}")
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
