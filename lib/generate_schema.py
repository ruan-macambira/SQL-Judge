""" Use the database connection to adapt its schema to the applications objects """
from lib.schema import (
    Schema, Table, Column, Index,
    add_table_to_schema, add_column_to_table, add_index_to_column
)
from lib.adapter import DBAdapter

def generate_schema(conn: DBAdapter) -> Schema:
    """ Generate an Schema objects containing the schema contained in the provided database """
    schema = Schema()
    for table_name in conn.tables():
        table: Table = Table(table_name)

        for name, col_type in conn.columns(table_name).items():
            column = Column(name=name, col_type=col_type,
                            primary_key=conn.primary_key(table_name, name))
            add_column_to_table(table, column)
        add_table_to_schema(schema, table)

    for column in schema.columns:
        for table in schema.tables:
            if conn.references(column.table.name, column.name) == table.name:
                column.references = table

    for column in schema.columns:
        index = Index(name=conn.index(column.table.name, column.name))

        add_index_to_column(column, index)

    return schema
