""" Database adapters """
from typing import List, Dict, Optional
class DBAdapter:
    """ Specify the methods a Database Connection must have """

    def tables(self) -> List[str]:
        """ Return the tables on the Schema """
        raise NotImplementedError

    def columns(self, table_name: str) -> Dict[str, str]:
        """ Given a Table Name, returns its columns names and types """
        raise NotImplementedError

    def triggers(self, table_name: str) -> Dict[str, str]:
        """ Given a Table, returns the triggers associated """
        raise NotImplementedError

    def primary_key(self, table_name: str, column_name: str) -> bool:
        """ Given a table name and a column, informs if it is a primary key """
        raise NotImplementedError

    def references(self, table_name: str, column_name: str) -> Optional[str]:
        """ Given a table and a column, returns which table it references """
        raise NotImplementedError

    def index(self, table_name: str, column_name: str) -> Optional[str]:
        """ Return the indexes assigned a column in a table """
        raise NotImplementedError

    def constraints(self, table_name: str, column_name: str) -> Dict[str, str]:
        """ Return the constraint assigned to a column in a table """
        raise NotImplementedError

    def functions(self) -> List[str]:
        """ Return the Schema Functions """
        raise NotImplementedError

    def procedures(self) -> List[str]:
        """ Return the Schema Procedures """
        raise NotImplementedError
