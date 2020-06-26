# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

@pytest.fixture
def adapter(build_mock_conn):
    return build_mock_conn({
        'table_one': {
            'columns': {'column_one': 'int', 'column_two': 'int'},
            'primary_key': ['column_one'],
            'references': {'column_two': 'table_two'}
        }, 'table_two': {
            'columns': {'column_three': 'int', 'column_four': 'int'},
            'primary_key': ['column_three']
        }
    })

def test_mock_adapter_tables(adapter):
    assert adapter.tables() == ['table_one', 'table_two']

def test_mock_adapter_columns(adapter):
    assert adapter.columns('table_one') == {'column_one': 'int', 'column_two': 'int'}

def test_mock_adapter_foreign_key(adapter):
    assert adapter.primary_key('table_one', 'column_one') is True

def test_mock_adapter_no_foreign_key(adapter):
    assert adapter.primary_key('table_one', 'column_two') is False

def test_mock_adapter_references(adapter):
    assert adapter.references('table_one', 'column_two') == 'table_two'

def test_no_references(adapter):
    assert adapter.references('table_one', 'column_one') is None
