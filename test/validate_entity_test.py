# pylint: disable=C, redefined-outer-name
import pytest
from validate_schema.validation_entity import needs_validation, canonical_name

@pytest.fixture
def schema(serial_schema):
    return serial_schema({
        'tables': {'table': {'columns': {'column': {'constraints': {'constraint': {}}}}}},
        'functions': {'function': {}}})

@pytest.fixture
def entity(schema):
    return schema.functions[0]

@pytest.fixture
def table(schema):
    return schema.tables[0]

@pytest.fixture
def table_entity(schema):
    return schema.columns[0]

@pytest.fixture
def column_entity(schema):
    return schema.constraints[0]

# needs_validation
def test_needsval_not_using_an_entity_raises_an_error():
    with pytest.raises(TypeError):
        needs_validation(None, [])

def test_generic_entity_always_succeed(entity):
    assert needs_validation(entity, []) is True

def test_table_passes_if_its_name_is_not_in_ignore_list(table):
    assert needs_validation(table, []) is True

def test_table_fails_if_its_name_is_in_ignore_list(table):
    assert needs_validation(table, ['table']) is False

def test_table_entity_succeeds_if_table_succeeds(table_entity):
    assert needs_validation(table_entity, []) is True

def test_table_entity_fails_if_table_fails(table_entity):
    assert needs_validation(table_entity, ['table']) is False

def test_column_entity_succeeds_if_table_succeeds(column_entity):
    assert needs_validation(column_entity, []) is True

def test_column_entity_fails_if_table_fails(column_entity):
    assert needs_validation(column_entity, ['table']) is False

# canonical_name
def test_canname_not_using_an_entity_raises_an_error():
    with pytest.raises(TypeError):
        needs_validation(None, [])

def test_generic_entity_has_its_name_as_canonical(entity):
    assert canonical_name(entity) == entity.name

def test_table_entity_has_its_and_its_table_name_as_canonical(table_entity):
    assert canonical_name(table_entity) == f'{table_entity.table.name}.{table_entity.name}'

def test_column_entity_has_its_column_and_itself_names(column_entity):
    assert canonical_name(column_entity) == f'{column_entity.table.name}.{column_entity.column.name}.{column_entity.name}'
