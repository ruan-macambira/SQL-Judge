""" Fixtures """
# pylint: disable=redefined-outer-name
import sqlite3
import pytest
from lib.schema import Schema, Table, Column
from lib.schema import add_table, add_column
from lib.connection import SQLiteConnection, DBConnection
from lib.validation import ValidationConfig

# schema.Schema
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


# schema.Table
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

# schema.Column
@pytest.fixture
def build_column():
    """ Column Factory """
    def _build_column(name: str = 'column_name', col_type: str = 'column_type',
                      primary_key: bool = False, references: Table = None):
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

# validation.ValidationConfig
@pytest.fixture
def build_validation_config():
    """ Validation Configuration object Factory """
    def _build_validation_config(table_validations=None, column_validations=None,
                                 connection=None, ignore_tables=None):
        return ValidationConfig(
            connection=connection, table_validations=table_validations or [],
            column_validations=column_validations or [], ignore_tables=ignore_tables or []
        )
    return _build_validation_config

@pytest.fixture
def validation_config(build_validation_config, mock_conn):
    """ Basic validation Configuration File """
    return build_validation_config([], [], mock_conn, [])

# connection.SQLiteConnection
@pytest.fixture
def sqlite_conn():
    """ A Connection with a Database containing two tables
        - products: Empty Table
        - contacts: Containting one element """
    with sqlite3.connect(':memory:') as conn:
        conn.execute('CREATE TABLE products(name TEXT)')

        conn.execute('CREATE TABLE contacts(first_name TEXT, last_name TEXT)')
        conn.execute("INSERT INTO contacts(first_name, last_name) VALUES('Alan', 'Turing')")
        conn.commit()

        yield SQLiteConnection(connection=conn)


@pytest.fixture
def sqlite_conn_fk():
    """ A Connection with a Database containing two tables
        - products: Empty Table
        - contacts: Containting one element """
    with sqlite3.connect(':memory:') as conn:
        conn.execute('CREATE TABLE contacts(ID INTEGER PRIMARY KEY AUTOINCREMENT,'\
            'first_name TEXT, last_name TEXT)')
        conn.execute('CREATE TABLE services(id integer PRIMARY KEY,' \
            'contact_id integer references contacts(id))')
        conn.commit()

        yield SQLiteConnection(connection=conn)

class MockConnection(DBConnection):
    """ Mock classes to generate the return values of a connection object """
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
    """ Mock Database schema Adapter Factory """
    def _build_mock_conn(mock_values):
        return MockConnection(mock_values)
    return _build_mock_conn

@pytest.fixture
def mock_conn():
    """ A basic mock database schema adapter """
    return MockConnection({
        'table_one': [{'name': 'column_one', 'type': 'text'}],
        'table_two': [{'name': 'column_1', 'type': 'int'}, {'name': 'column_2', 'type': 'int'}]
    })
