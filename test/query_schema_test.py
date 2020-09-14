#pylint: disable=missing-module-docstring
#pylint: disable=missing-function-docstring
import pytest
from validate_schema.query_schema import QuerySchema

@pytest.fixture
def query_schema():
    return QuerySchema()

def test_invalid_entity_raises_attribute_error(query_schema):
    with pytest.raises(AttributeError):
        query_schema.insert('invalid_entity', [])

def test_batch_insert_and_select_tables(query_schema):
    tables = [{'name': 'table_one'}, {'name': 'table_two'}]
    query_schema.insert('table', tables)
    assert query_schema.select('table') == tables

def test_batch_insert_and_select_schema_column(query_schema):
    tables = [{'name': 'table_one'}, {'name': 'table_two'}]
    query_schema.insert('table', tables)
    columns = [
        {'table_name': 'table_one', 'name': 'column_one'},
        {'table_name': 'table_one', 'name': 'column_two'},
        {'table_name': 'table_two', 'name': 'column_three'}
    ]
    query_schema.insert('column', columns)
    assert query_schema.select('column') == columns

def test_batch_insert_and_select_schema_constraints(query_schema):
    tables = [{'name': 'table_one'}, {'name': 'table_two'}]
    query_schema.insert('table', tables)
    columns = [
        {'table_name': 'table_one', 'name': 'column_one'},
        {'table_name': 'table_one', 'name': 'column_two'},
        {'table_name': 'table_two', 'name': 'column_three'}
    ]
    query_schema.insert('column', columns)
    constraints = [
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'constraint_one'},
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'constraint_two'},
        {'table_name': 'talbe_one', 'column_name': 'column_two', 'name': 'constraint_three'},
        {'table_name': 'table_two', 'column_name': 'column_three', 'name': 'constraint_four'}
    ]
    query_schema.insert('constraint', constraints)
    assert query_schema.select('constraint') == constraints
