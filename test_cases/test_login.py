import pytest
from untils.http_requests import HTTPClient
from untils.logger import logger

@pytest.fixture(scope='class')
def client():
    client = HTTPClient()
    yield client
    client.session.close()

class TestLogin:
    @pytest.mark.parametrize("username, password, expected_code", [
        ("admin", "password", 200),
        ("invalid_user", "password", 400),
        ("admin", "wrong_password", 400)
    ])
    def test_login(self, client, username, password, expected_code):
        """测试登录接口"""
        endpoint = "/login"
        payload = {
            "username": username,
            "password": password
        }

        logger.info(f"Testing login with {username}/{password}")
        response = client.post(endpoint, json=payload)
        assert response.status_code == expected_code
        if response.status_code == 200:
            assert "token" in response.json()

if __name__ == "__main__":
    pytest.main()

