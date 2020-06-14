import cx_Oracle
from lib.adapter import DBAdapter

class OracleAdapter(DBAdapter):
    """ Database Connection to a Oracle Database """
    def __init__(self, host: str, database: str, username: str, password: str):
        self.host: str = host
        self.database: str = database
        self.username: str = username
        self.password: str = password

    def connection(self):
        return cx_Oracle.connect(
            self.username, self.password,
            f'{self.host}/{self.database}'
        )

    def execute(self, sql):
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

    def tables(self):
        return []

    def columns(self, table_name: str):
        return []
