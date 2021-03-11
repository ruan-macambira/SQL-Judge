#! /usr/bin/python3
""" Main Module """
import sys
import json
import logging
import pkg_resources
from .validate import validate_entities
from .parse_configuration.build_configuration import ConfigurationBuilder
from .schema import Schema
from .export import formatted_output

def default_config():
    """default configuration file"""
    return json.loads(pkg_resources.resource_string('sql_judge.parse_configuration',
                                                    'default_configuration.json'))

def user_config(filename):
    """user-provided configuration file"""
    try:
        with open(filename) as file:
            return json.loads(file.read(None))
    except FileNotFoundError as fnf:
        raise RuntimeError(f"File '{filename}' could not be found") from fnf
    except json.JSONDecodeError as jsond:
        raise RuntimeError(f"Error while parsing '{filename}'") from jsond

def sql_judge(filenames) -> list:
    """ Main function """
    if len(filenames) == 0:
        logging.error('At least one configuration file must be provided')
        return []

    try:
        config_builder = ConfigurationBuilder.load(default_config())
        for filename in filenames:
            config_builder = config_builder.merge(ConfigurationBuilder.load(user_config(filename)))

        config = config_builder.build()
        schema = Schema(config.connection)
        report = validate_entities(config.validations, config.ignore_tables, schema)
        return formatted_output(report, config.export)
    except RuntimeError as err:
        logging.error(str(err))
        return []

def main():
    """Console Scripts entry point"""
    output = sql_judge(sys.argv[1:])

    for line in output:
        print(line)


if __name__ == '__main__':
    main()
