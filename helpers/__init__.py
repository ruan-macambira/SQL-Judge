import sqlite3

def generate_sqlite_schema(filepath: str, schema_options: dict):
    with sqlite3.connect(filepath) as connection:
        cursor = connection.cursor()

        for table, columns in schema_options.items():
            cursor.execute(create_table_query(table, columns))

        cursor.close()

def create_table_query(table_name: str, columns: list):
    columns_sql = []
    for column_options in columns:
        columns_sql.append(create_table_column_subquery(column_options))

    return 'CREATE TABLE {} ({})'.format(table_name, ', '.join(columns_sql))

def create_table_column_subquery(options: dict):
    column_name = options['name']
    column_type = options['type']
    return f'{column_name} {column_type}'
