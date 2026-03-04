from tests.page.user_form_page import UserFormPage

class EditUserPage(UserFormPage):
    """编辑用户页面"""
    
    # 覆盖 iframe pattern，注意这里 pattern 较宽泛以匹配不同 ID
    IFRAME_SRC_PATTERN = "/system/user/edit"

    def is_loaded(self, timeout=10):
        """验证编辑用户页面是否加载完成"""
        try:
            return self.find(*self.user_name_input, timeout=timeout) is not None
        except Exception:
            return False

    def set_login_name(self, name):
        """覆盖基类方法：编辑页面登录账号通常不可修改，记录警告或跳过"""
        self.logger.warning("EditUserPage: Login name is read-only and cannot be modified.")
        return self
