"""Confinguration Builder for Adapter Options"""
from abc import ABC, abstractmethod
from typing import List, Dict
import importlib
import pkg_resources

class AdapterBuilder(ABC):
    """Abstract Class for retrieving the adapter used to fetch DB schema data"""
    params: List[str]
    named_params: Dict[str, str]

    def __init__(self, params = None, named_params = None):
        self._invalidation = None
        self.params = params or []
        self.named_params = named_params or {}

    @classmethod
    @abstractmethod
    def elligible(cls, config) -> bool:
        """Checks whether the config matches with the type"""

    @abstractmethod
    def asdict(self) -> dict:
        """Convert Params to a Dict"""

    def merge(self, other) -> 'AdapterBuilder':
        """Merge two Adapter Options"""
        keys = {*self.asdict(), *other.asdict()}
        ret = {}
        for key in keys:
            if key == 'named_params':
                continue
            ret[key] = other.asdict().get(key) or self.asdict().get(key)
        ret['named_params'] = {**self.named_params, **other.named_params}
        return from_json(ret)   

    @abstractmethod
    def build(self):
        """Build Configuration Adapter Param"""

    @abstractmethod
    def is_valid(self) -> bool:
        """Checks validity"""

    def __eq__(self, other):
        return self.asdict() == other.asdict()

    def error(self) -> str:
        """Invalid builder message"""
        return self._invalidation

class UnresolvedAdapterBuilder(AdapterBuilder):
    """Similar to a Null Object, it is instantiaded in a 'from_json' call whenever
    it cannot resolve to an appended or pluggable type."""
    def __init__(self, params = None, named_params = None, **_unresolved):
        super().__init__(params, named_params)

    @classmethod
    def elligible(cls, _config):
        return True

    def is_valid(self):
        self._invalidation = 'Builder could not resolve Adapter Type'
        return False

    def asdict(self):
        return {'params': self.params, 'named_params': self.named_params}

    def build(self):
        raise RuntimeError('Cannot Build an Unresolved Adapter Builder')

class AppendedAdapterBuilder(AdapterBuilder):
    """Adapter Builder for modules used in Python discovery"""
    def __init__(self, module, klass, params = None, named_params = None):
        super().__init__(params, named_params)
        self.module = module
        self.klass = klass

    @classmethod
    def elligible(cls, config):
        return 'module' in config and 'klass' in config

    def is_valid(self):
        if self.module is None:
            self._invalidation = 'Adapter Module not provided'
            return False
        if self.klass is None:
            self._invalidation = 'Adapter Class not provided'
            return False
        return True

    def asdict(self):
        return {
            'module': self.module,
            'klass': self.klass,
            'params': self.params,
            'named_params': self.named_params
        }

    def build(self):
        adapter_module = importlib.import_module(self.module)
        return getattr(adapter_module, self.klass)(*self.params, **self.named_params)

class PluggableAdapterBuilder(AdapterBuilder):
    """Adapter Builder for modules that are plugins"""
    def __init__(self, plugin, params = None, named_params = None):
        super().__init__(params, named_params)
        self.plugin = plugin

    @classmethod
    def elligible(cls, config):
        return 'plugin' in config

    def is_valid(self):
        if self.plugin is None:
            return False
        return True

    def asdict(self):
        return {
            'plugin': self.plugin,
            'params': self.params,
            'named_params': self.named_params
        }

    def build(self):
        iter_adapter_plugins = pkg_resources.iter_entry_points('sql_judge.adapter')
        try:
            plugin_module = next(p for p in iter_adapter_plugins if p.name == self.plugin).load()
            return getattr(plugin_module, 'Adapter')(*self.params, **self.named_params)
        except StopIteration as stopit:
            raise RuntimeError(f"Could not find plugin with '{self.plugin}' ID") from stopit

def from_json(options):
    """AdapterBuilder factory made out of a dict.
    The Type of Adapter depends on the keys the config holds"""
    if 'class' in options:
        options['klass'] = options['class']
        del options['class']
    for builder in (AppendedAdapterBuilder,PluggableAdapterBuilder):
        if builder.elligible(options):
            return builder(**options)
    return UnresolvedAdapterBuilder(**options)

def default_adapter():
    """Default Adapter Configuration. Alias for an adapter that has no properties"""
    return from_json({})
