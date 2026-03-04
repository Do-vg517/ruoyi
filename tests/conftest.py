import os
import time
import pytest
import allure
from tests.config.loader import load_settings
from tests.util_tools.logger import get_logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime
import subprocess

 
def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=None)
    parser.addoption("--browser", action="store", default=None)
    parser.addoption("--headless", action="store_true", default=False)
 
 
@pytest.fixture(scope="session")
def settings(pytestconfig):
    s = load_settings()
    if pytestconfig.getoption("--base-url"):
        s["base_url"] = pytestconfig.getoption("--base-url")
    if pytestconfig.getoption("--browser"):
        s["browser"] = pytestconfig.getoption("--browser")
    if pytestconfig.getoption("--headless"):
        s["headless"] = True
    return s


@pytest.fixture(scope="session")
def base_url(settings):
    return settings["base_url"]
 
 
 
 
 
def _make_chrome(headless):
     options = ChromeOptions()
     if headless:
         options.add_argument("--headless=new")
     options.add_argument("--window-size=1920,1080")
     options.add_argument("--disable-gpu")
     options.add_argument("--no-sandbox")
     service = ChromeService(ChromeDriverManager().install())
     return webdriver.Chrome(service=service, options=options)
 
 
def _make_firefox(headless):
     options = FirefoxOptions()
     if headless:
         options.add_argument("-headless")
     service = FirefoxService(GeckoDriverManager().install())
     return webdriver.Firefox(service=service, options=options)
 
 
def _make_edge(headless):
     options = EdgeOptions()
     if headless:
         options.add_argument("--headless=new")
     options.add_argument("--window-size=1920,1080")
     service = EdgeService(EdgeChromiumDriverManager().install())
     return webdriver.Edge(service=service, options=options)
 
 
@pytest.fixture(scope="session", autouse=True)
def _init_logging():
    get_logger()
    return True


@pytest.fixture(scope="function")
def driver(settings):
    browser = settings["browser"].lower()
    headless = settings["headless"]
    if browser == "chrome":
        d = _make_chrome(headless)
    elif browser in ("ff", "firefox"):
        d = _make_firefox(headless)
    elif browser == "edge":
        d = _make_edge(headless)
    else:
        d = _make_chrome(headless)
    d.implicitly_wait(5)
    yield d
    try:
        d.quit()
    except Exception:
        pass
 
 
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            try:
                png = drv.get_screenshot_as_png()
                allure.attach(png, name=f"screenshot_{int(time.time())}", attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass

def pytest_sessionfinish(session):
    logger = get_logger()
    """
    所有测试会话结束后自动执行
    """
    # 定义路径
    allure_results_dir = "./allure-results"
    allure_report_dir = "./allure-report"
    
    # 仅在主节点运行（避免多进程重复执行）
    if not hasattr(session.config, 'workerinput'):
        # 检查结果目录是否存在且有内容
        if os.path.exists(allure_results_dir) and os.listdir(allure_results_dir):
            logger.info(f"\n🚀 开始生成测试报告...")
            try:
                # 生成HTML报告
                # 注意：这里使用 shell=True 在 Windows 下可能更稳定，或者确保 allure 在 PATH 中
                subprocess.run(
                    f"allure generate {allure_results_dir} -o {allure_report_dir} --clean",
                    shell=True,
                    check=True
                )
                
                logger.info(f"✅ 报告生成成功！")
                logger.info(f"📁 报告位置: {os.path.abspath(allure_report_dir)}")
                
                # 自动打开报告
                logger.info("正在自动打开报告 (按 Ctrl+C 停止服务)...")                
                subprocess.run(f"allure open {allure_report_dir}", shell=True)
                
            except subprocess.CalledProcessError as e:
                logger.error(f"\n❌ 报告生成失败: {e}")
            except FileNotFoundError:
                logger.error("\n❌ 未找到allure命令，请确保allure已安装并配置环境变量")
        else:
            logger.warning(f"\n⚠️ 未找到测试结果数据: {allure_results_dir}")
