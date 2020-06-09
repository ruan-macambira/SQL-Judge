import pytest
from lib.connection import DBConnection
from lib.generate_schema import generate_schema

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
def mock_conn():
    return MockConnection({
        'table_one': [{'name': 'column_one', 'type': 'text'}],
        'table_two': [{'name': 'column_1', 'type': 'int'}, {'name': 'column_2', 'type': 'int'}]
    })

def test_generate_schema_adds_tables_to_schema(schema, mock_conn):
    generate_schema(schema, mock_conn)

    assert [table.name for table in schema.tables] == ['table_one', 'table_two']

def test_generate_schema_add_columns_to_scehma(schema, mock_conn):
    generate_schema(schema, mock_conn)

    assert [column.name for column in schema.tables[0].columns] == ['column_one']
    assert [column.name for column in schema.tables[1].columns] == ['column_1', 'column_2']

def test_generate_schema_assigns_the_column_type_to_column(schema, mock_conn):
    generate_schema(schema, mock_conn)

    assert [column.type for column in schema.tables[0].columns] == ['text']
