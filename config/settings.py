import configparser
import os

#获取项目根目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#读取配置文件
config=configparser.ConfigParser()
config.read(os.path.join(BASE_DIR,'config','config.ini'))

#配置文件
class APIConfig:
    # 接口地址
    BASE_URL=config.get('API','base_url')
    # 请求超时时间
    TIMEOUT=config.getint('API','timeout')

#数据库配置
class DBConfig:
    # 数据库配置
    HOST = config.get('DB', 'host')
    # 数据库端口
    PORT = config.getint('DB', 'port')
    # 数据库名称
    USER = config.get('DB', 'user')
    # 数据库密码
    PASSWORD = config.get('DB', 'password')
    # 数据库名称
    DATABASE = config.get('DB', 'database')

