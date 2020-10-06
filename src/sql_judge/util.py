""" Helper functions that does not fit in a specific module of the project """
import functools

def cached_property(method):
    """Decorator meant to mimic Python 3.8's cached_property"""
    return property(functools.lru_cache()(method))

def find(collection, condition):
    """Return the first element in collection that satisfies condition"""
    return next((element for element in collection if condition(element)), None)
