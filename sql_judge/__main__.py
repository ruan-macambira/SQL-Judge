#! /usr/bin/python3
""" Main Module """
import sys
import pkg_resources
from .validate import validate_entities
from .parse_configuration.build_configuration import ConfigurationBuilder
from .schema import Schema
from .export import formatted_output

def default_config():
    return pkg_resources.resource_string(
        'sql_judge.parse_configuration', 'default_configuration.json')

def user_config(filename):
    with open(filename) as file:
        return file.read(None)

def sql_judge(filenames):
    """ Main function """
    config_builder = ConfigurationBuilder.from_json(default_config())
    for filename in filenames:
        config_builder = config_builder.merge(ConfigurationBuilder.from_json(user_config(filename)))

    config = config_builder.build()
    schema = Schema(config.connection)
    report = validate_entities(config, schema)
    return formatted_output(report, config.export)

if __name__ == '__main__':
    output = sql_judge(sys.argv[1:])

    for line in output:
        print(line)
