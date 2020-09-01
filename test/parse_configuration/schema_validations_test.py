# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from types import ModuleType
import pytest
from validate_schema import validates
from validate_schema.parse_configuration.schema_validations import (
    module_validations, inspect_validations, to_configuration)

@pytest.fixture
def mockule():
    mock = ModuleType('mockule')
    mock.not_a_validations = lambda: None
    mock.validate_table = validates('table')(lambda x: x)
    mock.validate_invalid = validates('invalid')(lambda x: x)

    return mock

@pytest.fixture
def validations(mockule): # pylint: disable=redefined-outer-name
    return module_validations(mockule)

def test_module_validations_returns_functions_decotared_as_validations(mockule): # pylint: disable=redefined-outer-name
    assert set(module_validations(mockule)) == \
        set((mockule.validate_table, mockule.validate_invalid))

def test_inspect_validations_validates_the_entity_the_function_validates(validations): # pylint: disable=redefined-outer-name
    assert inspect_validations(validations) == ["'invalid' is not a valid entity"]

def test_to_configuration_export_function_to_a_format_accepted_by_the_configuration(validations, mockule): # pylint: disable=redefined-outer-name
    assert to_configuration(validations) == {
        'table': [mockule.validate_table],
        'invalid': [mockule.validate_invalid]
    }
