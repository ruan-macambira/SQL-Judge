#pylint: disable=missing-module-docstring
#pylint: disable=missing-function-docstring
import pytest
from validate_schema.query_schema import query_schema_from_adapter
from validate_schema.mock_adapter import MockAdapter

@pytest.fixture
def query_schema():
    return query_schema_from_adapter(MockAdapter({
        'table_one': {
            'columns': {
                'column_one': 'type_one', 'column_two': 'type_two'
            }, 'constraints': {
                'column_one': {
                    'constraint_one': 'ctype_one',
                    'constraint_two': 'ctype_two'
                }, 'column_two': {
                    'constraint_three': 'ctype_three'
                }
            }
        }, 'table_two': {
            'columns': {
                'column_three': 'type_three'
            }, 'constraints': {
                'column_three': {
                    'constraint_four': 'ctype_four'
                }
            }
        }
    }))

def test_invalid_entity_raises_attribute_error(query_schema):
    with pytest.raises(AttributeError):
        query_schema.insert('invalid_entity', [])

def test_batch_insert_and_select_tables(query_schema):
    tables = [{'name': 'table_one'}, {'name': 'table_two'}]
    assert query_schema.select('table') == tables

def test_batch_insert_and_select_schema_column(query_schema):
    columns = [
        {'table_name': 'table_one', 'name': 'column_one'},
        {'table_name': 'table_one', 'name': 'column_two'},
        {'table_name': 'table_two', 'name': 'column_three'}
    ]
    assert query_schema.select('column') == columns

def test_batch_insert_and_select_schema_constraints(query_schema):
    constraints = [
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'constraint_one'},
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'constraint_two'},
        {'table_name': 'table_one', 'column_name': 'column_two', 'name': 'constraint_three'},
        {'table_name': 'table_two', 'column_name': 'column_three', 'name': 'constraint_four'}
    ]
    assert query_schema.select('constraint') == constraints
