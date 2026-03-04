from selenium.webdriver.common.by import By
from tests.page.base_page import BasePage


class HomePage(BasePage):
    # 侧边栏菜单区域
    side_menu = (By.ID, "side-menu")
    # 顶部导航
    navbar = (By.CLASS_NAME, "navbar-static-side")
    # 用户头像区域
    user_panel = (By.CLASS_NAME, "user-panel")
    # 注销按钮
    logout_btn = (By.CSS_SELECTOR, "a[href*='logout']")
    # 个人中心
    profile_link = (By.CSS_SELECTOR, "a[href*='profile']")

    def is_loaded(self, timeout=10):
        """验证首页是否加载完成"""
        try:
            return self.find(*self.side_menu, timeout=timeout) is not None
        except Exception:
            return False

    def get_user_info(self):
        """获取当前登录用户信息"""
        try:
            panel = self.find(*self.user_panel)
            return panel.text
        except Exception as e:
            self.logger.error(f"Get user info failed: {e}")
            raise

    def click_menu(self, menu_name):
        """点击一级菜单"""
        try:
            # 使用XPath定位包含特定文本的菜单项
            xpath = f"//ul[@id='side-menu']//span[contains(text(), '{menu_name}')]/.."
            self.click(By.XPATH, xpath)
        except Exception as e:
            self.logger.error(f"Click menu '{menu_name}' failed: {e}")
            raise
        
    def click_submenu(self, submenu_name):
        """点击二级菜单"""
        try:
            # 使用XPath定位包含特定文本的二级菜单项
            xpath = f"//ul[@id='side-menu']//a[contains(text(), '{submenu_name}')]"
            self.click(By.XPATH, xpath)
        except Exception as e:
            self.logger.error(f"Click submenu '{submenu_name}' failed: {e}")
            raise

    def click_system_management(self):
        """点击系统管理"""
        try:
            self.click_menu("系统管理")
        except Exception as e:
            self.logger.error(f"Click system management failed: {e}")
            raise

    def logout(self):
        """注销登录"""
        try:
            self.click(*self.logout_btn)
        except Exception as e:
            self.logger.error(f"Logout failed: {e}")
            raise

    def go_to_profile(self):
        """进入个人中心"""
        try:
            self.click(*self.profile_link)
        except Exception as e:
            self.logger.error(f"Go to profile failed: {e}")
            raise
