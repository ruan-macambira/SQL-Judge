""" Operations that alter the Schema in order to represent the adapter source """
from .schema import Schema, Table, Column, Index, Constraint, Trigger, Function, Procedure

def add_table_to_schema(schema: Schema, table: Table) -> None:
    """ Add a Table to the Schema """
    schema.tables.append(table)
    table.schema = schema

def add_column_to_table(table: Table, column: Column) -> None:
    """ Add a Column to a Table """
    table.columns.append(column)
    column.table = table

def add_trigger_to_table(table: Table, trigger: Trigger) -> None:
    """ Add a Trigger to a Table """
    table.triggers.append(trigger)
    trigger.table = table

def add_index_to_column(column: Column, index: Index) -> None:
    """ Add an Index to a Column """
    column.index = index
    index.column = column

def add_constraint_to_column(column: Column, constraint: Constraint) -> None:
    """ Add a constraint to a Column """
    column.constraints.append(constraint)
    constraint.column = column

def add_function_to_schema(schema: Schema, function: Function) -> None:
    """ Add a function to a Schema """
    schema.functions.append(function)
    function.schema = schema

def add_procedure_to_schema(schema: Schema, procedure: Procedure) -> None:
    """ Add a procedure to a Schema """
    schema.procedures.append(procedure)
    procedure.schema = schema
