#pylint: disable=missing-module-docstring, missing-function-docstring, redefined-outer-name
import pytest
from sql_judge import schema as mschema

@pytest.fixture
def query_schema(build_mock_conn):
    return build_mock_conn({
        'tables': {
            'table_one': {
                'columns': {
                    'column_one': {
                        'constraints': {'constraint_one': {}},
                        'primary_key': True,
                        'indexes': {'index_one': {}}
                    },
                    'column_two': { 'references': 'table_two'}},
                'triggers': {'trigger_one': {}}
            }, 'table_two': {'columns': {'column_three': {}}}
        }, 'sequences': {'sequence_one': {}}
    })

@pytest.fixture
def schema(query_schema):
    return mschema.Schema(query_schema)

@pytest.fixture
def entity(schema):
    return mschema.Entity(group='entity', name='entity_one', schema=schema, param_one='foo')

@pytest.fixture
def table(schema):
    return mschema.Table(name='table_one', schema=schema)

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

def test_table_primary_key(schema):
    assert schema.tables[0].primary_key == schema.tables[0].columns[0]

def test_column_primary_key(schema):
    assert [col.primary_key for col in schema.tables[0].columns] == [True, False]

def test_column_references(schema):
    assert schema.tables[0].columns[1].references == schema.tables[1]

def test_schema_constraint_returns_constraint_entities(schema):
    assert [cons.name for cons in schema.constraints] == ['constraint_one']

def test_schema_indexes_returns_index_entities(schema):
    assert [index.name for index in schema.indexes] == ['index_one']

# Entity
def test_entity_name_is_its_group_capitalized():
    assert mschema.Entity(group='table', name='', schema=None).__name__ == 'Table'

def test_entity_returns_additional_parameter(entity):
    assert entity.param_one == 'foo'

def test_entity_raise_attribute_error_if_not_a_additional_parameter(entity):
    with pytest.raises(AttributeError):
        entity.param_two # pylint: disable=pointless-statement

def test_entity_schema_returns_an_instance_of_schema(entity):
    assert isinstance(entity, mschema.Entity)

def test_entity_name_returns_its_name(entity):
    assert entity.name == 'entity_one'

# Table
def test_table_columns_returns_column_instances(table):
    assert table.columns[0].name == 'column_one'

def test_table_triggers_returns_trigger_instances(table):
    assert table.triggers[0].name == 'trigger_one'


# Column
def test_column_table_returns_table_instance(schema):
    assert schema.columns[0].table == schema.tables[0]

def test_column_constraints_returns_constraint_instances(schema):
    assert schema.columns[0].constraints[0] == schema.constraints[0]

def test_column_indexes_returns_index_instances(schema):
    assert schema.columns[0].index == schema.indexes[0]

def test_column_entity_column_returns_column_instance(schema):
    column_entity = mschema.Constraint(
        name='constraint_one', column='column_one',
        table='table_one', schema=schema
    )
    assert column_entity.column == schema.columns[0]
