""" Package responsible for transform the different ways of
inputting the configuration in a single Configuration Object """
from validate_schema.configuration import Configuration
from .schema_validations import module_validations, to_configuration

def configuration_from_module(options):
    """ Constrct Configuration file from module """
    return Configuration(
        connection=options.adapter(),
        validations=_module_validations(options.validations()),
        ignore_tables=options.ignore_tables(),
        export=options.export()
    )

def _module_validations(module):
    validations = module_validations(module)
    return to_configuration(validations)
