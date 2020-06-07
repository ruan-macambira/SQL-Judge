import pytest
from lib.validation import run_table_validations, run_tableset_validation

def pass_validation(_table):
    return None

def fail_validation(_table):
    return 'ERROR'

def test_run_validations_returns_a_list(table):
    assert run_table_validations(table, [pass_validation, fail_validation]) == ['ERROR']

def test_run_validations_no_messages_returns_empty_list(table):
    assert run_table_validations(table, [pass_validation]) == []

def test_cannot_run_validations_in_no_table():
    with pytest.raises(TypeError):
        run_table_validations(None, [pass_validation])

def test_cannot_run_no_validations_in_a_table(table):
    with pytest.raises(ValueError):
        run_table_validations(table, [])

def test_run_tableset_validations(table):
    assert run_tableset_validation([table], [fail_validation]) == [(table, 'ERROR')]
