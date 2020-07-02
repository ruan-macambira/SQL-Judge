import pytest
from lib.schema_operations import (add_column_to_table, add_table_to_schema, add_index_to_column, add_trigger_to_table, add_constraint_to_column)

# add_table_to_schema
def test_add_table_assigns_schema_to_table(schema, table):
    add_table_to_schema(schema, table)

    assert table.schema == schema

def test_add_table_adds_the_table_to_schema(schema, table):
    add_table_to_schema(schema, table)

    assert table in schema.tables

# add_column_to_table
def test_add_column_assigns_table_to_column(table, column):
    add_column_to_table(table, column)

    assert column.table == table

def test_add_column_adds_the_column_to_table(table, column):
    add_column_to_table(table, column)

    assert column in table.columns

def test_add_column_with_primary_key(table, primary_key_column):
    add_column_to_table(table=table, column=primary_key_column)

    assert table.primary_key == primary_key_column

def test_add_column_cannot_reassign_primary_key(table, build_column):
    column = build_column(primary_key=True)
    add_column_to_table(table=table, column=build_column(primary_key=True))

    assert add_column_to_table(table=table, column=column) is False
    assert column not in table.columns

# add_index_to_column
def test_add_index_assigns_column_to_index(column, index):
    add_index_to_column(column, index)

    assert column.index == index

def test_add_index_assigns_index_to_column(column, index):
    add_index_to_column(column, index)

    assert index.column == column

# add_constraint_to_column
def test_add_constraint_assigns_constraints_to_column(column, constraint):
    add_constraint_to_column(column, constraint)

    assert constraint in column.constraints

def test_add_constraint_assigns_column_to_constraint(column, constraint):
    add_constraint_to_column(column, constraint)

    assert constraint.column == column

# add_trigger_to_table
def test_add_trigger_assigns_trigger_to_table(table, trigger):
    add_trigger_to_table(table, trigger)

    assert trigger in table.triggers

def test_add_trigger_assigns_table_to_trigger(table, trigger):
    add_trigger_to_table(table, trigger)

    assert trigger.table == table
