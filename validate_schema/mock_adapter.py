""" A Mock for a Database Adapter, used to run tests """
import functools
from .adapter import DBAdapter

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
    def __init__(self, tables_info, functions_info=None, procedures_info=None, sequences_info=None):
        self.tables_info = tables_info
        self.functions_info = functions_info or []
        self.procedures_info = procedures_info or []
        self.sequences_info = sequences_info or []

    def tables(self):
        return list(self.tables_info.keys())

    def columns(self, table_name):
        return self.tables_info[table_name]['columns']

    @_none_if_key_error
    def primary_key(self, table_name, column_name):
        return column_name in self.tables_info[table_name]['primary_key']

    @_none_if_key_error
    def references(self, table_name, column_name):
        return self.tables_info[table_name]['references'][column_name]

    @_none_if_key_error
    def index(self, table_name, column_name):
        return self.tables_info[table_name]['indexes'][column_name]

    @_empty_dict_if_key_error
    def constraints(self, table_name, column_name):
        return self.tables_info[table_name]['constraints'][column_name]

    @_empty_dict_if_key_error
    def triggers(self, table_name):
        return self.tables_info[table_name]['triggers']

    def functions(self):
        return self.functions_info

    def procedures(self):
        return self.procedures_info

    def sequences(self):
        return self.sequences_info
