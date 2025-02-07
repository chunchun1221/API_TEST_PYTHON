
# 接口自动化测试框架

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/pytest-%E2%89%A56.0-green)](https://docs.pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure-Report-orange)](https://docs.qameta.io/allure/)

一个基于 **Python + Pytest + Allure** 的接口自动化测试框架，支持数据驱动、CI/CD 集成等功能。

---

## ✨ 核心特性
- **四层架构**：配置/工具/用例/数据完全解耦
- **多数据源驱动**：Excel/CSV/YAML/MySQL 测试数据支持
- **智能鉴权**：Token 自动获取刷新机制
- **多维度报告**：Allure 交互式报告 + 历史趋势分析
- **持续交付**：GitHub Actions/Jenkins 即插即用

---

## 🚀 快速启动
### 环境要求
- Python 3.8+
- Java 8+ (Allure 依赖)

### 安装部署
```bash
# 克隆仓库
git clone https://github.com/yourname/api-autotest-framework.git

# 安装依赖
pip install -r requirements.txt

# 扩展组件（按需安装）
pip install locust openpyxl requests_mock
```

### 目录结构
```bash
project/
├── config/            # 配置文件
├── data/              # 测试数据（Excel/CSV/YAML）
├── utils/             # 工具类（HTTP 客户端、数据库等）
├── test_cases/        # 测试用例
├── locustfile.py      # 性能测试脚本
├── reports/           # 测试报告（自动生成）
└── run.py             # 测试入口
```

---

## 🛠️ 使用指南

### 配置管理
1. 编辑 `config/config.ini`：
```ini
[API]
base_url = https://api.yourdomain.com
timeout = 15

[DB]
host = mysql.yourdomain.com
port = 3306
```

2. 动态加载配置：
```python
from config.settings import APIConfig, DBConfig
print(APIConfig.BASE_URL)  # 输出: https://api.yourdomain.com
```
## fixture使用示例
本框架通过pytest 的fixture机制，支持mock服务，http客户端复用，token自动化管理和接口关联

---
### 📚目录
- [HTTP 客户端](#http-客户端)
- [Mock 服务](#mock-服务)
- [Token 自动管理](#token-自动管理)
- [接口关联测试](#接口关联测试)

---

### HTTP 客户端💻
**用途**：复用 Session，提升请求效率，自动处理公共头信息。

##### **代码示例**
```python
# conftest.py
import pytest
from utils.http_client import HTTPClient

@pytest.fixture(scope="session")
def http_client():
    """全局 HTTP 客户端"""
    client = HTTPClient(base_url=APIConfig.BASE_URL)
    yield client
    client.close()  # 测试结束后关闭连接
``` 
**使用示例**：
```python
def test_get_user(http_client):
    response = http_client.get("/users/1")
    assert response.status_code == 200
 ```
## Mock 服务 😊
**用途**：模拟 API 请求，用于测试接口关联、性能测试等场景。
### 代码示例
```python
# conftest.py
import pytest
import requests_mock

@pytest.fixture
def mock_server():
    """Mock 服务 Fixture"""
    with requests_mock.Mocker() as m:
        yield m

# 预定义 Mock 规则
@pytest.fixture
def mock_login(mock_server):
    mock_server.post("/login", json={"token": "mock_token"})
    return mock_server
```
**使用示例**：
```python
def test_with_mock(mock_login, http_client):
    # 调用被 Mock 的登录接口
    response = http_client.post("/login", json={"user": "test"})
    assert response.json()["token"] == "mock_token"
```
## Token 自动管理 🚆
**用途**：自动获取和刷新
### 代码示例
```python
# conftest.py
@pytest.fixture(scope="session")
def auth_token(http_client):
    """全局 Token 获取"""
    response = http_client.post("/login", json={"user": "admin", "pwd": "123456"})
    return response.json()["token"]

@pytest.fixture(scope="function")
def auth_client(http_client, auth_token):
    """携带 Token 的客户端"""
    http_client.set_token(auth_token)
    return http_client
```

## 接口关联测试 🐻
**用途**：测试接口关联，例如登录后获取用户信息等。
### 代码示例
```python
# conftest.py
@pytest.fixture
def created_order_id(auth_client):
    """创建订单并返回订单ID"""
    response = auth_client.post("/orders", json={"product_id": 100})
    return response.json()["order_id"]
```
**使用示例**：
```python
def test_order_flow(created_order_id, auth_client):
    # 查询订单
    response = auth_client.get(f"/orders/{created_order_id}")
    assert response.json()["status"] == "pending"

    # 支付订单
    pay_response = auth_client.post(f"/orders/{created_order_id}/pay")
    assert pay_response.status_code == 200

    # 验证订单状态
    final_response = auth_client.get(f"/orders/{created_order_id}")
    assert final_response.json()["status"] == "paid"
```
---
   
# 数据驱动示例
```python
# test_cases/auth/test_login.py
@allure.feature("认证中心")
class TestLogin:
    @pytest.mark.parametrize("case", ExcelUtil("login_cases.xlsx").read_data())
    def test_login(self, client, case):
        allure.dynamic.title(case["title"])
        with allure.step("发送认证请求"):
            response = client.post("/login", json=case["data"])
        self._validate_response(response, case)
```

### 生成 Allure 报告
```bash
# 运行测试并生成报告
python run.py --env=prod --report=allure

# 本地查看报告
allure serve reports/allure_results
```

![Allure 报告预览](docs/images/allure-dashboard.png)


---

## 🤝 参与贡献
1. Fork 项目仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交代码 (`git commit -m 'Add some amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 发起 Pull Request

