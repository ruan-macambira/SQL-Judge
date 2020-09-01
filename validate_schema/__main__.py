#! /usr/bin/python3
""" Main Module """
import sys
import pkg_resources
from .run import run
from .parse_configuration.build_configuration import ConfigurationBuilder

def default_config():
    return pkg_resources.resource_string(
        'validate_schema.parse_configuration', 'default_configuration.json')

def user_config(filename):
    with open(filename) as file:
        return file.read(None)

def validate_schema(filenames):
    """ Main function """
    config_builder = ConfigurationBuilder.from_json(default_config())
    for filename in filenames:
        config_builder = config_builder.merge(ConfigurationBuilder.from_json(user_config(filename)))
    config = config_builder.build()

    return run(config)

if __name__ == '__main__':
    report = validate_schema(sys.argv[1:])

    for line in report:
        print(line)
