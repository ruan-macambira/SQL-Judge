""" Fixtures """
# pylint: disable=redefined-outer-name
import pytest
import sqlite3
from lib.schema import Schema, Table, Column
from lib.schema import add_table, add_column
from lib.connection import SQLiteConnection, DBConnection

@pytest.fixture
def build_schema(build_table):
    """ Schema Factory """
    def _build_schema(tables: int = 0):
        at_schema = Schema()
        for i in range(tables):
            add_table(at_schema, build_table(name=f'table_{i}'))
        return at_schema
    return _build_schema

@pytest.fixture
def schema(build_schema):
    """ Basic Schema """
    return build_schema()

@pytest.fixture
def build_table(build_column):
    """ Table Factory """
    def _build_table(name: str = 'table_name', columns: int = 0):
        at_table = Table(name)
        for _ in range(columns):
            add_column(at_table, build_column())
        return at_table
    return _build_table

@pytest.fixture
def table(build_table):
    """ Basic Table """
    return build_table()

@pytest.fixture
def build_column():
    """ Column Factory """
    def _build_column(name: str = 'column_name', col_type: str = 'column_type', primary_key: bool = False, references: Table = None):
        return Column(name=name, col_type=col_type, primary_key=primary_key, references=references)
    return _build_column

@pytest.fixture
def column(build_column):
    """ Basic Column """
    return build_column()

@pytest.fixture
def primary_key_column(build_column):
    """ Column that serves as a Primary Key in a Table"""
    return build_column(primary_key=True)

@pytest.fixture
def sqlite_conn():
    """ A Connection with a Database containing two tables
        - products: Empty Table
        - contacts: Containting one element """
    with sqlite3.connect('temp/test.sqlite3') as conn:
        conn.execute('CREATE TABLE products(name TEXT)')

        conn.execute('CREATE TABLE contacts(first_name TEXT, last_name TEXT)')
        conn.execute("INSERT INTO contacts VALUES('Alan', 'Turing')")
        conn.commit()

    yield SQLiteConnection('temp/test.sqlite3')

    with sqlite3.connect('temp/test.sqlite3') as conn:
        conn.execute('DROP TABLE contacts')
        conn.execute('DROP TABLE products')
        conn.commit()

class MockConnection(DBConnection):
    def __init__(self, mock_values):
        self.mock_values = mock_values

    def execute(self, sql):
        return None

    def tables(self):
        return self.mock_values.keys()

    def columns(self, table_name):
        return self.mock_values[table_name]

@pytest.fixture
def build_mock_conn():
    def _build_mock_conn(mock_values):
        return MockConnection(mock_values)
    return _build_mock_conn

@pytest.fixture
def mock_conn():
    return MockConnection({
        'table_one': [{'name': 'column_one', 'type': 'text'}],
        'table_two': [{'name': 'column_1', 'type': 'int'}, {'name': 'column_2', 'type': 'int'}]
    })
    