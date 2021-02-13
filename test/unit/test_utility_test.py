# pylint: disable=C, redefined-outer-name
from types import ModuleType
from sql_judge.validation_test_util import Validator
from sql_judge import validates

from pytest import fixture

@fixture
def validations_module():
    mock = ModuleType('mockule')
    mock.table_fails = validates('table')(lambda _: 'ERROR_A')
    mock.table_fails_b = validates('table')(lambda _: 'ERROR_B')

    return mock

@fixture
def validator(validations_module):
    return Validator(validations_module)

def test_entity_is_invalid_when_it_has_invalidations(build_entity, validator):
    table = build_entity('Table', 'foo')

    assert validator.valid(table) is False

def test_entity_is_valid_when_has_no_invalidations(build_entity, validator):
    procedure = build_entity('Procedure', 'foo')

    assert validator.valid(procedure) is True

def test_validate_brings_invalidation_messages(build_entity, validator):
    table = build_entity('Table', 'foo')

    assert validator.validate(table) == ['ERROR_A', 'ERROR_B']
