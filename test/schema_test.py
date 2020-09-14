#pylint: disable=missing-module-docstring
#pylint: disable=missing-function-docstring
import pytest
from validate_schema import new_schema
from validate_schema.query_schema import QuerySchema

@pytest.fixture
def query_schema():
    qs = QuerySchema()
    qs.insert_to_schema('table', [{'name': 'table_one'}])
    qs.insert_to_table('column', [
        {'table_name': 'table_one', 'name': 'column_one'},
        {'table_name': 'table_one', 'name': 'column_two'}
    ])
    qs.insert_to_table('trigger', [
        {'table_name': 'table_one', 'name': 'trigger_one'}
    ])
    qs.insert_to_column('constraint', [
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'constraint_one'}
    ])
    qs.insert_to_column('index', [
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'index_one'}
    ])
    return qs

@pytest.fixture
def entity(query_schema):
    return new_schema.Entity(group='entity', name='entity_one', query_schema=query_schema, param_one='foo')

@pytest.fixture
def table(query_schema):
    return new_schema.Table(name='table_one', query_schema=query_schema)

def test_entity_returns_additional_parameter(entity):
    assert entity.param_one == 'foo'

def test_entity_raise_attribute_error_if_not_a_additional_parameter(entity):
    with pytest.raises(AttributeError):
        entity.param_two

def test_entity_schema_returns_an_instance_of_schema(entity):
    assert type(entity.schema) is new_schema.Schema

def test_entity_name_returns_its_name(entity):
    assert entity.name == 'entity_one'

def test_entity_group_returns_its_group(entity):
    assert entity.group == 'entity'

def test_table_columns_returns_column_instances(table):
    assert table.columns[0].name == 'column_one'

def test_table_triggers_returns_trigger_instances(table):
    assert table.triggers[0].name == 'trigger_one'

def test_column_table_returns_table_instance(query_schema):
    assert new_schema.Column(name='column_one', table_name='table_one', query_schema=query_schema).table.name == 'table_one'

def test_column_constraints_returns_constraint_instances(query_schema):
    assert new_schema.Column(name='column_one', table_name='table_one', query_schema=query_schema).constraints[0].name == 'constraint_one'

def test_column_indexes_returns_index_instances(query_schema):
    assert new_schema.Column(name='column_one', table_name='table_one', query_schema=query_schema).indexes[0].name == 'index_one'

def test_column_entity_column_returns_column_instance(query_schema):
    column_entity = new_schema.ColumnEntity(
        group='constraint', name='constraint_one', column_name='column_one',
        table_name='table_one', query_schema=query_schema
    )
    assert column_entity.column.name == 'column_one'
