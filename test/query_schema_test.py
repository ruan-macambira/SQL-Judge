#pylint: disable=missing-module-docstring
#pylint: disable=missing-function-docstring
import pytest
from validate_schema.query_schema import query_schema_from_adapter
from validate_schema.serialized_adapter import SerializedAdapter

@pytest.fixture
def query_schema():
    return query_schema_from_adapter(SerializedAdapter({
        'tables': {
            'table_one': {
                'columns': {'column_one': {'type': 'type_one', 'constraints': {
                    'constraint_one': {'type': 'ctype_one'},
                    'constraint_two': {'type': 'ctype_two'}
                }}, 'column_two': {'type': 'type_two', 'constraints': {
                    'constraint_three': {'type': 'ctype_three'}
                }}}
            }, 'table_two': {
                'columns': {'column_three': {'type': 'type_three', 'constraints': {
                    'constraint_four': {'type': 'ctype_four'}
                }}}
            }
        }
    }))

def test_invalid_entity_raises_attribute_error(query_schema):
    with pytest.raises(AttributeError):
        query_schema.insert('invalid_entity', [])

def test_batch_insert_and_select_tables(query_schema):
    tables = [{'name': 'table_one'}, {'name': 'table_two'}]
    assert query_schema.select('tables') == tables

def test_batch_insert_and_select_schema_column(query_schema):
    columns = [
        {'table': 'table_one', 'name': 'column_one', 'type': 'type_one'},
        {'table': 'table_one', 'name': 'column_two', 'type': 'type_two'},
        {'table': 'table_two', 'name': 'column_three', 'type': 'type_three'}
    ]
    assert query_schema.select('columns') == columns

def test_batch_insert_and_select_schema_constraints(query_schema):
    constraints = [
        {'table': 'table_one', 'column': 'column_one', 'name': 'constraint_one', 'type': 'ctype_one'},
        {'table': 'table_one', 'column': 'column_one', 'name': 'constraint_two', 'type': 'ctype_two'},
        {'table': 'table_one', 'column': 'column_two', 'name': 'constraint_three', 'type': 'ctype_three'},
        {'table': 'table_two', 'column': 'column_three', 'name': 'constraint_four', 'type': 'ctype_four'}
    ]
    assert query_schema.select('constraints') == constraints
