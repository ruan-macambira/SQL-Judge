import functools
from .schema import Schema, Table, Column, Index, Constraint, Trigger, Function, Procedure

def add_table_to_schema(schema: Schema, table: Table) -> bool:
    """ Add a Table to the Schema """
    schema.tables.append(table)
    table.schema = schema

    return True

def add_column_to_table(table: Table, column: Column) -> bool:
    """ Add a Column to a Table """
    if column.primary_key is True and table.primary_key is not None:
        return False

    table.columns.append(column)
    column.table = table

    return True

def add_trigger_to_table(table: Table, trigger: Trigger) -> bool:
    """ Add a Trigger to a Table """
    table.triggers.append(trigger)
    trigger.table = table

    return True

def add_index_to_column(column: Column, index: Index) -> bool:
    """ Add an Index to a Column """
    column.index = index
    index.column = column

    return True

def add_constraint_to_column(column: Column, constraint: Constraint) -> bool:
    """ Add a constraint to a Column """
    column.constraints.append(constraint)
    constraint.column = column

    return True

def add_function_to_schema(schema: Schema, function: Function) -> bool:
    """ Add a function to a Schema """
    schema.functions.append(function)
    function.schema = schema

    return True

def add_procedure_to_schema(schema: Schema, procedure: Procedure) -> bool:
    """ Add a procedure to a Schema """
    schema.procedures.append(procedure)
    procedure.schema = schema

    return True
