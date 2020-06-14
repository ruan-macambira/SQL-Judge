""" Use the database connection to adapt its schema to the applications objects """
from lib.schema import Schema, Table, Column, add_table, add_column
from lib.adapter import DBAdapter

def generate_schema(conn: DBAdapter) -> Schema:
    """ Generate an Schema objects containing the schema contained in the provided database """
    schema = Schema()
    for table_name in conn.tables():
        table: Table = Table(table_name)
        add_table(schema, table)

    for table in schema.tables:
        for column_hash in conn.columns(table.name):
            column = Column(name=column_hash['name'], col_type=column_hash['type'],
                            primary_key=_as_bool(_sanitize(column_hash, 'primary_key', 'false')))

            for xtable in schema.tables:
                if _sanitize(column_hash, 'references', None) == xtable.name:
                    column.references = xtable
            add_column(table, column)

    return schema

def _sanitize(unsanitized_hash: dict, key, default=None):
    return unsanitized_hash[key] if key in unsanitized_hash else default

def _as_bool(not_bool: str) -> bool:
    return {'false': False, 'true': True}[not_bool]
