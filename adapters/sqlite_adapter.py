from typing import List, Dict, Optional
from sqlite3 import connect, Connection
from lib.adapter import DBAdapter
class SQLiteAdapter(DBAdapter):
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
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)

        result = [
            {cursor.description[i][0]: query_row[i] for i in range(len(cursor.description))}
            for query_row in cursor.fetchall()
        ]
        cursor.close()

        return result

    def tables(self) -> List[str]:
        sql = "SELECT tbl_name FROM SQLITE_MASTER WHERE TYPE='table' ORDER BY tbl_name"
        return [row['tbl_name'].upper() for row in self.execute(sql)]

    def triggers(self, table_name) -> Dict[str, str]:
        return {}

    def columns(self, table_name) -> Dict[str, str]:
        table_columns_sql = f"select name, type, pk from pragma_table_info('{table_name}')"
        table_columns = self.execute(table_columns_sql)

        return {
            column_data['name'].upper():column_data['type'].upper() for column_data in table_columns
        }

    def primary_key(self, table_name, column_name) -> bool:
        sql = f"select pk from pragma_table_info('{table_name}') where name = '{column_name}'"
        return len(self.execute(sql)) != 0


    def references(self, table_name, column_name) -> Optional[str]:
        if column_name not in self.columns(table_name).keys():
            return None
        table_fks_sql = f"select `table`, `from` from pragma_foreign_key_list('{table_name}')' \
            ' where `from` = '{column_name}'"
        table_foreign_keys = self.execute(table_fks_sql)

        return table_foreign_keys[0]['table'].upper() if len(table_foreign_keys) > 0 else None

    def index(self, table_name, column_name) -> Optional[str]:
        return None

    def constraints(self, table_name, column_name) -> Dict[str, str]:
        return {}

    def functions(self):
        return []

    def procedures(self):
        return []
