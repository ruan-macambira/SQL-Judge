import cx_Oracle
import sqlite3

class DBConnection:
    def execute(self, sql):
        raise NotImplementedError

class OracleConnection(DBConnection):
    def __init__(self, host: str, database: str, username: str, password: str):
        self.host: str = host
        self.database: str = database
        self.username: str = username
        self.password: str = password

    def execute(self, sql):
        aux = f'{self.host}/{self.database}'
        with cx_Oracle.connect(self.username, self.password, aux) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

class SQLiteConnection(DBConnection):
    def __init__(self, filename: str):
        self.filename: str = filename

    def execute(self, sql):
        """ Execute a 'SELECT' statement """
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            cursor.execute(sql)

            ret = []
            for aux in cursor.fetchall():
                auy = {}
                for i in range(len(cursor.description)):
                    auy[cursor.description[i][0]] = aux[i]
                ret.append(auy)
            cursor.close()

            return ret
