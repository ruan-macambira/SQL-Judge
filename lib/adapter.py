""" Database adapters """
from typing import List, Dict

class DBAdapter:
    """ Specify the methods a Database Connection must have """

    def tables(self) -> List[str]:
        """ Return the tables on the Schema """
        raise NotImplementedError

    def columns(self, table_name: str) -> List[Dict[str, str]]:
        """ Given a Table Name, returns its columns names and types """
        raise NotImplementedError

    def primary_key(self, table_name: str) -> List[str]:
        """ Given a table name, returns the column(s) that are primary keys """
        raise NotImplementedError

    def references(self, table_name: str) -> Dict[str, str]:
        """ Given a Table Name, returns which columns references which table """
        raise NotImplementedError

    def indexes(self, table_name: str):
        """ Return the indexes assigned to columns in a table """
        raise NotImplementedError
