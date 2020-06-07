from typing import List, Optional
from itertools import chain

class Column:
    """Table Column"""
    def __init__(self, name: str, col_type: str, primary_key: bool = False, references: 'Table' = None):
        self.table: Optional[Table] = None
        self.name: str = name
        self.type: str = col_type

        if references is not None and primary_key is True:
            raise TypeError

        self.primary_key = primary_key
        self.references: Optional['Table'] = references

class Table:
    """Database Table"""
    def __init__(self, name: str):
        self.schema: Optional[Schema] = None
        self.columns: List[Column] = []

        self.name: str = name

    @property
    def primary_key(self) -> Optional[Column]:
        """ Returns the table Primary Key, if it has any """
        candidates: List[Column] = [column for column in self.columns if column.primary_key is True]

        if len(candidates) == 0:
            return None
        return candidates[0]

def add_column(table: Table, column: Column) -> bool:
    """ Add an Column to the Table """
    if table is None or column is None:
        raise TypeError
    if column.primary_key is True and table.primary_key is not None:
        return False

    table.columns.append(column)
    column.table = table

    return True

class Schema:
    """Database Schema"""
    def __init__(self):
        self.tables: List[Table] = []

    def columns(self) -> List[Column]:
        """Database Tables Columns"""
        tables_columns = [table.columns for table in self.tables]
        return list(chain(*tables_columns))

def add_table(schema: Schema, table: Table) -> bool:
    """ Add an Table to the Schema """
    if schema is None or table is None:
        raise TypeError

    schema.tables.append(table)
    table.schema = schema

    return True
