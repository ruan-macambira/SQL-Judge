from lib.schema import Schema, Table, Column
from lib.schema import add_column, add_table

# Schema
def test_columns_returns_every_column_from_every_table(schema, build_table):
    table1 = build_table(columns=1)
    table2 = build_table(columns=1)

    add_table(schema, table1)
    add_table(schema, table2)

    assert table1.columns[0] in schema.columns()
    assert table2.columns[0] in schema.columns()

# add_table
def test_add_table_assigns_schema_to_table(schema, table):
    add_table(schema, table)

    assert table.schema == schema


def test_dd_table_adds_the_table_to_schema(schema, table):
    add_table(schema, table)

    assert table in schema.tables

# Table

# add_column
def test_add_column_assigns_table_to_column(table, column):
    add_column(table, column)

    assert column.table == table

def test_add_column_adds_the_column_to_table(table, column):
    add_column(table, column)

    assert column in table.columns
