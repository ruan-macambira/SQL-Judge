""" Fixtures """
# pylint: disable=redefined-outer-name
import pytest
from lib.schema import Schema, Table, Column
from lib.schema import add_table, add_column

@pytest.fixture
def schema():
    """ Basic Schema """
    return Schema()

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
    def _build_column(name: str = 'column_name', col_type: str = 'column_type'):
        return Column(name=name, col_type=col_type)
    return _build_column

@pytest.fixture
def column(build_column):
    """ Basic Column """
    return build_column()
