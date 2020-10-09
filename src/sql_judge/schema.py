"""Database Schema"""
from typing import List, Optional
from collections import namedtuple
from .util import find, cached_property

class Schema:
    """Database Schema"""
    def __init__(self, adapter):
        self._adapter = adapter

        # Caching references used more than once to avoid making multiple calls to the adapter
        self._references = self._adapter.references()
        self._primary_keys = self._adapter.primary_keys()

    def __references(self, params):
        ref_tuple = namedtuple('Reference', ['table', 'column', 'references'])
        references = (ref_tuple(*el) for el in self._references)
        ref = find(references, lambda el: el.table == params['table_name'] and el.column == params['name'])
        return ref.references if ref is not None else None

    def __is_primary_key(self, params):
        pkey = find(
            self._primary_keys,
            lambda el: el == (params['table_name'], params['name'])
        )
        return pkey is not None

    def __entities(self, factory, group):
        return [
            factory(schema=self, **params) for params in getattr(self._adapter, group)()
        ]

    @cached_property
    def tables(self) -> List['Table']:
        """ Database Tables"""
        return self.__entities(Table, 'tables')

    @cached_property
    def columns(self) -> List['Column']:
        """ Database Columns """
        return [
            Column(
                schema=self, primary_key = self.__is_primary_key(params),
                references = self.__references(params), **params)
            for params in self._adapter.columns()
        ]

    @cached_property
    def sequences(self) -> List['Entity']:
        """ Database Sequences """
        return self.__entities(Sequence, 'sequences')

    @cached_property
    def functions(self) -> List['Entity']:
        """ Database Functions """
        return self.__entities(Function, 'functions')

    @cached_property
    def procedures(self) -> List['Entity']:
        """ Database Procedures """
        return self.__entities(Procedure, 'procedures')

    @cached_property
    def triggers(self) -> List['TableEntity']:
        """ Database Table Triggers """
        return self.__entities(Trigger, 'triggers')

    @cached_property
    def constraints(self) -> List['ColumnEntity']:
        """ Database Column Constraints """
        return self.__entities(Constraint, 'constraints')

    @cached_property
    def indexes(self) -> List['ColumnEntity']:
        """ Database Column Indexes """
        return self.__entities(Index, 'indexes')

    def entities(self):
        """ Schema Entities """
        return [
            *self.tables,
            *self.columns,
            *self.triggers,
            *self.indexes,
            *self.constraints,
            *self.sequences,
            *self.functions,
            *self.procedures
        ]


class Entity:
    """ Generic Database Schema Entity """
    def __init__(self, group: str, schema: Schema, name: str, **custom_params):
        self._schema: Schema = schema
        self.__name: str = name
        self._custom_params: dict = custom_params
        self.__name__ = group.capitalize()

    @property
    def name(self) -> str:
        """ Entity Name """
        return self.__name

    @property
    def schema(self) -> Schema:
        """ Entity Schema """
        return self._schema

    def __getattribute__(self, item):
        if item in super().__getattribute__('_custom_params'):
            return self._custom_params[item]
        return super().__getattribute__(item)

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
    """Database Table"""
    def __init__(self, name, schema, **custom_params):
        super().__init__(group='table', name=name, schema=schema, **custom_params)

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

class TableEntity(Entity):
    """ Entity That belongs to a Table """
    def __init__(self, group, name, table_name, schema, **custom_params):
        super().__init__(group=group, name=name, schema=schema, **custom_params)
        self._table = find(self._schema.tables, lambda el: el.name == table_name)

    @property
    def table(self) -> Table:
        """ Table assigned to Entity """
        return self._table

def Trigger(**params): # pylint: disable=invalid-name
    """ Trigger Entity """
    return TableEntity(group='trigger', **params)

class Column(TableEntity):
    """ Column Entity """
    def __init__(self, name, table_name, schema, primary_key=False, references=None, **custom_params):
        super().__init__(group='column', name=name, table_name=table_name, schema=schema, **custom_params)
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
        return find(
            self._schema.indexes,
            lambda index: index.table == self.table and index.column.name == self.name
        )

    @property
    def constraints(self) -> List['ColumnEntity']:
        """ Column Constraint """
        return [
            cons for cons in self._schema.constraints
            if cons.table == self.table and cons.column.name == self.name
        ]

class ColumnEntity(TableEntity):
    """ Entity that belongs to a Column """
    def __init__(self, group, name, table_name, column_name, schema, **custom_params):
        super().__init__(group=group, name=name, table_name=table_name, schema=schema, **custom_params)
        self._column = find(
            self._schema.columns,
            lambda el: el.table == self.table and el.name == column_name
        )

    @property
    def column(self) -> Column:
        """ Column Assigned to Entity """
        return self._column

def Index(*args, **kwargs): # pylint: disable=invalid-name
    """ Index Entity """
    return ColumnEntity(group='index', *args, **kwargs)

def Constraint(*args, **kwargs): # pylint: disable=invalid-name
    """ Constraint Entity """
    return ColumnEntity(group='constraint', *args, **kwargs)
