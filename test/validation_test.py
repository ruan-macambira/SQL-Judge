# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring
from pytest import fixture
from sql_judge.validate import validate_entities
from sql_judge.schema import Schema
from sql_judge import validates
from sql_judge.util import find

@fixture
def report(build_mock_conn):
    validations = validations={
        'Tables': [fail_validation],
        'Columns': [pass_validation],
        'Functions': [raise_validation]
    }
    schema = Schema(build_mock_conn({
        'tables': {'table_one': {'columns': {'column_one': {}}}, 'ignore': {}},
        'functions': {'function_one': {}}
    }))
    return validate_entities(validations, ['ignore'], schema)

def pass_validation(_table):
    return None

def fail_validation(_table):
    return 'ERROR'

def raise_validation(_table):
    raise Exception('something wrong happened')

# validate
def test_passed_tests_does_not_produce_outputs(report):
    assert 'Columns' not in report

def test_failed_tests_inserts_message_to_the_output(report):
    assert ('Tables', 'table_one', 'ERROR') in report

def test_validations_that_raises_an_exception_insert_message_to_the_output(report):
    error_message = 'validation "raise_validation" raised a Exception with the message "something wrong happened"'
    assert ('Functions', 'function_one', error_message) in report

# validates
@validates('table')
def validation(_table):
    return 'It runs!'

def test_validates_sets_validates_attribute():
    assert validation.validates == 'table'

def test_validates_returns_callable():
    assert validation(None) == 'It runs!'
