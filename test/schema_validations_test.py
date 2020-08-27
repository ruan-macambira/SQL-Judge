# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from validate_schema.schema_validations import (
    extract_validations_from_module,
    inspect_validations,
    to_configuration
)
from . import validations

def extracted_validations():
    return extract_validations_from_module(validations)

def test_extract_validations():
    assert set(extracted_validations()) == set([
        validations.validate_table, validations.validate_column, validations.validate_invalid_entity
    ])

def test_inspect_validations():
    assert inspect_validations(extracted_validations()) == ["'invalid_entity' is not a valid entity"]

def test_to_configuration():
    assert to_configuration(extracted_validations()) == {
        'table': [validations.validate_table], 'column': [validations.validate_column],
        'invalid_entity': [validations.validate_invalid_entity]
    }