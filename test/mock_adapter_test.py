# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

@pytest.fixture
def adapter(build_mock_conn):
    return build_mock_conn({
        'table_one': {
            'columns': {'column_one': 'int', 'column_two': 'int'},
            'primary_key': ['column_one'],
            'references': {'column_two': 'table_two'},
            'constraints': {'column_one': {
                'column_one_constraint': 'primary_key', 'column_one_constraint_2': 'not null'
                }},
            'triggers': {'trigger_one': 'hook_one'}
        }, 'table_two': {
            'columns': {'column_three': 'int', 'column_four': 'int'},
            'primary_key': ['column_three'],
            'indexes': {'column_three': 'column_three_index'},
            'triggers': {'trigger_two': 'hook_two'}
        }
    })

#pylint: disable=redefined-outer-name
def test_mock_adapter_tables(adapter):
    assert adapter.tables() == ['table_one', 'table_two']

def test_columns(adapter):
    assert adapter.columns() == [
        ('table_one', 'column_one', 'int'),
        ('table_one', 'column_two', 'int'),
        ('table_two', 'column_three', 'int'),
        ('table_two', 'column_four', 'int')
    ]

def test_primary_key(adapter):
    assert adapter.primary_keys() == [
        ('table_one', 'column_one'),
        ('table_two', 'column_three')
    ]

def test_no_primary_key(build_mock_conn):
    assert build_mock_conn({
        'table_one': {'columns': {'column_one': 'type_one'}}
    }).primary_keys() == []

def test_references(adapter):
    assert adapter.references() == [
        ('table_one', 'column_two', 'table_two')
    ]

def test_indexes(adapter):
    assert adapter.indexes() == [
        ('table_two', 'column_three', 'column_three_index')
    ]

def test_constraints(adapter):
    assert adapter.constraints() == [
        ('table_one', 'column_one', 'column_one_constraint', 'primary_key'),
        ('table_one', 'column_one', 'column_one_constraint_2', 'not null')
    ]

def test_triggers(adapter):
    assert adapter.triggers() == [
        ('table_one', 'trigger_one', 'hook_one'),
        ('table_two', 'trigger_two', 'hook_two')
    ]

def test_functions(build_mock_conn):
    assert build_mock_conn({}, functions_info=['function_one']).functions() == ['function_one']

def test_procedures(build_mock_conn):
    assert build_mock_conn(procedures_info=['procedure_one']).procedures() == ['procedure_one']
