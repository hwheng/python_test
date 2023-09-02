import pymysql
from config import setting


class DBHelper(object):

    def __init__(self):
        # TODO 此处配置，可以去配置文件中读取。
        self.pool = setting.POOL

    def get_conn_cursor(self):
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    @staticmethod
    def close_conn_cursor(*args):
        for item in args:
            item.close()

    def exec(self, sql, **kwargs):
        conn, cursor = self.get_conn_cursor()

        result = cursor.execute(sql, kwargs)
        conn.commit()

        self.close_conn_cursor(conn, cursor)
        return result

    def fetch_one(self, sql, **kwargs):
        conn, cursor = self.get_conn_cursor()

        cursor.execute(sql, kwargs)
        result = cursor.fetchone()

        self.close_conn_cursor(conn, cursor)
        return result

    def fetch_all(self, sql, **kwargs):
        conn, cursor = self.get_conn_cursor()

        cursor.execute(sql, kwargs)
        result = cursor.fetchall()

        self.close_conn_cursor(conn, cursor)

        return result


db = DBHelper()


