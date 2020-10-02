"""Functions that presents relevant information
about an schema entity regarding validations -
namely: whether it needs validations and the name it will appear on the report"""
from functools import singledispatch
from .schema import Entity, Table, TableEntity, ColumnEntity

@singledispatch
def needs_validation(entity, _ignore_tables: list):
    """Check if entity should or not be validated, considering the ignore-tables configuration"""
    raise TypeError("This method does not accept instances other than Entity")

@needs_validation.register
def _(_entity: Entity, _ignore_tables: list):
    return True

@needs_validation.register # type: ignore
def _(table: Table, ignore_tables: list):
    return table.name not in ignore_tables

@needs_validation.register #type: ignore
def _(table_entity: TableEntity, ignore_tables: list):
    return needs_validation(table_entity.table, ignore_tables)

@singledispatch
def canonical_name(entity):
    """The entity identifier on the report"""
    raise NotImplementedError

@canonical_name.register #type: ignore
def _(entity: Entity):
    return entity.name

@canonical_name.register #type: ignore
def _(table_entity: TableEntity):
    return f'{canonical_name(table_entity.table)}.{table_entity.name}'

@canonical_name.register #type: ignore
def _(column_entity: ColumnEntity):
    return f'{canonical_name(column_entity.column)}.{column_entity.name}'
