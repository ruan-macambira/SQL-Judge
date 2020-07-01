""" Use the database connection to adapt its schema to the applications objects """
from lib.schema import Schema, Table, Column, Index, Constraint, Trigger, Function, Procedure
from lib.schema_operations import (
    add_table_to_schema, add_column_to_table, add_trigger_to_table,
    add_index_to_column, add_constraint_to_column, add_function_to_schema, add_procedure_to_schema
)
from lib.adapter import DBAdapter

def generate_schema(conn: DBAdapter) -> Schema:
    """ Generate an Schema objects containing the schema contained in the provided database """
    schema = Schema()
    for table_name in conn.tables():
        table: Table = Table(table_name)
        _insert_columns_to_table(table, conn)
        _insert_triggers_to_table(table, conn)
        add_table_to_schema(schema, table)

    for column in schema.columns:
        _insert_references_to_column(column, schema, conn)
        _insert_index_to_column(column, conn)
        _insert_constraints_to_column(column, conn)

    for function_name in conn.functions():
        function: Function = Function(function_name)
        add_function_to_schema(schema, function)

    for procedure_name in conn.procedures():
        procedure: Procedure = Procedure(procedure_name)
        add_procedure_to_schema(schema, procedure)

    return schema

def _insert_columns_to_table(table: Table, conn: DBAdapter) -> None:
    for name, col_type in conn.columns(table.name).items():
        column = Column(name=name, col_type=col_type,
                        primary_key=conn.primary_key(table.name, name))
        add_column_to_table(table, column)

def _insert_triggers_to_table(table: Table, conn: DBAdapter) -> None:
    for name, hook in conn.triggers(table.name).items():
        trigger = Trigger(name=name, hook=hook)
        add_trigger_to_table(table, trigger)

def _insert_references_to_column(column: Column, schema: Schema, conn: DBAdapter) -> None:
    for table in schema.tables:
        if conn.references(column.table.name, column.name) == table.name:
            column.references = table

def _insert_index_to_column(column: Column, conn: DBAdapter) -> None:
    index_name = conn.index(column.table.name, column.name)
    if index_name is not None:
        add_index_to_column(column, Index(name=index_name))

def _insert_constraints_to_column(column: Column, conn: DBAdapter) -> None:
    for (cons_name, cons_type) in conn.constraints(column.table.name, column.name).items():
        constraint = Constraint(name=cons_name, cons_type=cons_type)
        add_constraint_to_column(column, constraint)
