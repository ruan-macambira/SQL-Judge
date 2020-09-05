# Adapted from http://code.activestate.com/recipes/576527-freeze-make-any-object-immutable/
# pylint: disable=C
import inspect
from types import MethodWrapperType

immutable_types = set((int, str))

class Frozen():
    def __init__(self, value):
        self._value = value

    def __getattribute__(self, item):
        if item == '_value': return super().__getattribute__(item)
        value = getattr(self._value, item)

        if value.__class__ in immutable_types \
            or inspect.isbuiltin(value) \
            or type(value) == MethodWrapperType:
            return value
        return freeze(value)
  
    def __setattr__(self, name, value):
        if name == '_value': super().__setattr__(name, value)
        else: raise Exception("Can't modify frozen object {0}".format(self._value))
    
def freeze(value):
    return Frozen(value)
