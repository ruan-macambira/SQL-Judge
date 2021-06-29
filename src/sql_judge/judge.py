from typing import Collection, Callable, Dict, IO
from dataclasses import dataclass, InitVar, field
from sys import stdout, stderr
from .adapter import AbstractAdapter
from .validate import entities_validation
from .export import formatted_output
from .schema import Schema
from .schema_validations import module_validations, to_configuration
from .validation_entity import needs_validation

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
    validations = to_configuration(module_validations(validations_module))
    exporter = lambda report: formatted_output(report, export)
    _needs_validation = lambda entity: needs_validation(entity, ignore_tables)
    return Judge(
        adapter=adapter, validations=validations,
        needs_validation=_needs_validation, exporter=exporter,
        out=out, err=err
    ).judge()

@dataclass
class Judge:
    adapter: InitVar[AbstractAdapter]
    schema: Schema = field(init=False)
    validations: Dict[str, Collection]
    needs_validation: Callable = lambda: None
    exporter: Callable = lambda: None
    out: IO = stdout
    err: IO = stderr

    def __post_init__(self, adapter):
        self._isvalid(adapter)
        self.schema = Schema(adapter)

    def _isvalid(self, adapter):
        if not isinstance(adapter, AbstractAdapter):
            raise RuntimeError("Adapter must inherit AbstractAdapter")

    def judge(self):
        try:
            report = entities_validation(self.validations, self.needs_validation, self.schema)
            for line in self.exporter(report):
                print(line, file=self.out)
        except RuntimeError as error:
            print(str(error), file=self.err)
