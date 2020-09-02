# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

@pytest.fixture
def adapter(query_adapter):
    return query_adapter({
        'table_one': {
            'columns': {'column_one': 'int', 'column_two': 'int'},
            'primary_key': ['column_one'],
            'references': {'column_two': 'table_two'},
            'constraints': {'column_one': {'column_one_constraint': 'primary_key'}},
            'triggers': {'trigger_one': 'hook_one'}
        }, 'table_two': {
            'columns': {'column_three': 'int', 'column_four': 'int'},
            'primary_key': ['column_three'],
            'indexes': {'column_three': 'column_three_index'}
        }
    })
#pylint: disable=redefined-outer-name
def test_mock_adapter_tables(adapter):
    assert adapter.tables() == ['table_one', 'table_two']

def test_columns(adapter):
    assert adapter.columns('table_one') == {'column_one': 'int', 'column_two': 'int'}

def test_foreign_key(adapter):
    assert adapter.primary_key('table_one', 'column_one') is True

def test_no_foreign_key(adapter):
    assert adapter.primary_key('table_one', 'column_two') is False

def test__references(adapter):
    assert adapter.references('table_one', 'column_two') == 'table_two'

def test_no_references(adapter):
    assert adapter.references('table_one', 'column_one') is None

def test_indexes(adapter):
    assert adapter.index('table_two', 'column_three') == 'column_three_index'

def test_no_indexes(adapter):
    assert adapter.index('table_two', 'column_four') is None

def test_constraints(adapter):
    assert adapter.constraints('table_one', 'column_one') == \
        {'column_one_constraint': 'primary_key'}

def test_no_constraints(adapter):
    assert adapter.constraints('table_one', 'column_two') == {}

def test_triggers(adapter):
    assert adapter.triggers('table_one') == {'trigger_one': 'hook_one'}

def test_no_triggers(adapter):
    assert adapter.triggers('table_two') == {}
