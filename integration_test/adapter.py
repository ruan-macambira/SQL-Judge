# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
from sql_judge.adapter import AbstractAdapter

class Adapter(AbstractAdapter):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def tables(self):
        return []

    def columns(self):
        return []

    def primary_keys(self):
        return []

    def references(self):
        return []

    def constraints(self):
        return []

    def indexes(self):
        return []

    def triggers(self):
        return []

    def functions(self):
        return []

    def procedures(self):
        return []

    def sequences(self):
        return []

    def __eq__(self, other):
        return self.__class__ == other.__class__
