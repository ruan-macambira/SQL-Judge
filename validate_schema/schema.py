""" Database Schema-Related objects and fucntions """
from typing import List, Optional
from itertools import chain

class Schema:
    """Database Schema"""
    def __init__(self):
        self.tables: List['Table'] = []
        self.functions: List['Function'] = []
        self.procedures: List['Procedure'] = []
        self.sequences: List['SchemaEntity'] = []

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

    def entities(self):
        return {
            'Tables': self.tables,
            'Functions': self.functions,
            'Procedures': self.procedures,
            'Columns': self.columns,
            'Triggers': self.triggers,
            'Indexes': self.indexes,
            'Constraints': self.constraints,
        }

def null_schema():
    """ Schema Null Object """
    return Schema()

class Entity: #pylint: disable=too-few-public-methods
    """Generic Schema Entity of a Database"""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        """Entity Name"""
        return self._name

    def canonical_name(self):
        raise NotImplementedError

    def needs_validation(self, ignore_tables=None):
        raise NotImplementedError

class SchemaEntity(Entity): #pylint: disable=too-few-public-methods
    """Entity that is owned directly by the schema"""
    def __init__(self, name):
        super().__init__(name=name)
        self.schema: Schema = null_schema()

    def canonical_name(self):
        return self.name

    def needs_validation(self, _ignore_tables=None):
        return True

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

    def needs_validation(self, ignore_tables=None):
        return not self.name in (ignore_tables or [])

def null_table() -> Table:
    """Table Null Object"""
    return Table('')

class TableEntity(Entity): #pylint: disable=too-few-public-methods
    """Entity directly related to a Table"""
    def __init__(self, name):
        super().__init__(name=name)
        self.table: Table = null_table()

    def canonical_name(self):
        return '{}.{}'.format(self.table.canonical_name(), self.name)

    def needs_validation(self, ignore_tables=None):
        return self.table.needs_validation(ignore_tables)

class Trigger(TableEntity):
    """Table Trigger"""
    def __init__(self, name: str, hook: str):
        super().__init__(name=name)
        self._hook = hook

    @property
    def hook(self):
        """The moment the trigger is invoked (BEFORE INSERT, AFTER INSERT, BEFORE UPDATE, etc.)"""
        return self._hook

class Column(TableEntity):
    """Table Column"""
    def __init__(
            self, name: str, col_type: str, primary_key: bool = False, references: 'Table' = None):
        if references is not None and primary_key is True:
            raise TypeError
        super().__init__(name=name)
        self.index: Optional['Index'] = None
        self.constraints: List['Constraint'] = []
        self.references: Optional['Table'] = references

        self._type: str = col_type
        self._primary_key = primary_key

    @property
    def type(self):
        """Column Data Type (varchar, numeric, date, etc.)"""
        return self._type

    @property
    def primary_key(self) -> bool:
        """The Column is the primary key of the table"""
        return self._primary_key

def null_column() -> Column:
    """Column Null Object"""
    return Column('', '')

class ColumnEntity(Entity): #pylint: disable=too-few-public-methods
    """ Entity directly related to a column """
    def __init__(self, name):
        super().__init__(name=name)
        self.column: Column = null_column()

    def canonical_name(self):
        return '{}.{}'.format(self.column.canonical_name(), self.name)

    def needs_validation(self, ignore_tables=None):
        return self.column.needs_validation(ignore_tables)

class Index(ColumnEntity):
    """Column Index"""
    def __init__(self, name: str, unique: bool = False):
        super().__init__(name=name)
        self._unique: bool = unique

    @property
    def unique(self):
        """The index constraints the column to be a unique one"""
        return self._unique

class Constraint(ColumnEntity):
    """ Column Constraint """
    def __init__(self, name: str, cons_type: str):
        super().__init__(name=name)
        self._type = cons_type

    @property
    def type(self):
        """Constraint Type (unique, primary key, foreign key, etc.)"""
        return self._type
