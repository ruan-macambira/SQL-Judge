from typing import TextIO, MutableMapping
import toml
_LOCALE: MutableMapping = {}

def load_toml(ftoml: TextIO):
    load_labels(toml.load(ftoml))

def load_labels(labels: MutableMapping):
    global _LOCALE #pylint: disable = global-statement
    _LOCALE = labels

def translate(label, scope = None):
    try:
        levels = label.split('.')
        if scope is not None:
            levels = scope.split('.') + levels
        value =  _LOCALE
        for level in levels:
            value = value[level]
        return value
    except KeyError as err:
        raise RuntimeError('Missing label from locale') from err

t = translate
