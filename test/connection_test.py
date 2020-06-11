# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

def test_execute_select_empty_table_return_empty_list(sqlite_conn):
    assert sqlite_conn.execute('SELECT * FROM PRODUCTS') == []

def test_execute_select_non_empty_table_return_its_data(sqlite_conn):
    assert sqlite_conn.execute('SELECT * FROM CONTACTS') == \
            [{'first_name': 'Alan', 'last_name': 'Turing'}]

def test_execute_custom_select(sqlite_conn):
    assert sqlite_conn.execute('SELECT first_name FROM CONTACTS') == [{'first_name': 'Alan'}]


def test_tables_return_the_database_tables(sqlite_conn):
    assert sqlite_conn.tables() == ['CONTACTS', 'PRODUCTS']

def test_columns_return_the_tables_columns(sqlite_conn):
    assert sqlite_conn.columns('CONTACTS') == [
        {'name': 'FIRST_NAME', 'type': 'TEXT', 'primary_key': 'false'},
        {'name': 'LAST_NAME', 'type': 'TEXT', 'primary_key': 'false'}
    ]

def test_columns_marks_the_primary_key_column(sqlite_conn_fk):
    assert sqlite_conn_fk.columns('SERVICES')[0]['primary_key'] == 'true'

def test_columns_marks_the_foreign_key_references(sqlite_conn_fk):
    assert sqlite_conn_fk.columns('SERVICES')[1]['references'] == 'CONTACTS'
