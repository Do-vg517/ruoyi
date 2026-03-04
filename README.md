# RuoYi UI Automation Test Framework

## 1. 项目介绍及来源
本项目是基于 [RuoYi](http://ruoyi.vip/) 系统开发的 UI 自动化测试框架。旨在通过自动化手段验证若依管理系统的核心功能，提高回归测试效率，确保系统稳定性。

项目来源：自主开发[ruoyi](http://ruoyi.vip)测试项目，采用业界主流的 Python + Selenium + Pytest + Allure 技术栈。
项目部署详看若依官网，拉取代码本地部署，本测试系统为了方便测试，将登录模块的验证码功能关闭。

## 2. 框架结构
本项目采用 Page Object Model (POM) 设计模式，结构清晰，易于维护。

```text
ruoyi/
├── tests/
│   ├── config/             # 配置文件 (环境配置、日志配置等)
│   ├── data/               # 测试数据 (YAML格式，实现数据驱动)
│   ├── page/               # 页面对象 (POM层，封装页面元素与操作)
│   ├── testcase/           # 测试用例 (Pytest脚本)
│   ├── util_tools/         # 工具类 (日志、数据加载器等)
│   ├── html/               # 本地调试用的HTML资源
│   └── conftest.py         # Pytest共享夹具 (Driver初始化、钩子函数等)
├── allure-results/         # Allure 原始结果数据 (已忽略)
├── allure-report/          # Allure 生成的 HTML 报告 (已忽略)
├── pytest.ini              # Pytest 核心配置文件
├── requirements.txt        # 项目依赖清单
└── README.md               # 项目说明文档
```

## 3. 工作内容
本项目已实现以下核心模块的自动化测试：

1.  **登录模块**：验证正常登录及异常登录场景。
2.  **角色管理** (`test_fix_role_auth.py`)：

    -   新增角色（支持自定义权限）。
    -   修改角色数据权限（支持数据范围设置）。
    -   删除角色。
    -   多iframe切换与复杂弹窗处理。
3.  **用户管理**：
    -   新增用户（包含部门选择、角色分配等）。
    -   编辑用户（修改用户信息）。
    -   删除用户。
    -   重置密码。
    -   重置密码 (`test_reset_passw.py`)：验证管理员重置用户密码功能。
4.  **框架特性**：
    -   **数据驱动**：使用 YAML 文件 (`tests/data/test_data.yaml`) 管理测试数据，实现代码与数据分离。
    -   **显式等待**：封装 Selenium 等待机制，提升脚本稳定性。
    -   **日志记录**：自动记录操作日志与错误堆栈 (`tests/log/`)。
    -   **自动报告**：测试结束后自动生成并打开 Allure 可视化报告。

## 4. 环境部署

### 基础环境
-   **操作系统**: Windows
-   **Python**: 3.8+
-   **Java**: JDK 1.8+ (用于运行 Allure 服务)
-   **浏览器**: Google Chrome (推荐)

### 被测系统
确保若依系统（RuoYi）已在本地或远程环境部署并启动。
-   默认地址: `http://localhost:80` (可在 `tests/config/settings.yml` 或 `conftest.py` 中修改)

## 5. 安装依赖

1.  **克隆项目**
    ```bash
    git clone <repository_url>
    cd ruoyi
    ```

2.  **创建虚拟环境 (可选但推荐)**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **安装 Python 依赖**
    ```bash
    pip install -r requirements.txt
    ```
    *核心依赖: pytest, selenium, allure-pytest, webdriver-manager, PyYAML*

4.  **安装 Allure 命令行工具**
    -   下载 Allure: [Allure Releases](https://github.com/allure-framework/allure2/releases)
    -   解压并将 `bin` 目录添加到系统环境变量 `PATH` 中。
    -   验证安装: `allure --version`

## 6. 执行步骤

### 运行所有测试
在项目根目录下执行：
```bash
pytest
```
*注：执行完成后，会自动生成 Allure 报告并自动打开浏览器展示。*

### 运行指定模块
例如，运行角色权限修复测试：
```bash
pytest tests/testcase/test_scenario/test_fix_role_auth.py
```
运行重置密码测试：
```bash
pytest tests/testcase/test_scenario/test_reset_passw.py
```

### 关于测试报告
每次执行测试后，`allure-results` 和 `allure-report` 目录会自动更新。这两个目录已被添加至 `.gitignore`，不会提交到版本控制系统中，确保仓库整洁。
