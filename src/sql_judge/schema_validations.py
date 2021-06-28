"""
Capture and organize schema validations
"""
import inspect
from collections import defaultdict
VALID_ENTITITES = [
    'table', 'column', 'trigger', 'constraint', 'function', 'procedure', 'index'
]

def _module_functions(module):
    return (element for (_, element) in inspect.getmembers(module, predicate=inspect.isfunction))

def module_validations(module):
    """ Extracts methods decorated as validations from the module """
    return [
        function for function in _module_functions(module)
        if getattr(function, 'validates', None) is not None
    ]

def to_configuration(validations):
    """ Converts a collection of validation functions to the configuration format """
    validations_dict = defaultdict(list)

    for validation in validations:
        validations_dict[validation.validates].append(validation)
    return validations_dict
