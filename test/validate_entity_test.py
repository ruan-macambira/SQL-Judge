import pytest
from validate_schema.validation_entity import ValidationEntity

@pytest.fixture
def schema(serial_schema):
    return serial_schema({
        'tables': {'table': {'columns': {'column': {'constraints': {'constraint': {}}}}}},
        'functions': {'function': {}}})

@pytest.fixture
def val_entity(schema):
    return ValidationEntity(schema.functions[0])

@pytest.fixture
def val_table(schema):
    return ValidationEntity(schema.tables[0])

@pytest.fixture
def val_tentity(schema):
    return ValidationEntity(schema.columns[0])

@pytest.fixture
def val_centity(schema):
    return ValidationEntity(schema.constraints[0])

# needs_validation
def test_needsval_not_using_an_entity_raises_an_error():
    with pytest.raises(TypeError):
        ValidationEntity(None).needs_validation([])

def test_generic_entity_always_succeed(val_entity):
    assert val_entity.needs_validation([]) is True

def test_table_passes_if_its_name_is_not_in_ignore_list(val_table):
    assert val_table.needs_validation([]) is True

def test_table_fails_if_its_name_is_in_ignore_list(val_table):
    assert val_table.needs_validation(['table']) is False

def test_table_entity_succeeds_if_table_succeeds(val_tentity):
    assert val_tentity.needs_validation([]) is True

def test_table_entity_fails_if_table_fails(val_tentity):
    assert val_tentity.needs_validation(['table']) is False

def test_column_entity_succeeds_if_table_succeeds(val_centity):
    assert val_centity.needs_validation([]) is True

def test_column_entity_fails_if_table_fails(val_centity):
    assert val_centity.needs_validation(['table']) is False

# canonical_name
def test_canname_not_using_an_entity_raises_an_error():
    with pytest.raises(TypeError):
        ValidationEntity(None).needs_validation([])

def test_generic_entity_has_its_name_as_canonical(val_entity):
    assert val_entity.canonical_name() == val_entity.entity.name

def test_table_entity_has_its_and_its_table_name_as_canonical(val_tentity):
    entity = val_tentity.entity
    assert val_tentity.canonical_name() == f'{entity.table.name}.{entity.name}'

def test_column_entity_has_its_column_and_itself_names(val_centity):
    entity = val_centity.entity
    assert val_centity.canonical_name() == f'{entity.table.name}.{entity.column.name}.{entity.name}'

# is_valid
def test_it_is_valid_when_has_no_errors(val_entity):
    assert val_entity.is_valid() is True

def test_it_is_not_valid_when_has_at_least_one_error(val_entity):
    val_entity.errors.append('ERROR')
    assert val_entity.is_valid() is False
