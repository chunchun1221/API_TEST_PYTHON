import pytest
from untils.http_requests import HTTPClient
from untils.logger import logger
from untils.excel import ExcelUtil
import allure
@pytest.fixture(scope='class')
def client():
    client = HTTPClient()
    yield client
    client.session.close()


@allure.feature("登录模块")
class TestLogin:

    # 读取 Excel 数据
    data = ExcelUtil().read_excel(sheet_name='Login', use_cols=['账号名', '密码', '预期码'])
    all_case = []
    for row in data:
        all_case.append(row)
    @allure.story("登录接口")


    @pytest.mark.parametrize("username, password, assert_message", all_case)
    def test_login(self, client, username, password, assert_message):
        """
        测试登录接口
        :param client: HTTP 客户端
        :param username: 账号名
        :param password: 密码
        :param assert_message: 预期结果
        """
        # 动态设置 Allure 报告的标题和描述
        allure.dynamic.title(f"测试登录接口 - 用户名: {username}, 密码: {password}")
        allure.dynamic.description(f"预期结果: {assert_message}")

        endpoint = "/login"
        payload = {
            "username": username,
            "password": password
        }

        # 记录日志
        logger.info(f"Testing login with {username}/{password}")

        # 发送请求
        with allure.step("发送登录请求"):
            response = client.post(endpoint, json=payload)
            logger.info(f"响应状态码: {response.status_code}")

        # 验证响应
        with allure.step("验证响应"):
            assert response.status_code == assert_message, f"预期状态码: {assert_message}, 实际状态码: {response.status_code}"
            if response.status_code == 200:
                assert "token" in response.json(), "响应中未找到 token"
if __name__ == "__main__":
    pytest.main()

