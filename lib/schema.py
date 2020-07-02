""" Database Schema-Related objects and fucntions """
from typing import List, Optional
from itertools import chain

class Schema:
    """Database Schema"""
    def __init__(self):
        self.tables: List['Table'] = []
        self.functions: List['Function'] = []
        self.procedures: List['Procedure'] = []

    @property
    def triggers(self) -> List['Trigger']:
        """ Database Table Triggers """
        table_triggers = [table.triggers for table in self.tables]
        return list(chain(*table_triggers))

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
    def constraints(self) -> List['Constraint']:
        """ Database Column Constraints """
        column_constraints = [column.constraints for column in self.columns]
        return list(chain(*column_constraints))

def null_schema():
    """ Schema Null Object """
    return Schema()

class Entity:
    """Generic Schema Entity of a Database"""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        """Entity Name"""
        return self._name

class SchemaEntity(Entity):
    """Entity that is owned directly by the schema"""
    def __init__(self, name):
        super().__init__(name=name)
        self.table: Schema = null_schema()

class Table(SchemaEntity):
    """Database Table"""
    def __init__(self, name: str):
        super().__init__(name=name)
        self.columns: List['Column'] = []
        self.triggers: List['Trigger'] = []

    @property
    def primary_key(self) -> Optional['Column']:
        """ Returns the table Primary Key, if it has any """
        candidates: List['Column'] = [column for column in self.columns if column.primary_key]

        if len(candidates) == 0:
            return None
        return candidates[0]

def null_table() -> Table:
    """Table Null Object"""
    return Table('')

class TableEntity(Entity):
    """Entity directly related to a Table"""
    def __init__(self, name):
        super().__init__(name=name)
        self.table: Table = null_table()

class Trigger(TableEntity):
    """Table Trigger"""
    def __init__(self, name: str, hook: str):
        super().__init__(name=name)
        self.hook = hook.upper() # AFTER CREATE, AFTER UPDATE, AFTER DELETE

class Column(TableEntity):
    """Table Column"""
    def __init__(
            self, name: str, col_type: str, primary_key: bool = False, references: 'Table' = None):
        if references is not None and primary_key is True:
            raise TypeError
        super().__init__(name=name)
        self.index: Optional['Index'] = None
        self.constraints: List['Constraint'] = []

        self.type: str = col_type
        self.primary_key = primary_key
        self.references: Optional['Table'] = references

def null_column() -> Column:
    """Column Null Object"""
    return Column('', '')

class ColumnEntity(Entity):
    """ Entity directly related to a column """
    def __init__(self, name):
        super().__init__(name=name)
        self.column: Column = null_column()

class Index(ColumnEntity):
    """Column Index"""
    def __init__(self, name: str, unique: bool = False):
        super().__init__(name=name)
        self.unique: bool = unique

class Constraint(ColumnEntity):
    """ Column Constraint """
    def __init__(self, name: str, cons_type: str):
        super().__init__(name=name)
        self.type = cons_type

class Function(SchemaEntity):
    """ Schema Function """
    pass

class Procedure(SchemaEntity):
    """ Schema Procedure """
    pass
