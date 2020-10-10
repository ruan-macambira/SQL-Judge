# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from sql_judge import validates

def is_invalid(entity):
    if not entity.valid:
        return 'Invalid'

@validates('invalid_entity')
def validate_invalid_entity(_invalid_entity):
    return None

def not_a_validation():
    return None

@validates('table')
def val_table(table):
    return is_invalid(table)

@validates('column')
def val_column(column):
    return is_invalid(column)
