# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from sql_judge import validates

@validates('table')
def validate_table(_table):
    return None

@validates('column')
def validate_column(_column):
    return None

@validates('invalid_entity')
def validate_invalid_entity(_invalid_entity):
    return None

def not_a_validation():
    return None
