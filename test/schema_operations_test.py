# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from validate_schema.generate_schema import (
    add_index_to_column, add_entity_to_schema, add_subentity_to_entity
)

# add_entity_to_schema
def test_add_entity_assigns_schema_to_entity(schema, table):
    add_entity_to_schema(schema, table, 'tables')

    assert table.schema == schema

def test_add_entity_adds_the_entity_to_schema(schema, table):
    add_entity_to_schema(schema, table, 'tables')

    assert table in schema.tables

# add_subentity_to_entity
def test_add_subentity_assigns_entity_to_subentity(table, column):
    add_subentity_to_entity(table, 'table', column, 'columns')

    assert column.table == table

def test_add_subentity_assigns_subentity_to_entity(table, column):
    add_subentity_to_entity(table, 'table', column, 'columns')

    assert column in table.columns

def test_add_column_with_primary_key(table, primary_key_column):
    add_subentity_to_entity(table, 'table', primary_key_column, 'columns')

    assert table.primary_key == primary_key_column

# add_index_to_column
def test_add_index_assigns_column_to_index(column, index):
    add_index_to_column(column, index)

    assert column.index == index

def test_add_index_assigns_index_to_column(column, index):
    add_index_to_column(column, index)

    assert index.column == column
