""" Database adapters """
from typing import List, Dict

class DBAdapter:
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
