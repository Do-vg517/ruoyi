from selenium.webdriver.common.by import By
from tests.page.base_page import BasePage

class RolePage(BasePage):
    # 搜索区域
    role_name_input = (By.NAME, "roleName")
    role_key_input = (By.NAME, "roleKey")
    status_select = (By.NAME, "status")
    search_btn = (By.XPATH, "//a[contains(text(), '搜索')]")
    reset_btn = (By.XPATH, "//a[contains(text(), '重置')]")

    # 工具栏按钮
    add_btn = (By.XPATH, "//a[contains(@onclick, '$.operate.add()')]")
    edit_btn = (By.XPATH, "//a[contains(@onclick, '$.operate.edit()')]")
    remove_btn = (By.XPATH, "//a[contains(@onclick, '$.operate.removeAll()')]")
    export_btn = (By.XPATH, "//a[contains(@onclick, '$.table.exportExcel()')]")
    # 表格
    table = (By.TAG_NAME, "table")
    
    def is_loaded(self, timeout=10):
        """验证角色管理页面是否加载完成"""
        try:
            return self.find(*self.table, timeout=timeout) is not None
        except Exception:
            return False

    def search_role(self, role_name=None, role_key=None, status=None):
        """
        搜索角色
        :param role_name: 角色名称
        :param role_key: 权限字符
        :param status: 角色状态 ('0': 正常, '1': 停用)
        """
        if role_name:
            self.type(*self.role_name_input, text=role_name)
        if role_key:
            self.type(*self.role_key_input, text=role_key)
        if status:
            self.select_option_by_value(*self.status_select, value=status)
        
        self.click(*self.search_btn)
        return self

    def click_add(self):
        """点击新增按钮"""
        self.click(*self.add_btn)
        return self

    def click_edit(self):
        """点击修改按钮"""
        self.click(*self.edit_btn)
        return self

    def click_remove(self):
        """点击删除按钮"""
        self.click(*self.remove_btn)
        return self

    def click_export(self):
        """点击导出按钮"""
        self.click(*self.export_btn)
        return self
