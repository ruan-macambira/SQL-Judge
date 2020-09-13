#pylint: disable=missing-module-docstring
#pylint: disable=missing-function-docstring
import pytest
from validate_schema.query_schema import QuerySchema

@pytest.fixture
def query_schema():
    return QuerySchema()

def test_invalid_entity_raises_attribute_error(query_schema):
    with pytest.raises(AttributeError):
        query_schema.insert_to_schema('invalid_entity', [])

def test_batch_insert_and_select_tables(query_schema):
    tables = [{'name': 'table_one'}, {'name': 'table_two'}]
    query_schema.insert_to_schema('table', tables)
    assert query_schema.select_from_schema('table') == tables

def test_batch_insert_and_select_columns(query_schema):
    tables = [{'name': 'table_one'}, {'name': 'table_two'}]
    query_schema.insert_to_schema('table', tables)
    columns = [
        {'table_name': 'table_one', 'name': 'column_one'},
        {'table_name': 'table_one', 'name': 'column_two'},
        {'table_name': 'table_two', 'name': 'column_three'}
    ]
    query_schema.insert_to_table('column', columns)
    assert query_schema.select_from_table('column', table_name='table_one') == columns[0:2]

def test_batch_insert_and_select_constraints(query_schema):
    tables = [{'name': 'table_one'}, {'name': 'table_two'}]
    query_schema.insert_to_schema('table', tables)
    columns = [
        {'table_name': 'table_one', 'name': 'column_one'},
        {'table_name': 'table_one', 'name': 'column_two'},
        {'table_name': 'table_two', 'name': 'column_three'}
    ]
    query_schema.insert_to_table('column', columns)
    constraints = [
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'constraint_one'},
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'constraint_two'},
        {'table_name': 'talbe_one', 'column_name': 'column_two', 'name': 'constraint_three'},
        {'table_name': 'table_two', 'column_name': 'column_three', 'name': 'constraint_four'}
    ]
    query_schema.insert_to_column('constraint', constraints)
    assert query_schema.select_from_column('constraint', table_name='table_one', column_name='column_one') == constraints[0:2]
