from selenium.webdriver.common.by import By
from tests.page.base_page import BasePage

class DeptSelectPage(BasePage):
    # 搜索区域
    keyword_input = (By.ID, "keyword")
    search_btn = (By.ID, "btn")
    
    # 树节点容器
    tree_container = (By.ID, "tree")
    
    # 展开/折叠
    expand_btn = (By.XPATH, "//a[contains(@onclick, '$.tree.expand()')]")
    collapse_btn = (By.XPATH, "//a[contains(@onclick, '$.tree.collapse()')]")

    def search(self, keyword):
        """搜索部门"""
        self.type(*self.keyword_input, text=keyword)
        self.click(*self.search_btn)
        return self

    def expand_all(self):
        """展开所有节点"""
        self.click(*self.expand_btn)
        return self

    def collapse_all(self):
        """折叠所有节点"""
        self.click(*self.collapse_btn)
        return self

    def select_dept_by_name(self, dept_name):
        """
        根据部门名称选择节点
        :param dept_name: 部门名称，如 "研发部门"
        """
        # zTree 的节点通常是 span 或 a 标签
        # 100.html 显示结构为 <a title="研发部门">...<span id="tree_3_span">研发部门</span></a>
        # 所以可以通过 title 属性或 span 文本定位
        try:
            # 优先尝试通过 title 属性定位 a 标签并点击
            xpath = f"//a[@title='{dept_name}']"
            self.click(By.XPATH, xpath)
        except Exception:
            # 备选：通过 span 文本定位
            xpath = f"//span[text()='{dept_name}']"
            self.click(By.XPATH, xpath)
        return self
