import pytest
import requests
import requests_mock


# 使用 pytest fixture 来初始化 requests_mock


# 测试函数使用 mock_server fixture

def test_get_data(mock_server):
    response = requests.get('https://api.example.com/data')
    

    # 断言响应的 JSON 数据是否正确
    assert response.status_code == 200
    assert response.json() == {'key': 'value'}


def test_post_data(mock_server):
    response = requests.post('https://api.example.com/data', json={'name': 'test'})

    # 断言响应的 JSON 数据是否正确
    assert response.status_code == 201
    assert response.json() == {'status': 'success'}



if __name__ == '__main__':
    pytest.main()