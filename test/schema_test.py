#pylint: disable=missing-module-docstring
#pylint: disable=missing-function-docstring
import pytest
from lib.generate_schema import add_entity_to_schema

# Schema
def test_columns_returns_every_column_from_every_table(schema, build_table):
    table1 = build_table(columns=1)
    table2 = build_table(columns=1)

    add_entity_to_schema(schema, table1, 'tables')
    add_entity_to_schema(schema, table2, 'tables')

    assert schema.columns == table1.columns + table2.columns

def test_columns_in_an_empty_schema_returns_an_empty_list(schema):
    assert schema.columns == []

def test_indexes_in_an_empty_schema_returns_an_empty_list(schema):
    assert schema.indexes == []

def test_constraints_in_an_empty_schema_returns_an_empty_list(schema):
    assert schema.constraints == []

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
