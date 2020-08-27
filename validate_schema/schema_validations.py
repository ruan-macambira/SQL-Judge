"""
Capture and organize schema validations
"""
import inspect
from collections import defaultdict
VALID_ENTITITES = [
    'table', 'column', 'trigger', 'constraint', 'function', 'procedure', 'index'
]

def _extract_function_from_module(module):
    return (element for (_, element) in inspect.getmembers(module) if inspect.isfunction(element))

def extract_validations_from_module(module):
    """ Extracts methods decorated as validations from the module """
    return [
        function for function in _extract_function_from_module(module)
        if getattr(function, 'validates', None) is not None
    ]

def inspect_validations(validations):
    """ Returns validation_warnings """
    return [
        f"'{validation.validates}' is not a valid entity"
        for validation in validations
        if validation.validates.lower() not in VALID_ENTITITES
    ]

def to_configuration(validations):
    """ Converts a collection of validation fucntions to the configuration format """
    validations_dict = defaultdict(list)

    for validation in validations:
        validations_dict[validation.validates].append(validation)
    return validations_dict
