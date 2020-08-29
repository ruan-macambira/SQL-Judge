# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
from validate_schema.adapter import DBAdapter

class Adapter(DBAdapter):
    def tables(self):
        return []

    def columns(self, _table_name):
        return []

    def primary_key(self, _table_name, _column_name):
        return []

    def references(self, _table_name, _column_name):
        return []

    def constraints(self, _table_name, _column_name):
        return []

    def index(self, _table_name, _column_name):
        return []

    def triggers(self, _table_name):
        return []

    def functions(self):
        return []

    def procedures(self):
        return []
