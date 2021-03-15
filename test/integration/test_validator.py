# pylint: disable=C, redefined-outer-name
from collections import namedtuple
from pytest import fixture
from validations import validation
from sql_judge.validation_test_util import Validator

Entity = namedtuple('Entity', ['group', 'name', 'valid'])

@fixture
def validator() -> Validator:
    return Validator(validation)

@fixture
def entity():
    def _(group: str, name: str, valid: bool):
        return Entity(group, name, valid)
    return _

def validator_run_validations(validator, entity):
    assert validator.valid(entity('table', 'table_name', True))

def validator_returns_errors(validator, entity):
    assert validator.validate(entity('table', '', False)) == ['Invalid']
