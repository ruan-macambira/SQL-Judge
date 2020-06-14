""" Database adapters """
from sqlite3 import connect, Connection
from typing import List, Dict
import cx_Oracle
import psycopg2

class DBConnection:
    """ Specify the methods a Database Connection must have """

    def connection(self):
        """ The Database connection object """
        raise NotImplementedError

    def execute(self, sql: str) -> List[Dict[str, str]]:
        """ Execute an SQL 'SELECT' Query """
        raise NotImplementedError

    def tables(self) -> List[str]:
        """ Return the tables on the Schema """
        raise NotImplementedError

    def columns(self, table_name: str) -> List[Dict[str, str]]:
        """ Return the column names and types in the table """
        raise NotImplementedError

class OracleConnection(DBConnection):
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

class PostgresConnection(DBConnection):
    """ Database Adapter to a Postgress database """
    def __init__(self, host: str, database: str, username: str, password: str, port:str):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port

    def connection(self):
        return psycopg2.connect(
            host=self.host, dbname=self.database, port=self.port,
            user=self.username, password=self.password
        )

    def execute(self, sql):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        ret = []
        for query_row in cursor.fetchall():
            auy = {}
            for i in range(len(cursor.description)):
                auy[cursor.description[i][0]] = query_row[i]
            ret.append(auy)
        cursor.close()
        conn.close()

        return ret

    def tables(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\'"

        return [row['table_name'].upper() for row in self.execute(sql)]

class SQLiteConnection(DBConnection):
    """ Database Connection to a SQLite Database """
    def __init__(self, filename: str = None, connection: Connection = None):
        if connection is not None:
            self._connection = connection
            return
        if filename is not None:
            self._connection = connect(filename)

    def connection(self):
        return self._connection

    def execute(self, sql: str) -> List[Dict[str, str]]:
        """ Execute a 'SELECT' statement """
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)

        ret = []
        for query_row in cursor.fetchall():
            auy = {}
            for i in range(len(cursor.description)):
                auy[cursor.description[i][0]] = query_row[i]
            ret.append(auy)
        cursor.close()

        return ret

    def tables(self) -> List[str]:
        """ Return the tables of the schema """
        sql = "SELECT tbl_name FROM SQLITE_MASTER WHERE TYPE='table' ORDER BY tbl_name"

        return [row['tbl_name'].upper() for row in self.execute(sql)]

    def columns(self, table_name):
        """ Return the columns and the types of a table """
        table_columns_sql = f"select name, type, pk from pragma_table_info('{table_name}')"
        table_fks_sql = f"select `table`, `from` from pragma_foreign_key_list('{table_name}')"

        intbool = ['false', 'true']

        table_columns = self.execute(table_columns_sql)
        table_foreign_keys = self.execute(table_fks_sql)

        columns_info = []
        for column_data in table_columns:
            column_info = {
                'name': column_data['name'].upper(), 'type': column_data['type'],
                'primary_key': intbool[column_data['pk']]
            }

            # cross-references the table columns to the table references to identify foreign keys
            for foreign_key in table_foreign_keys:
                if column_data['name'] == foreign_key['from']:
                    column_info['references'] = foreign_key['table'].upper()
                    break
            columns_info.append(column_info)
        return columns_info
