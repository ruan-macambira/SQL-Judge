import functools
from .schema import Schema, Table, Column, Index, Constraint, Trigger

def _raise_type_error_if_any_is_none(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if None in args or None in kwargs:
            raise TypeError
        return function(*args, **kwargs)
    return wrapper

@_raise_type_error_if_any_is_none
def add_table_to_schema(schema: Schema, table: Table) -> bool:
    """ Add a Table to the Schema """
    schema.tables.append(table)
    table.schema = schema

    return True

@_raise_type_error_if_any_is_none
def add_column_to_table(table: Table, column: Column) -> bool:
    """ Add a Column to a Table """
    if column.primary_key is True and table.primary_key is not None:
        return False

    table.columns.append(column)
    column.table = table

    return True

@_raise_type_error_if_any_is_none
def add_trigger_to_table(table: Table, trigger: Trigger) -> bool:
    """ Add a Trigger to a Table """
    table.triggers.append(trigger)
    trigger.table = table

    return True

@_raise_type_error_if_any_is_none
def add_index_to_column(column: Column, index: Index) -> bool:
    """ Add an Index to a Column """
    column.index = index
    index.column = column

    return True

@_raise_type_error_if_any_is_none
def add_constraint_to_column(column: Column, constraint: Constraint) -> bool:
    """ Add a constraint to a Column """
    column.constraints.append(constraint)
    constraint.column = column

    return True
