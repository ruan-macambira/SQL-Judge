""" Package responsible for transform the different ways of
inputting the configuration in a single Configuration Object """
from validate_schema import Configuration
from .schema_validations import module_validations, to_configuration

def _module_validations(module):
    validations = module_validations(module)
    return to_configuration(validations)
