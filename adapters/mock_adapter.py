""" A Mock for a Database Adapter, used to run tests """
import functools
from lib.adapter import DBAdapter

def _none_if_key_error(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except KeyError:
            return None

    return wrapper

def _empty_dict_if_key_error(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return {}
    return wrapper

class MockAdapter(DBAdapter):
    """ Mock classes to generate the return values of a connection object """
    def __init__(self, mock_values):
        self.mock_values = mock_values

    def tables(self):
        return list(self.mock_values.keys())

    def columns(self, table_name):
        return self.mock_values[table_name]['columns']

    @_none_if_key_error
    def primary_key(self, table_name, column_name):
        return column_name in self.mock_values[table_name]['primary_key']

    @_none_if_key_error
    def references(self, table_name, column_name):
        return self.mock_values[table_name]['references'][column_name]

    @_none_if_key_error
    def index(self, table_name, column_name):
        return self.mock_values[table_name]['indexes'][column_name]

    @_empty_dict_if_key_error
    def constraints(self, table_name, column_name):
        return self.mock_values[table_name]['constraints'][column_name]

    @_empty_dict_if_key_error
    def triggers(self, table_name):
        return self.mock_values[table_name]['triggers']
