from typing import Collection, Callable, Dict, IO
from sys import stdout, stderr
from .adapter import AbstractAdapter
from .validate import validate_entities
from .export import formatted_output
from .schema import Schema
from .validation_entity import needs_validation
from .adapter import AbstractAdapter
from .schema_validations import module_validations, to_configuration

__all__ = ('judge',)

def judge(
    adapter: AbstractAdapter,
    validations_module: Dict[str, Collection[Callable]],
    ignore_tables: Collection[str] = tuple(),
    export: str = 'CLI',
    out: IO = stdout,
    err: IO = stderr
):
    """Default caller for SQL Judge"""
    try:
        schema = Schema(adapter)
        validations = to_configuration(module_validations(validations_module))
        report = validate_entities(validations, ignore_tables, schema)
        for line in formatted_output(report, export):
            print(line, file=out)
    except RuntimeError as error:
        print(str(error), file=err)
