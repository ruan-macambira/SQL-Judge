""" A Mock for a Database Adapter, used to run tests """
from .adapter import DBAdapter

class MockAdapter(DBAdapter):
    """ Mock classes to generate the return values of a connection object """
    def __init__(self, tables_info, functions_info=None, procedures_info=None, sequences_info=None):
        self.tables_info = tables_info or {}
        self.functions_info = functions_info or []
        self.procedures_info = procedures_info or []
        self.sequences_info = sequences_info or []

    def tables(self):
        return list(self.tables_info.keys())

    def columns(self):
        table_columns = ((table, props['columns']) for table, props in self.tables_info.items())
        result = []
        for table, columns in table_columns:
            for cname, ctype in columns.items():
                result.append((table, cname, ctype))
        return result

    def primary_keys(self):
        first_or_none = lambda lst: lst[0] if len(lst) > 0 else None
        return [
            (table, first_or_none(props.get('primary_key', [])))
            for table, props in self.tables_info.items()
            if first_or_none(props.get('primary_key', [])) is not None
        ]

    def _table_entities(self, entity_name):
        table_entities = ((table, props.get(entity_name, {}))
                          for table, props in self.tables_info.items())
        result = []
        for table, entities in table_entities:
            for column, entity in entities.items():
                result.append((table, column, entity))
        return result

    def references(self):
        return self._table_entities('references')

    def indexes(self):
        return self._table_entities('indexes')

    def constraints(self):
        table_constraints = ((table, props.get('constraints', {}))
                             for table, props in self.tables_info.items())
        result = []
        for table, constraints in table_constraints:
            for column, constraint in constraints.items():
                cname, ctype = list(constraint.items())[0]
                result.append((table, column, cname, ctype))
        return result

    def triggers(self):
        return self._table_entities('triggers')

    def functions(self):
        return self.functions_info

    def procedures(self):
        return self.procedures_info

    def sequences(self):
        return self.sequences_info
