"""Validates the Schema"""
from .judge import judge, Judge

__all__ = ('judge', 'Judge', 'validates')

def validates(entity):
    """ Sets Entity to which the validation will run """
    def _validates(validation):
        validation.validates = entity
        return validation
    return _validates
