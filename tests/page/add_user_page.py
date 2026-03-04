from tests.page.user_form_page import UserFormPage

class AddUserPage(UserFormPage):
    """新增用户页面"""
    
    # 覆盖 iframe pattern
    IFRAME_SRC_PATTERN = "/system/user/add"

    def is_loaded(self, timeout=10):
        """验证新增用户页面是否加载完成"""
        try:
            return self.find(*self.user_name_input, timeout=timeout) is not None
        except Exception:
            return False

