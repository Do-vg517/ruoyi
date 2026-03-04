# utils/driver_utils.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import Config
import logging

class DriverUtils:
    """浏览器驱动工具类"""
    
    @staticmethod
    def get_chrome_driver():
        """获取Chrome浏览器驱动"""
        options = webdriver.ChromeOptions()
        
        # 基本配置
        options.add_argument('--start-maximized')  # 最大化窗口
        options.add_argument('--disable-infobars')  # 禁用信息栏
        options.add_argument('--disable-notifications')  # 禁用通知
        options.add_argument('--disable-popup-blocking')  # 禁用弹窗拦截
        options.add_argument('--lang=zh-CN')  # 设置语言
        
        # 无头模式配置
        if Config.HEADLESS:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
        
        # 忽略证书错误
        options.add_argument('--ignore-certificate-errors')
        
        # 添加实验性选项
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            # 使用webdriver-manager自动管理驱动
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            # 设置超时时间
            driver.implicitly_wait(Config.IMPLICITLY_WAIT)
            driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            
            logging.info("Chrome浏览器驱动初始化成功")
            return driver
            
        except Exception as e:
            logging.error(f"Chrome浏览器驱动初始化失败: {str(e)}")
            raise