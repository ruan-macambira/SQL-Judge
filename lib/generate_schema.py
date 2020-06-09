from lib.schema import Schema, Table, Column, add_table, add_column
from lib.connection import DBConnection

def generate_schema(conn: DBConnection) -> Schema:
    schema = Schema()
    for table_name in conn.tables():
        table = Table(table_name)
        add_table(schema, table)

        for column_hash in conn.columns(table_name):
            column = Column(name=column_hash['name'], col_type=column_hash['type'])
            add_column(table, column)

    return schema
