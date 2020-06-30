""" Database Schema-Related objects and fucntions """
from typing import List, Optional
from itertools import chain

class Schema:
    """Database Schema"""
    def __init__(self):
        self.tables: List['Table'] = []

    @property
    def columns(self) -> List['Column']:
        """Database Tables Columns"""
        tables_columns = [table.columns for table in self.tables]
        return list(chain(*tables_columns))

    @property
    def indexes(self) -> List['Index']:
        """ Database Columns Indexes """
        return [column.index for column in self.columns if column.index is not None]

    @property
    def entities(self) -> dict:
        """A Dict containing the schema entities"""
        return {
            'Tables': self.tables,
            'Columns': self.columns,
            'Indexes': self.indexes,
        }

    @property
    def entity_groups(self):
        """ the groups of entitites contained in a schema """
        return self.entities.keys()

class SchemaEntity:
    """Generic Schema Entity of a Database"""
    @property
    def canonical_name(self):
        """ The unique name the entity has that represents itself """
        raise NotImplementedError

class Table(SchemaEntity):
    """Database Table"""
    def __init__(self, name: str):
        self.schema: Optional[Schema] = None
        self.columns: List['Column'] = []

        self.name: str = name

    @property
    def primary_key(self) -> Optional['Column']:
        """ Returns the table Primary Key, if it has any """
        candidates: List['Column'] = [column for column in self.columns if column.primary_key]

        if len(candidates) == 0:
            return None
        return candidates[0]

    @property
    def canonical_name(self):
        return self.name

class Column(SchemaEntity):
    """Table Column"""
    def __init__(
            self, name: str, col_type: str, primary_key: bool = False, references: 'Table' = None):
        if references is not None and primary_key is True:
            raise TypeError
        self.table: Optional[Table] = None
        self.index: Optional['Index'] = None
        self.name: str = name
        self.type: str = col_type
        self.primary_key = primary_key
        self.references: Optional['Table'] = references

    @property
    def canonical_name(self):
        return f'{self.table.canonical_name}.{self.name}'


class Index(SchemaEntity):
    """Column Index"""
    def __init__(self, name: str, unique: bool = False):
        self.column: Optional[Column] = None
        self.name: str = name
        self.unique: bool = unique

    @property
    def table(self):
        """ Index Column's associated table """
        if self.column is None:
            return None
        return self.column.table

    @property
    def canonical_name(self):
        return f'{self.column.canonical_name}.{self.name}'

def add_table_to_schema(schema: Schema, table: Table) -> bool:
    """ Add a Table to the Schema """
    if schema is None or table is None:
        raise TypeError

    schema.tables.append(table)
    table.schema = schema

    return True

def add_column_to_table(table: Table, column: Column) -> bool:
    """ Add a Column to a Table """
    if table is None or column is None:
        raise TypeError
    if column.primary_key is True and table.primary_key is not None:
        return False

    table.columns.append(column)
    column.table = table

    return True

def add_index_to_column(column: Column, index: Index) -> bool:
    """ Add an Index to a Column """
    if column is None or index is None:
        raise TypeError

    column.index = index
    index.column = column

    return True
