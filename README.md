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

### 数据驱动示例
```python
# test_cases/auth/test_login.py
@allure.feature("认证中心")
class TestLogin:
    @pytest.mark.parametrize("case", ExcelLoader.load("login_cases.xlsx"))
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

