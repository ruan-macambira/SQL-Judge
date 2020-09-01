# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest
from validate_schema.parse_configuration.schema_validations import (
    module_validations,
    inspect_validations,
    to_configuration
)

@pytest.fixture
def extracted_validations(validations_module):
    return module_validations(validations_module)

def test_extract_validations(extracted_validations, validations_module): # pylint: disable=redefined-outer-name
    assert set(extracted_validations) == set([
        validations_module.validate_table, validations_module.validate_column, validations_module.validate_invalid_entity
    ])

def test_inspect_validations(extracted_validations): # pylint: disable=redefined-outer-name
    assert inspect_validations(extracted_validations) == ["'invalid_entity' is not a valid entity"]

def test_to_configuration(extracted_validations, validations_module): # pylint: disable=redefined-outer-name
    assert to_configuration(extracted_validations) == {
        'table': [validations_module.validate_table], 'column': [validations_module.validate_column],
        'invalid_entity': [validations_module.validate_invalid_entity]
    }
