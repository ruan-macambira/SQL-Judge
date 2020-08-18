#! /usr/bin/python3
import sys
import importlib
from .run import run
from .configuration import Configuration

def validate_schema(filename):
    options = importlib.import_module(filename)

    config = Configuration(
        connection=options.adapter(),
        validations=options.validations(),
        ignore_tables=options.ignore_tables(),
        export=options.export()
    )
    return run(config)

if __name__ == '__main__':
    report = validate_schema(sys.argv[1])

    for line in report:
        print(line)
