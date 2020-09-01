# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring
from validate_schema.validate import validate_entity
from validate_schema import validates

def pass_validation(_table):
    return None

def fail_validation(_table):
    return 'ERROR'

# run_table_validations
def test_run_validations_returns_a_list(table):
    assert validate_entity(table, [pass_validation, fail_validation]) == ['ERROR']

def test_run_validations_no_messages_returns_empty_list(table):
    assert validate_entity(table, [pass_validation]) == []

# validates
@validates('table')
def validation(_table):
    return 'It runs!'

def test_validates_sets_validates_attribute():
    assert validation.validates == 'table'

def test_validates_returns_callable():
    assert validation(None) == 'It runs!'
