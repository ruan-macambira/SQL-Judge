# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from types import ModuleType
import pytest
from sql_judge import validates
from sql_judge.schema_validations import (module_validations)

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
