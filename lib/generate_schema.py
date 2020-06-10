from lib.schema import Schema, Table, Column, add_table, add_column
from lib.connection import DBConnection

def generate_schema(conn: DBConnection) -> Schema:
    schema = Schema()
    for table_name in conn.tables():
        table: Table = Table(table_name)
        add_table(schema, table)

        for column_hash in conn.columns(table_name):
            column = Column(name=column_hash['name'], col_type=column_hash['type'],
                            primary_key=as_bool(sanitize(column_hash, 'primary_key', 'false')))
            add_column(table, column)

    return schema

def sanitize(unsanitized_hash: dict, key, default=None):
    return unsanitized_hash[key] if key in unsanitized_hash else default

def as_bool(not_bool: str) -> bool:
    return {'false': False, 'true': True}[not_bool]
