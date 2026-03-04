import time
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tests.page.login_page import LoginPage
from tests.page.home_page import HomePage
from tests.page.role_page import RolePage
from tests.page.add_role_page import AddRolePage
from tests.page.edit_role_page import EditRolePage
from tests.util_tools.logger import get_logger
from tests.util_tools.data_loader import DataLoader

# 公共参数定义
BASE_URL = "http://localhost:80"
USERNAME = "admin"
PASSWORD = "123456"

@pytest.mark.ui
@allure.feature("角色管理")
@allure.story("新增角色")
@allure.title("新增角色")
@pytest.mark.parametrize("data", DataLoader.load_yaml("tests/data/test_data.yaml", key="add_role_data"))
def test_add_role(driver, data):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _role_page = RolePage(driver, BASE_URL)
    _add_role_page = AddRolePage(driver, BASE_URL)
    _logger = get_logger()

    @allure.step("登录系统")
    def step1():
        _login_page.open_login_page()
        # time.sleep(1)
        _login_page.login(USERNAME, PASSWORD)
        # time.sleep(2)
        _logger.info("执行登录操作")

    @allure.step("进入角色管理页面")
    def step2():
        _home_page.click_system_management()
        time.sleep(1)
        _home_page.click_submenu("角色管理")
        time.sleep(2)
        
        # 显式等待并切换到角色管理iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/role']"))
            )
            _logger.info("成功切换到角色管理iframe")
        except Exception as e:
            _logger.error(f"切换角色管理iframe失败: {e}")
            raise
            

    @allure.step("新增角色并提交")
    def step3():
        _role_page.click_add()
        time.sleep(2)
        _logger.info("点击新增角色按钮")
        
        _driver.switch_to.default_content()
        # 显式等待并切换到新增角色iframe
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/role/add']"))
            )
            _logger.info("成功切换到新增角色iframe")
        except Exception as e:
            _logger.error(f"切换新增角色iframe失败: {e}")
            raise
        
        _add_role_page.fill_role_info(data)
        time.sleep(1)
        _add_role_page.submit()
        _logger.info(f"提交新增角色成功: {data['role_name']}")
        
        # 提交后切回主文档以捕获弹窗 (submit方法已切回，此处确保上下文正确)
        _driver.switch_to.default_content()
        try:
            # 显式等待"操作成功"的提示出现
            success_locator = (By.XPATH, "//*[contains(text(), '操作成功')]")
            WebDriverWait(_driver, 10).until(
                EC.presence_of_element_located(success_locator)
            )
            # 获取提示文本并断言
            success_element = _driver.find_element(*success_locator)
            assert "操作成功" in success_element.text
        except Exception as e:
            _logger.error(f"验证操作成功失败: {e}")
            # allure.attach(_driver.get_screenshot_as_png(), name="assertion_failed", attachment_type=allure.attachment_type.PNG)
            raise

    step1()
    step2()
    step3()

