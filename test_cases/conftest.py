import pytest
import requests_mock
from untils.excel import ExcelUtil
from untils.http_requests import HTTPClient


#测试夹具，做mock-sever和数据驱动的准备

@pytest.fixture(scope='function')
def mock_server():
    # 创建一个 Mock Server，模拟服务端返回数据
    with requests_mock.Mocker() as mock:
        # 模拟一个 GET 请求
        mock.get('https://api.example.com/data', json={'key': 'value'}, status_code=200)



        # 模拟 POST 请求
        mock.post('https://api.example.com/data', json={'status': 'success'}, status_code=201)

        # 你可以根据需要添加更多的 mock 数据
        yield mock  # 返回给测试函数，允许访问 mock 对象


@pytest.fixture(scope='function')
def client():
    client = HTTPClient()
    yield client
    client.session.close()
