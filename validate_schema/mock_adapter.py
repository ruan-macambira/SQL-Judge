""" A Mock for a Database Adapter, used to run tests """
from .adapter import DBAdapter

class MockAdapter(DBAdapter):
    """ Mock classes to generate the return values of a connection object """
    def __init__(self, tables_info=None, functions_info=None, procedures_info=None):
        self.tables_info = tables_info or {}
        self.functions_info = functions_info or []
        self.procedures_info = procedures_info or []

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

    def references(self):
        table_references = ((table, props.get('references', {})) for table, props in self.tables_info.items())
        result = []
        for table, references in table_references:
            for column, referenced_table in references.items():
                result.append((table, column, referenced_table))
        return result

    def indexes(self):
        table_indexes = ((table, props.get('indexes', {})) for table, props in self.tables_info.items())
        result = []
        for table, indexes in table_indexes:
            for column, index in indexes.items():
                result.append((table, column, index))
        return result

    def constraints(self):
        table_constraints = ((table, props.get('constraints', {})) for table, props in self.tables_info.items())
        result = []
        for table, constraints in table_constraints:
            for column, constraint in constraints.items():
                cname, ctype = list(constraint.items())[0]
                result.append((table, column, cname, ctype))
        return result

    def triggers(self):
        table_triggers = ((table, props.get('triggers', {})) for table, props in self.tables_info.items())
        result = []
        for table, triggers in table_triggers:
            for trigger, hook in triggers.items():
                result.append((table, trigger, hook))
        return result

    def functions(self):
        return self.functions_info

    def procedures(self):
        return self.procedures_info
