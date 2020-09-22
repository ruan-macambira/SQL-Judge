from functools import singledispatch
from .schema import Entity, Table, TableEntity, ColumnEntity

class ValidationEntity:
    def __init__(self, entity: Entity):
        self.entity: Entity = entity
        self.errors: list = []

    def needs_validation(self, ignore_tables: list):
        return needs_validation(self.entity, ignore_tables)

    def canonical_name(self):
        return canonical_name(self.entity)

    def is_valid(self):
        return len(self.errors) == 0


@singledispatch
def needs_validation(entity, _ignore_tables: list):
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
