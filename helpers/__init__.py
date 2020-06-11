""" General use helpers """
import sqlite3
from typing import Dict, Optional, List

def generate_sqlite_schema(schema_options: Dict[str, list],
                           filepath: str = ':memory:')-> Optional[sqlite3.Connection]:
    """Generates a SQLite Database schema based the options supplied

    Params:
        schema_options -- Dict[str, list]. The keys are the table names
        and value a list containing dicts, each representing a column in the table.
        It is mandatory that every table has at least one column.
            column options:
                name -- the column name
                type -- the column data type
                primary_key(Optional) -- flags if the column is a primary key or not
                references(Optional) -- if it references another table(i.e foreign key),
                    send its name
        filepath(Optional) -- the file where the generated schema will be present.
        It is stored in memory only by default

    Return:
        if a filepath is present, it returns None.
        if not, it returns the SQlite connection object
    """
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()

    for table, columns in schema_options.items():
        cursor.execute(_create_table_query(table, columns))

    cursor.close()

    if filepath == ':memory:':
        return connection

    connection.close()
    return None

def _create_table_query(table_name: str, columns: List[dict]):
    columns_sql = []
    for column_options in columns:
        columns_sql.append(_create_table_column_partial_query(column_options))

    return 'CREATE TABLE {} ({})'.format(table_name, ', '.join(columns_sql))

def _create_table_column_partial_query(options: Dict[str, str]):
    column_name = options['name']
    column_type = options['type']

    if 'primary_key' in options and options['primary_key'] == 'true':
        return '{} {} PRIMARY KEY'.format(column_name, column_type)
    if 'references' in options and options['references'] is not None:
        return '{} {} REFERENCES {}'.format(column_name, column_type, options['references'])
    return f'{column_name} {column_type}'
