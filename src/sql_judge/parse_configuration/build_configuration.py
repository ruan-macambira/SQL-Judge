""" Sets ConfigurationBuilder, a class responsible to merge configuration
options from various sources, merge them, and build a valid Configuration
Object to use in the rest of the proccess """
import importlib
import json
from dataclasses import dataclass, field
from typing import List, Optional
from .. import Configuration
from . import schema_validations, adapter_builder


@dataclass
class ConfigurationBuilder:
    """Group, Validate and Build the Configurations parameters"""
    adapter: adapter_builder.AdapterBuilder = field(default_factory=adapter_builder.default_adapter)
    validations_module: Optional[str] = None
    ignore_tables: List[str] = field(default_factory=list)
    export_format: Optional[str] = None
    export_output: Optional[str] = None
    _invalidation: Optional[str] = None

    @classmethod
    def from_json(cls, json_str):
        """Generates an instance based from a JSON string"""
        try:
            options = json.loads(json_str)
        except json.JSONDecodeError as jserr:
            raise RuntimeError('Error while parsing configuration') from jserr
        adapter_options = options.get('adapter', {})
        validation_options = options.get('validations', {})
        export_options = options.get('export', {})
        return cls(
            adapter = adapter_builder.from_json(adapter_options),
            ignore_tables=options.get('ignore_tables', []),
            validations_module=validation_options.get('module'),
            export_format=export_options.get('format')
        )

    def merge(self, builder: 'ConfigurationBuilder'):
        """ Combine two builders """
        return ConfigurationBuilder(
            adapter=self.adapter.merge(builder.adapter),
            validations_module=builder.validations_module or self.validations_module,
            ignore_tables=self.ignore_tables + builder.ignore_tables,
            export_format=builder.export_format or self.export_format
        )

    def is_valid(self):
        """Checks validity of Configuration Builder"""
        if not self.adapter.is_valid():
            self._invalidation = self.adapter.error()
            return False
        if self.validations_module is None:
            self._invalidation = 'Validations Module not provided'
            return False
        if self.export_format is None:
            self._invalidation = 'Export Format not provided'
            return False
        return True


    def _validations(self):
        validations_module = importlib.import_module(self.validations_module)
        validations = schema_validations.module_validations(validations_module)
        return schema_validations.to_configuration(validations)

    def build(self) -> Configuration:
        """Use the internal parameters to generate a Configuration Instance"""
        if not self.is_valid():
            raise RuntimeError(self._invalidation)
        return Configuration(
            connection=self.adapter.build(),
            validations=self._validations(),
            export=self.export_format, #type: ignore
            ignore_tables=self.ignore_tables
        )
