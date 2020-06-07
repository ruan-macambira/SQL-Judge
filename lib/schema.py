from typing import List, Optional
from itertools import chain

class Column:
    """Table Column"""
    def __init__(self, name: str, col_type: str):
        self.table: Optional[Table] = None
        self.name: str = name
        self.type: str = col_type

class Table:
    """Database Table"""
    def __init__(self, name: str):
        self.schema: Optional[Schema] = None
        self.columns: List[Column] = []
        self.primary_key: Optional[Column] = None

        self.name: str = name

def add_column(table: Table, column: Column, primary_key: bool = False) -> bool:
    """ Add an Column to the Table """
    if table is None or column is None:
        raise TypeError
    if primary_key is True and table.primary_key is not None:
        return False

    table.columns.append(column)
    column.table = table

    if primary_key:
        table.primary_key = column

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
