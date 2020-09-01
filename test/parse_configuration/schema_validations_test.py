from types import ModuleType
import pytest
from validate_schema import validates
from validate_schema.parse_configuration.schema_validations import (
    module_validations, inspect_validations, to_configuration)

@pytest.fixture
def mockule():
    mock = ModuleType('mockule')
    mock.no_validation = lambda: None
    mock.validation = validates('table')(lambda x: x)
    mock.invalidation = validates('foo')(lambda x: x)

    return mock

@pytest.fixture
def validations(mockule):
    return module_validations(mockule)

def test_module_validations(mockule):
    assert set(module_validations(mockule)) == set((mockule.validation, mockule.invalidation))

def test_inspect_validations(validations):
    assert inspect_validations(validations) == ["'foo' is not a valid entity"]

def test_to_configuration(validations, mockule):
    assert to_configuration(validations) == {
        'table': [mockule.validation],
        'foo': [mockule.invalidation]
    }
