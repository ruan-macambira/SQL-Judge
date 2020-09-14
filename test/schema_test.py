#pylint: disable=missing-module-docstring, missing-function-docstring, redefined-outer-name
import pytest
from validate_schema import new_schema
from validate_schema.query_schema import QuerySchema

@pytest.fixture
def query_schema():
    query_schema = QuerySchema()
    query_schema.insert_to_schema('sequence', [{'name': 'sequence_one'}])
    query_schema.insert_to_schema('table', [
        {'name': 'table_one'}, {'name': 'table_two'}
    ])
    query_schema.insert_to_table('column', [
        {'table_name': 'table_one', 'name': 'column_one'},
        {'table_name': 'table_one', 'name': 'column_two'},
        {'table_name': 'table_two', 'name': 'column_three'}
    ])
    query_schema.insert_to_table('trigger', [
        {'table_name': 'table_one', 'name': 'trigger_one'}
    ])
    query_schema.insert_to_column('constraint', [
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'constraint_one'}
    ])
    query_schema.insert_to_column('index', [
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'index_one'}
    ])
    return query_schema

@pytest.fixture
def schema(query_schema):
    return new_schema.Schema(query_schema)

@pytest.fixture
def entity(schema):
    return new_schema.Entity(group='entity', name='entity_one', query_schema=schema, param_one='foo')

@pytest.fixture
def table(schema):
    return new_schema.Table(name='table_one', query_schema=schema)

# Schema
def test_schema_sequences_returns_schema_sequences(schema):
    assert [seq.name for seq in schema.sequences] == ['sequence_one']

def test_schema_function_returns_schema_functions(schema):
    assert schema.functions == []

def test_schema_procedures_returns_schema_procedures(schema):
    assert schema.procedures == []

def test_schema_tables_returns_table_entities(schema):
    assert [table.name for table in schema.tables] == ['table_one', 'table_two']

def test_schema_columns_returns_column_entities(schema):
    assert [column.name for column in schema.columns] == \
        ['column_one', 'column_two', 'column_three']

def test_schema_triggers_returns_trigger_entities(schema):
    assert [trigger.name for trigger in schema.triggers] == ['trigger_one']

def test_schema_constraint_returns_constraint_entities(schema):
    assert [cons.name for cons in schema.constraints] == ['constraint_one']

def test_schema_indexes_returns_index_entities(schema):
    assert [index.name for index in schema.indexes] == ['index_one']

# Entity
def test_entity_returns_additional_parameter(entity):
    assert entity.param_one == 'foo'

def test_entity_raise_attribute_error_if_not_a_additional_parameter(entity):
    with pytest.raises(AttributeError):
        entity.param_two # pylint: disable=pointless-statement

def test_entity_schema_returns_an_instance_of_schema(entity):
    assert isinstance(entity, new_schema.Entity)

def test_entity_name_returns_its_name(entity):
    assert entity.name == 'entity_one'

def test_entity_group_returns_its_group(entity):
    assert entity.group == 'entity'

def test_table_columns_returns_column_instances(table):
    assert table.columns[0].name == 'column_one'

def test_table_triggers_returns_trigger_instances(table):
    assert table.triggers[0].name == 'trigger_one'

def test_column_table_returns_table_instance(schema):
    assert new_schema.Column(name='column_one', table_name='table_one', query_schema=schema).table.name == 'table_one'

def test_column_constraints_returns_constraint_instances(schema):
    column =  new_schema.Column(name='column_one', table_name='table_one', query_schema=schema)
    assert column.constraints[0].name == 'constraint_one'

def test_column_indexes_returns_index_instances(schema):
    assert new_schema.Column(name='column_one', table_name='table_one', query_schema=schema).indexes[0].name == 'index_one'

def test_column_entity_column_returns_column_instance(schema):
    column_entity = new_schema.ColumnEntity(
        group='constraint', name='constraint_one', column_name='column_one',
        table_name='table_one', query_schema=schema
    )
    assert column_entity.column.name == 'column_one'
