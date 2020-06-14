from typing import List, Dict
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
