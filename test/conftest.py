import pytest
from lib.schema import Schema, Table, Column
from lib.schema import add_table, add_column

@pytest.fixture
def schema():
    return Schema()

@pytest.fixture
def build_table(build_column):
    def _build_table(name: str = 'table_name', columns: int = 0):
        at_table = Table(name)
        for _ in range(columns):
            add_column(at_table, build_column())
        return at_table
    return _build_table

@pytest.fixture
def table():
    return Table(name='table_name')

@pytest.fixture
def build_column():
    def _build_column(name: str = 'column_name', col_type: str = 'column_type'):
        return Column(name=name, col_type=col_type)
    return _build_column

@pytest.fixture
def column():
    return Column(name='column_name', col_type='column_type')
