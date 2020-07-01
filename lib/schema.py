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

    @property
    def entities(self) -> dict:
        """A Dict containing the schema entities"""
        return {
            'Tables': self.tables,
            'Columns': self.columns,
            'Triggers': self.triggers,
            'Indexes': self.indexes,
            'Constraints': self.constraints,
            'Functions': self.functions,
            'Procedures': self.procedures
        }

    @property
    def entity_groups(self):
        """ the groups of entitites contained in a schema """
        return self.entities.keys()

def null_schema():
    """ Schema Null Object """
    return Schema()

class SchemaEntity:
    """Generic Schema Entity of a Database"""
    def table_name(self):
        """ The Table this entity is associated, directly or not """
        raise NotImplementedError

    @property
    def canonical_name(self):
        """ The unique name the entity has that represents itself """
        raise NotImplementedError

class Table(SchemaEntity):
    """Database Table"""
    def __init__(self, name: str):
        self.schema: Optional[Schema] = None
        self.columns: List['Column'] = []
        self.triggers: List['Trigger'] = []

        self.name = name

    def table_name(self):
        return self.name

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

def null_table() -> Table:
    """Table Null Object"""
    return Table('')

class Trigger(SchemaEntity):
    """Table Trigger"""
    def __init__(self, name: str, hook: str):
        self.table: Table = null_table()

        self.name = name
        self.hook = hook.upper() # AFTER CREATE, AFTER UPDATE, AFTER DELETE

    def table_name(self):
        return self.table.name

    @property
    def canonical_name(self):
        return f'{self.table.canonical_name}.{self.name}'

class Column(SchemaEntity):
    """Table Column"""
    def __init__(
            self, name: str, col_type: str, primary_key: bool = False, references: 'Table' = None):
        if references is not None and primary_key is True:
            raise TypeError
        self.table: Table = null_table()
        self.index: Optional['Index'] = None
        self.constraints: List['Constraint'] = []

        self.name: str = name
        self.type: str = col_type
        self.primary_key = primary_key
        self.references: Optional['Table'] = references

    def table_name(self):
        return self.table.name

    @property
    def canonical_name(self):
        return f'{self.table.canonical_name}.{self.name}'

def null_column() -> Column:
    """Column Null Object"""
    return Column('', '')

class Index(SchemaEntity):
    """Column Index"""
    def __init__(self, name: str, unique: bool = False):
        self.column: Column = null_column()

        self.name: str = name
        self.unique: bool = unique


    def table_name(self):
        return self.column.table.name

    @property
    def canonical_name(self):
        return f'{self.column.canonical_name}.{self.name}'

class Constraint(SchemaEntity):
    """ Column Constraint """
    def __init__(self, name: str, cons_type: str):
        self.column: Column = null_column()

        self.name = name
        self.type = cons_type

    def table_name(self):
        return self.column.table.name

    @property
    def canonical_name(self):
        return f'{self.column.canonical_name}.{self.name}'

class Function(SchemaEntity):
    """ Schema Function """
    def __init__(self, name):
        self.name = name
        self.schema: Schema = null_schema()

    def table_name(self):
        return 'sjnkjrnreojnregojrebnreojgbreogjbrnegorueb'

    @property
    def canonical_name(self):
        return self.name

class Procedure(SchemaEntity):
    """ Schema Procedure """
    def __init__(self, name):
        self.name = name
        self.schema: Schema = null_schema()

    def table_name(self):
        return ''

    @property
    def canonical_name(self):
        return self.name
