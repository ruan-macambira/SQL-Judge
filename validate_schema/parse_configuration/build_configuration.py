""" Sets ConfigurationBuilder, a class responsible to merge configuration
options from various sources, merge them, and build a valid Configuration
Object to use in the rest of the proccess """
import importlib
import json
from dataclasses import dataclass, field
from typing import List, Optional
from .. import Configuration
from . import schema_validations

@dataclass
class ConfigurationBuilder:
    """Group, Validate and Build the Configurations parameters"""
    adapter_module: Optional[str] = None
    adapter_class: Optional[str] = None
    validations_module: Optional[str] = None
    ignore_tables: List[str] = field(default_factory=list)
    export_format: Optional[str] = None
    export_output: Optional[str] = None

    @classmethod
    def from_json(cls, json_str):
        """Generates an instance based from a JSON string"""
        options = json.loads(json_str)
        adapter_options = options.get('adapter', {})
        validation_options = options.get('validations', {})
        export_options = options.get('export', {})
        return cls(
            adapter_module=adapter_options.get('module'),
            adapter_class=adapter_options.get('class'),
            ignore_tables=options.get('ignore_tables', []),
            validations_module=validation_options.get('module'),
            export_format=export_options.get('format')
        )

    def merge(self, builder: 'ConfigurationBuilder'):
        """ Combine two builders """
        return ConfigurationBuilder(
            adapter_module=builder.adapter_module or self.adapter_module,
            adapter_class=builder.adapter_class or self.adapter_class,
            validations_module=builder.validations_module or self.validations_module,
            ignore_tables=self.ignore_tables + builder.ignore_tables,
            export_format=builder.export_format or self.export_format
        )

    def is_valid(self):
        """Checks validity of Configuration Builder"""
        if self.adapter_module is None:
            return False
        if self.adapter_class is None:
            return False
        if self.validations_module is None:
            return False
        if self.export_format is None:
            return False
        return True

    def _adapter(self):
        adapter_module = importlib.import_module(self.adapter_module)
        return getattr(adapter_module, self.adapter_class)()

    def _validations(self):
        validations_module = importlib.import_module(self.validations_module)
        validations = schema_validations.module_validations(validations_module)
        return schema_validations.to_configuration(validations)

    def build(self) -> Configuration:
        """Use the internal parameters to generate a Configuration Instance"""
        if not self.is_valid():
            raise ValueError
        return Configuration(
            connection=self._adapter(),
            validations=self._validations(),
            export=self.export_format, #type: ignore
            ignore_tables=self.ignore_tables
        )
