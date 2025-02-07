import pytest
from untils.logger import logger
import allure
from untils.excel import ExcelUtil


def load_login_data():
    excel_util = ExcelUtil()
    sheet_name = 'Login'
    use_cols = ['账号名', '密码', '预期码']
    data_generator = excel_util.read_excel(sheet_name=sheet_name, use_cols=use_cols)
    all_case = []
    for row in data_generator:
        all_case.append(row)
    return all_case



@allure.feature("登录模块")
class TestLogin:
    @allure.story("登录接口")
    @pytest.mark.parametrize("username, password, assert_message", load_login_data())
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

