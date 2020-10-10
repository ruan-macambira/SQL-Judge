""" Sets ConfigurationBuilder, a class responsible to merge configuration
options from various sources, merge them, and build a valid Configuration
Object to use in the rest of the proccess """
import importlib
import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .. import Configuration
from . import schema_validations

@dataclass
class ConfigurationBuilder:
    """Group, Validate and Build the Configurations parameters"""
    adapter_module: Optional[str] = None
    adapter_class: Optional[str] = None
    adapter_params: List[str] = field(default_factory=list)
    adapter_named_params: Dict[str, str] = field(default_factory=dict)
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
            adapter_module=adapter_options.get('module'),
            adapter_class=adapter_options.get('class'),
            adapter_params=adapter_options.get('params', []),
            adapter_named_params=adapter_options.get('named_params', {}),
            ignore_tables=options.get('ignore_tables', []),
            validations_module=validation_options.get('module'),
            export_format=export_options.get('format')
        )

    def merge(self, builder: 'ConfigurationBuilder'):
        """ Combine two builders """
        return ConfigurationBuilder(
            adapter_module=builder.adapter_module or self.adapter_module,
            adapter_class=builder.adapter_class or self.adapter_class,
            adapter_params= builder.adapter_params or self.adapter_params,
            adapter_named_params={**self.adapter_named_params, **builder.adapter_named_params},
            validations_module=builder.validations_module or self.validations_module,
            ignore_tables=self.ignore_tables + builder.ignore_tables,
            export_format=builder.export_format or self.export_format
        )

    def is_valid(self):
        """Checks validity of Configuration Builder"""
        if self.adapter_module is None:
            self._invalidation = 'Adapter Module not provided'
            return False
        if self.adapter_class is None:
            self._invalidation = 'Adapter Class not provided'
            return False
        if self.validations_module is None:
            self._invalidation = 'Validations Module not provided'
            return False
        if self.export_format is None:
            self._invalidation = 'Export Format not provided'
            return False
        return True

    def _adapter(self):
        adapter_module = importlib.import_module(self.adapter_module)
        return getattr(adapter_module, self.adapter_class)(*self.adapter_params, **self.adapter_named_params)

    def _validations(self):
        validations_module = importlib.import_module(self.validations_module)
        validations = schema_validations.module_validations(validations_module)
        return schema_validations.to_configuration(validations)

    def build(self) -> Configuration:
        """Use the internal parameters to generate a Configuration Instance"""
        if not self.is_valid():
            raise RuntimeError(self._invalidation)
        return Configuration(
            connection=self._adapter(),
            validations=self._validations(),
            export=self.export_format, #type: ignore
            ignore_tables=self.ignore_tables
        )
