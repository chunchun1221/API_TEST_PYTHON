import pymysql
from config.settings import DBConfig


class MySQLClient:
    def __init__(self):
        self.connection = pymysql.connect(
            host=DBConfig.HOST,
            port=DBConfig.PORT,
            user=DBConfig.USER,
            password=DBConfig.PASSWORD,
            database=DBConfig.DATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        self.connection.close()

# 使用示例
# with MySQLClient() as db:
#     result = db.execute_query("SELECT * FROM users")