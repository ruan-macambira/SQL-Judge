from abc import ABC, abstractmethod
from typing import List, Dict
import importlib
import pkg_resources

class AbstractAdapterBuilder(ABC):
    params: List[str]
    named_params: Dict[str, str]

    def __init__(self, params = None, named_params = None):
        self._invalidation = None
        self.params = params or []
        self.named_params = named_params or {}

    @classmethod
    @abstractmethod
    def elligible(cls, config):
        """Checks whether the config matches with the type"""

    @abstractmethod
    def asdict(self):
        """Convert Params to a Dict"""

    def merge(self, other):
        """Merge two Adapter Options"""
        keys = {*self.asdict(), *other.asdict()}
        ret = {}
        for key in keys:
            ret[key] = other.asdict().get(key) or self.asdict().get(key)
        return from_json(ret)

    @abstractmethod
    def build(self):
        """Build Configuration Adapter Param"""

    @abstractmethod
    def is_valid(self):
        """Checks validity"""

    def __eq__(self, other):
        return self.asdict() == other.asdict()

    def error(self):
        return self._invalidation

class UnresolvedAdapterBuilder(AbstractAdapterBuilder):
    def __init__(self, params = None, named_params = None, **_unresolved):
        super().__init__(params, named_params)

    @classmethod
    def elligible(cls, _config):
        return True

    def is_valid(self):
        self._invalidation = 'Builder could not resolve Adapter Type'
        return False

    def asdict(self):
        return {}

    def build(self):
        raise RuntimeError('Cannot Build an Unresolved Adapter Builder')

class AppendedAdapterBuilder(AbstractAdapterBuilder):
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

class PluggableAdapterBuilder(AbstractAdapterBuilder):
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
    if 'class' in options:
        options['klass'] = options['class']
        del options['class']
    for builder in (AppendedAdapterBuilder,PluggableAdapterBuilder):
        if builder.elligible(options):
            return builder(**options)
    return UnresolvedAdapterBuilder(**options)

def default_adapter():
    return from_json({})
