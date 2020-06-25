#pylint: disable=missing-module-docstring
#pylint: disable=missing-function-docstring
import pytest
from lib.schema import add_column_to_table, add_table_to_schema

# Schema
def test_columns_returns_every_column_from_every_table(schema, build_table):
    table1 = build_table(columns=1)
    table2 = build_table(columns=1)

    add_table_to_schema(schema, table1)
    add_table_to_schema(schema, table2)

    assert table1.columns[0] in schema.columns()
    assert table2.columns[0] in schema.columns()

# add_table
def test_no_schema_cannot_have_tables_added(table):
    with pytest.raises(TypeError):
        add_table_to_schema(None, table)

def test_cannot_add_no_table_to_a_schema(schema):
    with pytest.raises(TypeError):
        add_table_to_schema(schema, None)

def test_add_table_assigns_schema_to_table(schema, table):
    add_table_to_schema(schema, table)

    assert table.schema == schema

def test_add_table_adds_the_table_to_schema(schema, table):
    add_table_to_schema(schema, table)

    assert table in schema.tables

# add_column
def test_cannot_add_column_to_no_table(column):
    with pytest.raises(TypeError):
        add_column_to_table(None, column)

def test_cannot_add_no_column_to_table(table):
    with pytest.raises(TypeError):
        add_column_to_table(table, None)

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

# Table
def test_table_start_without_primary_key(table):
    assert table.primary_key is None

# Column
def test_column_references(build_column, table):
    column = build_column(references=table)

    assert column.references == table

def test_column_cannot_be_both_primary_key_and_foreign_key(build_column, table):
    with pytest.raises(TypeError):
        build_column(primary_key=True, references=table)
