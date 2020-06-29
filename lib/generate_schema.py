""" Use the database connection to adapt its schema to the applications objects """
from lib.schema import Schema, Table, Column, add_table_to_schema, add_column_to_table
from lib.adapter import DBAdapter

def generate_schema(conn: DBAdapter) -> Schema:
    """ Generate an Schema objects containing the schema contained in the provided database """
    schema = Schema()
    for table_name in conn.tables():
        table: Table = Table(table_name)
        add_table_to_schema(schema, table)

    for table in schema.tables:
        for name, col_type in conn.columns(table.name).items():
            column = Column(name=name, col_type=col_type,
                            primary_key=conn.primary_key(table.name, name))

            for xtable in schema.tables:
                if conn.references(table.name, name) == xtable.name:
                    column.references = xtable
            add_column_to_table(table, column)

    return schema
