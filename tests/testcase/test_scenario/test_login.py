import time
import pytest
import allure
from tests.page.login_page import LoginPage
from tests.util_tools.logger import get_logger
from tests.util_tools.data_loader import DataLoader

# 公共参数定义
BASE_URL = "http://localhost:80"

# 全局变量，用于在step之间共享对象

@pytest.mark.parametrize("data", DataLoader.load_yaml("tests/data/test_data.yaml", key="login_data"))
def test_login_localhost(driver, data):
    _driver = driver
    _page = LoginPage(_driver, BASE_URL)
    _logger = get_logger()
    
    @allure.step("打开登录页")
    def step1():
        _page.open_login_page()
        time.sleep(2)  # 强制等待以观察页面打开
        assert _page.is_loaded()
        _logger.info("登录页已加载")

    @allure.step("输入账号与密码")
    def step2():
        _page.set_username(data['username'])
        time.sleep(1)  # 观察输入用户名
        _page.set_password(data['password'])
        time.sleep(1)  # 观察输入密码
        _page.set_remember(True)
        time.sleep(1)  # 观察勾选记住我
     

    @allure.step("点击登录并校验标题")
    def step3():
        _page.submit()
        time.sleep(3)  # 强制等待以观察登录后跳转
        title = _page.get_title()
        _logger.info(f"title: {title}")
        # 根据期望结果进行断言
        assert title == data['expected'], f"登录后标题不是预期的 '{data['expected']}'，而是 '{title}'"
        _logger.info(f"登录测试完成: {data['desc']}")


    step1()
    step2()
    step3()
