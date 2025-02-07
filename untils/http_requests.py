import requests
from untils.logger import logger
from config.settings import APIConfig


class HTTPClient:
    def __init__(self):
        self.base_url = APIConfig.BASE_URL
        self.timeout = APIConfig.TIMEOUT
        self.session = requests.Session()
        self.headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }

    def set_headers(self, headers):
        self.headers.update(headers)

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault('timeout', self.timeout)
        logger.info(f"Request: {method} {url}")
        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(f"Response: {response.status_code}")
            if response.status_code >= 400:
                logger.error(f"Request failed with status code {response.text}")
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    def get(self, endpoint, params=None):
        return self.request('GET', endpoint, params=params)

    def post(self, endpoint, data=None, json=None):
        return self.request('POST', endpoint, data=data, json=json)

if __name__ == "__main__":
    client = HTTPClient()
    # 确保只传递必要的参数，避免其他干扰
    login_repose=client.post('/login',data={"username": "string","email": "george.bluth@reqres.in","password":"string"})
    print(login_repose.text)
    user_repose=client.get('/users')
    print(user_repose.text)
    users_info=user_repose.json().get('data',[])
    user_ids=[user_info['id'] for user_info in users_info]



