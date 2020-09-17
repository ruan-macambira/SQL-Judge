from .util import find, cached_property
from typing import List, Optional

class Schema:
    """Database Schema"""
    def __init__(self, query_schema):
        self.__query_schema = query_schema

    def __references(self, params):
        ref = find(self.__query_schema.select('reference'), lambda el: el['table_name'] == params['table_name'] and el['column_name'] == params['name'])
        return None if not ref else ref['references']

    def __is_primary_key(self, params):
        pkey = find(self.__query_schema.select('primary_key'), lambda el: el['table_name'] == params['table_name'] and el['name'] == params['name'])
        return pkey is not None

    def __entities(self, factory):
        group = factory.__name__.lower()
        return [
            factory(schema=self, **params)
            for params in self.__query_schema.select(group)
        ]

    @cached_property
    def tables(self) -> List['Table']:
        """ Database Tables"""
        return self.__entities(Table)

    @cached_property
    def columns(self) -> List['Column']:
        """ Database Columns """
        return [
            Column(
                schema=self, primary_key = self.__is_primary_key(params),
                references = self.__references(params), **params)
            for params in self.__query_schema.select('column')
        ]


    @cached_property
    def sequences(self) -> List['Entity']:
        """ Database Sequences """
        return self.__entities(Sequence)

    @cached_property
    def functions(self) -> List['Entity']:
        """ Database Functions """
        return self.__entities(Function)

    @cached_property
    def procedures(self) -> List['Entity']:
        """ Database Procedures """
        return self.__entities(Procedure)

    @cached_property
    def triggers(self) -> List['TableEntity']:
        """ Database Table Triggers """
        return self.__entities(Trigger)

    @cached_property
    def constraints(self) -> List['ColumnEntity']:
        """ Database Column Constraints """
        return self.__entities(Constraint)

    @cached_property
    def indexes(self) -> List['ColumnEntity']:
        """ Database Column Indexes """
        return self.__entities(Index)

    def entities(self):
        return {
            'Tables': self.tables,
            'Columns': self.columns,
            'Triggers': self.triggers,
            'Indexes': self.indexes,
            'Constraints': self.constraints,
            'Sequences': self.sequences,
            'Functions': self.functions,
            'Procedures': self.procedures
        }

class Entity:
    """ Generic Database Schema Entity """
    def __init__(self, group: str, schema: Schema, name: str, **additional_params):
        self._schema: Schema = schema
        self.__name: str = name
        self.__group: str = group
        self._additional_params: dict = additional_params

    @property
    def name(self) -> str:
        """ Entity Name """
        return self.__name

    @property
    def schema(self) -> Schema:
        """ Entity Schema """
        return self._schema

    def __getattribute__(self, item):
        if item in super().__getattribute__('_additional_params'):
            return self._additional_params[item]
        return super().__getattribute__(item)

    def needs_validation(self, _ignore_tables=None):
        return True

    def canonical_name(self):
        return self.name

    @property
    def __name__(self):
        return self.__group.capitalize()

    def __str__(self):
        return f'<{self.__name__} "{self.name}">'

    def __repr__(self):
        return self.__str__()

def Function(*args, **kwargs): # pylint: disable=invalid-name
    """Function Entity"""
    return Entity(group='function', *args, **kwargs)

def Procedure(*args, **kwargs): # pylint: disable=invalid-name
    """Procedure Entity"""
    return Entity(group='procedure', *args, **kwargs)

def Sequence(*args, **kwargs): # pylint: disable=invalid-name
    """Sequence Entity"""
    return Entity(group='sequence', *args, **kwargs)

class Table(Entity):
    def __init__(self, name, schema, **additional_params):
        super().__init__(group='table', name=name, schema=schema, **additional_params)

    @cached_property
    def columns(self) -> List['Column']:
        """ Table Columns """
        return [
            column for column in self._schema.columns if column.table.name == self.name
        ]

    @cached_property
    def primary_key(self) -> Optional['Column']:
        """ Table Primary Key Column """
        return find(self.columns, lambda col: col.primary_key)

    @cached_property
    def triggers(self) -> List['TableEntity']:
        """ Table Triggers """
        return [
            trigger for trigger in self._schema.triggers if trigger.table.name == self.name
        ]

    def needs_validation(self, ignore_tables=None):
        return not self.name in (ignore_tables or [])

class TableEntity(Entity):
    """ Entity That belongs to a Table """
    def __init__(self, group, name, table_name, schema, **additional_params):
        super().__init__(group=group, name=name, schema=schema, **additional_params)
        self._table = find(self._schema.tables, lambda el: el.name == table_name)

    @property
    def table(self) -> Table:
        """ Table assigned to Entity """
        return self._table

    def needs_validation(self, ignore_tables=None):
        return self.table.needs_validation(ignore_tables)

    def canonical_name(self):
        return f'{self.table.canonical_name()}.{self.name}'

def Trigger(**params): # pylint: disable=invalid-name
    """ Trigger Entity """
    return TableEntity(group='trigger', **params)

class Column(TableEntity):
    """ Column Entity """
    def __init__(self, name, table_name, schema, primary_key=False, references=None, **additional_params):
        super().__init__(group='column', name=name, table_name=table_name, schema=schema, **additional_params)
        self.__primary_key: bool = primary_key
        self._references: str = references

    @property
    def primary_key(self) -> bool:
        """ Is Primary Key? """
        return self.__primary_key

    @property
    def references(self) -> Optional[Table]:
        """ The table it references, if any """
        if not self._references:
            return None
        return find(self._schema.tables, lambda el: el.name == self._references)

    @property
    def index(self) -> Optional['ColumnEntity']:
        """ Column Indexes """
        x = [
            index for index in self._schema.indexes
            if index.table == self.table and index.column.name == self.name
        ]
        return None if len(x) == 0 else x[0]

    @property
    def constraints(self) -> List['ColumnEntity']:
        """ Column Constraint """
        return [
            cons for cons in self._schema.constraints
            if cons.table == self.table and cons.column.name == self.name
        ]

class ColumnEntity(TableEntity):
    """ Entity that belongs to a Column """
    def __init__(self, group, name, table_name, column_name, schema, **additional_params):
        super().__init__(group=group, name=name, table_name=table_name, schema=schema, **additional_params)
        self._column_name = column_name
        self._column = find(self._schema.columns, lambda el: el.table == self.table and el.name == self._column_name)

    @property
    def column(self) -> Column:
        """ Column Assigned to Entity """
        return self._column

    def canonical_name(self):
        return f'{self.column.canonical_name()}.{self.name}'

def Index(*args, **kwargs): # pylint: disable=invalid-name
    """ Index Entity """
    return ColumnEntity(group='index', *args, **kwargs)

def Constraint(*args, **kwargs): # pylint: disable=invalid-name
    """ Constraint Entity """
    return ColumnEntity(group='constraint', *args, **kwargs)