@pytest.mark.ui
@allure.feature("角色管理")
@allure.story("编辑角色")
@allure.title("编辑角色")
@pytest.mark.parametrize("data", DataLoader.load_yaml("tests/data/test_data.yaml", key="edit_role_data"))
def test_edit_role(driver, data):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _role_page = RolePage(driver, BASE_URL)
    _edit_role_page = EditRolePage(driver, BASE_URL)
    _logger = get_logger()

    @allure.step("登录系统并进入角色管理")
    def step1():
        _login_page.open_login_page()
        _login_page.login(USERNAME, PASSWORD)
        _logger.info("执行登录操作")
        _home_page.click_system_management()
        time.sleep(1)
        _home_page.click_submenu("角色管理")
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/role']"))
            )
            _logger.info("成功切换到角色管理iframe")
        except Exception as e:
            _logger.error(f"切换角色管理iframe失败: {e}")
            raise

    @allure.step("搜索并进入角色编辑页面")
    def step2():
        time.sleep(2)
        _role_page.search_role("普通角色user4")
        time.sleep(2)
        _logger.info("搜索角色: 普通角色user4")
        
        # 检查是否有数据
        if "No records found" in _driver.page_source or "没有找到匹配的记录" in _driver.page_source:
            _logger.warning(f"角色 普通角色user4 不存在，跳过编辑操作")
            return

        # 选中并点击编辑
        try:
            first_checkbox = _driver.find_element(By.CSS_SELECTOR, "table#bootstrap-table tbody tr:first-child input[type='checkbox']")
            if not first_checkbox.is_selected():
                first_checkbox.click()
            _role_page.click_edit()
            time.sleep(2)
            _logger.info("点击编辑按钮")
        except Exception as e:
            _logger.error(f"点击编辑按钮失败: {e}")
            raise
        
        _driver.switch_to.default_content()
        # 切换到编辑角色iframe (src包含 /system/role/edit)
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/role/edit']"))
            )
            _logger.info("成功切换到编辑角色iframe")
        except Exception as e:
            _logger.error(f"切换编辑角色iframe失败: {e}")
            raise

    @allure.step("填写并提交编辑角色信息")
    def step3():
        _edit_role_page.fill_role_info(data)
        time.sleep(1)
        _edit_role_page.submit()
        # 验证操作成功
        _driver.switch_to.default_content()
        try:
            success_locator = (By.XPATH, "//*[contains(text(), '操作成功')]")
            WebDriverWait(_driver, 10).until(
                EC.presence_of_element_located(success_locator)
            )
            success_element = _driver.find_element(*success_locator)
            assert "操作成功" in success_element.text
            _logger.info("编辑操作成功")
        except Exception as e:
            _logger.error(f"编辑操作失败: {e}")
            raise
    step1()
    step2()
    step3()


@pytest.mark.ui
@allure.feature("角色管理")
@allure.story("删除角色")
@allure.title("删除角色")
@pytest.mark.parametrize("data", DataLoader.load_yaml("tests/data/test_data.yaml", key="delete_role_data"))
def test_delete_role(driver, data):
    _driver = driver
    _login_page = LoginPage(driver, BASE_URL)
    _home_page = HomePage(driver, BASE_URL)
    _role_page = RolePage(driver, BASE_URL)
    _logger = get_logger()

    @allure.step("登录系统并进入角色管理")
    def step1():
        _login_page.open_login_page()
        _login_page.login(USERNAME, PASSWORD)
        _home_page.click_system_management()
        time.sleep(1)
        _home_page.click_submenu("角色管理")
        time.sleep(1)
        
        try:
            WebDriverWait(_driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='/system/role']"))
            )
        except Exception as e:
            _logger.error(f"切换角色管理iframe失败: {e}")
            raise

    @allure.step("搜索并删除角色")
    def step2():
        _role_page.search_role(role_name=data["role_name"])
        time.sleep(1)
        _logger.info(f"搜索角色: {data['role_name']}")
        
        if "No records found" in _driver.page_source or "没有找到匹配的记录" in _driver.page_source:
            _logger.error(f"角色 {data['role_name']} 不存在，跳过删除操作")
            return

        try:
            first_checkbox = _driver.find_element(By.CSS_SELECTOR, "table#bootstrap-table tbody tr:first-child input[type='checkbox']")
            if not first_checkbox.is_selected():
                first_checkbox.click()
            
            _role_page.click_remove()
            time.sleep(1)
            _logger.info("点击删除按钮")
            
            _driver.switch_to.default_content()
            confirm_btn = WebDriverWait(_driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "layui-layer-btn0"))
            )
            confirm_btn.click()
            _logger.info("点击确认删除")
            
            success_locator = (By.XPATH, "//*[contains(text(), '操作成功')]")
            WebDriverWait(_driver, 10).until(
                EC.presence_of_element_located(success_locator)
            )
            assert "操作成功" in _driver.find_element(*success_locator).text
            _logger.info("删除角色操作成功")
            
        except Exception as e:
            _logger.error(f"删除角色操作失败: {e}")
            raise

    step1()
    step2()


