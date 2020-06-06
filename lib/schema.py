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

def add_column(table: Table, column: Column) -> bool:
    """ Add an Column to the Table """
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
    schema.tables.append(table)
    table.schema = schema

    return True
