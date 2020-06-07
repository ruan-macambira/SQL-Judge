# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring
import pytest
from lib.validation import validate_entity, batch_validate_entities
from lib.validation import ValidationConfig, tables_to_validate

def pass_validation(_table):
    return None

def fail_validation(_table):
    return 'ERROR'

# run_table_validations
def test_run_validations_returns_a_list(table):
    assert validate_entity(table, [pass_validation, fail_validation]) == ['ERROR']

def test_run_validations_no_messages_returns_empty_list(table):
    assert validate_entity(table, [pass_validation]) == []

def test_cannot_run_validations_in_no_table():
    with pytest.raises(TypeError):
        validate_entity(None, [pass_validation])

def test_cannot_run_no_validations_in_a_table(table):
    with pytest.raises(ValueError):
        validate_entity(table, [])

# run_tableset_validation
def test_run_tableset_validations(table):
    assert batch_validate_entities([table], [fail_validation]) == [(table, 'ERROR')]


def test_cannot_run_tableset_with_no_validations(table):
    with pytest.raises(ValueError):
        batch_validate_entities([table], [])

# tables_to_validate
def test_tables_to_validate(build_schema):
    schema = build_schema(tables=2)
    config = ValidationConfig(ignore_tables=[schema.tables[0].name])

    assert schema.tables[0] not in tables_to_validate(schema, config)
    assert schema.tables[1] in tables_to_validate(schema, config)

def test_cannot_filter_with_no_config(schema):
    with pytest.raises(TypeError):
        assert tables_to_validate(schema, None)

def test_cannot_filter_no_schema():
    with pytest.raises(TypeError):
        assert tables_to_validate(None, ValidationConfig())
