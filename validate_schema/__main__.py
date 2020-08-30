#! /usr/bin/python3
""" Main Module """
import sys
from .run import run
from .parse_configuration.build_configuration import ConfigurationBuilder

def default_config():
    with open('validate_schema/parse_configuration/default_configuration.json') as f:
        return f.read(None)

def user_config(filename):
    with open(filename) as f:
        return f.read(None)

def validate_schema(filename):
    """ Main function """
    config = ConfigurationBuilder.from_json(default_config()) \
        .merge(ConfigurationBuilder.from_json(user_config(filename))) \
        .build()    

    return run(config)

if __name__ == '__main__':
    report = validate_schema(sys.argv[1])

    for line in report:
        print(line)
