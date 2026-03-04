from selenium.webdriver.common.by import By
from tests.page.base_page import BasePage


class UserPage(BasePage):
    # 搜索区域
    login_name_input = (By.NAME, "loginName")
    phonenumber_input = (By.NAME, "phonenumber")
    status_select = (By.NAME, "status")
    search_btn = (By.XPATH, "//a[contains(@class, 'btn-primary') and contains(@onclick, 'search')]")
    reset_btn = (By.XPATH, "//a[contains(@class, 'btn-warning') and contains(@onclick, 'reset')]")

    # 工具栏按钮
    add_btn = (By.XPATH, "//a[contains(@class, 'btn-success') and contains(@onclick, 'add')]")
    edit_btn = (By.XPATH, "//a[contains(@class, 'btn-primary') and contains(@onclick, 'edit')]")
    remove_btn = (By.XPATH, "//a[contains(@class, 'btn-danger') and contains(@onclick, 'removeAll')]")
    import_btn = (By.XPATH, "//a[contains(@class, 'btn-info') and contains(@onclick, 'importExcel')]")
    export_btn = (By.XPATH, "//a[contains(@class, 'btn-warning') and contains(@onclick, 'exportExcel')]")

    # 表格区域
    table = (By.ID, "bootstrap-table")
    
    def is_loaded(self, timeout=10):
        """验证用户页面是否加载完成"""
        try:
            return self.find(*self.table, timeout=timeout) is not None
        except Exception:
            return False

    def search_user(self, login_name=None, phonenumber=None, status=None):
        """搜索用户"""
        try:
            if login_name:
                self.type(*self.login_name_input, text=login_name)
            if phonenumber:
                self.type(*self.phonenumber_input, text=phonenumber)
            # 这里简化状态选择，后续可扩展为下拉框操作
            self.click(*self.search_btn)
        except Exception as e:
            self.logger.error(f"Search user failed: {e}")
            raise

    def click_add(self):
        """点击新增按钮"""
        try:
            self.click(*self.add_btn)
        except Exception as e:
            self.logger.error(f"Click add button failed: {e}")
            raise

    def click_edit(self):
        """点击修改按钮"""
        try:
            self.click(*self.edit_btn)
        except Exception as e:
            self.logger.error(f"Click edit button failed: {e}")
            raise

    def click_remove(self):
        """点击删除按钮"""
        try:
            self.click(*self.remove_btn)
        except Exception as e:
            self.logger.error(f"Click remove button failed: {e}")
            raise
