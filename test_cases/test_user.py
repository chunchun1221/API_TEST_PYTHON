import allure
import pytest
import requests
from untils.logger import logger


# 获取用户ID的 Fixture
@pytest.fixture
def user_ids(client):
    """
    通过接口获取所有用户ID，返回user_ids列表
    """
    mock_data = [
        {"id": 1, "email": "george.bluth@reqres.in", "first_name": "George", "last_name": "Bluth",
         "avatar": "https://reqres.in/img/faces/1-image.jpg"},
        {"id": 2, "email": "janet.weaver@reqres.in", "first_name": "Janet", "last_name": "Weaver",
         "avatar": "https://reqres.in/img/faces/2-image.jpg"},
        {"id": 3, "email": "emma.wong@reqres.in", "first_name": "Emma", "last_name": "Wong",
         "avatar": "https://reqres.in/img/faces/3-image.jpg"},
        {"id": 4, "email": "eve.holt@reqres.in", "first_name": "Eve", "last_name": "Holt",
         "avatar": "https://reqres.in/img/faces/4-image.jpg"},
        {"id": 5, "email": "charles.morris@reqres.in", "first_name": "Charles", "last_name": "Morris",
         "avatar": "https://reqres.in/img/faces/5-image.jpg"},
        {"id": 6, "email": "tracey.ramos@reqres.in", "first_name": "Tracey", "last_name": "Ramos",
         "avatar": "https://reqres.in/img/faces/6-image.jpg"}
    ]
    try:
        with allure.step('获取用户信息'):
            res = client.get('/users')
            if res.status_code != 200:
                logger.error(f"获取用户信息失败，状态码: {res.status_code}")
                logger.warning(f"我要用mock数据了")
                pytest.fail("获取用户信息失败")
                return [user['id'] for user in mock_data if 'id' in user]
            logger.info(f'用户信息: {res.json()}')

            # 提取用户信息
            users_data = res.json().get('data', [])
            if not isinstance(users_data, list):
                logger.error("用户信息格式错误，data 不是列表")
                pytest.fail("用户信息格式错误")

            # 提取user_id
            user_ids = [user['id'] for user in users_data if 'id' in user]
            logger.info(f'user_ids: {user_ids}')
            return user_ids
    except Exception as e:
        logger.error(f"获取用户信息时发生异常: {e}")
        logger.warning(f"我要用mock数据了")
        pytest.fail("获取用户信息时发生异常")
        return [user['id'] for user in mock_data if 'id' in user]



@allure.feature('用户信息模块')
class TestUser:
    @allure.story('用户信息接口(所有信息)')
    def test_user(self, client, user_ids):
        """
        测试用户接口，确保能正确获取用户信息
        """
        assert user_ids, "用户ID列表为空"

    @allure.story("单用户信息")
    def test_user_id(self, client, user_ids):
        """
        测试通过 user_id 获取单个用户信息
        """
        if not user_ids:
            pytest.skip("没有用户ID可以测试")

        for user_id in user_ids:
            with allure.step(f'获取用户ID为 {user_id} 的信息'):
                try:
                    res = client.get(f'/users/{user_id}')
                    if res.status_code != 200:
                        logger.error(f"获取用户ID为 {user_id} 的信息失败，状态码: {res.status_code}")
                        pytest.fail(f"获取用户ID为 {user_id} 的信息失败")

                    logger.info(f"测试用户ID: {user_id} 获取单用户信息成功")
                except Exception as e:
                    logger.error(f"获取用户ID为 {user_id} 的信息时发生异常: {e}")
                    pytest.fail(f"获取用户ID为 {user_id} 的信息时发生异常")


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_user.py'])
