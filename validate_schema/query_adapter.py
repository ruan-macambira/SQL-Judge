from typing import List, Dict, Optional
from .adapter import DBAdapter

class QueryAdapter:
    def __init__(self, adapter):
        self._adapter: DBAdapter = adapter

    def tables(self) -> List[str]:
        return self._adapter.tables()

    def columns(self, table_name: str) -> Dict[str, str]:
        return {
            column:ctype for (table, column, ctype)
            in self._adapter.columns()
            if table == table_name
        }

    def triggers(self, table_name: str) -> Dict[str, str]:
        return {
            trigger:hook for (table, trigger, hook)
            in self._adapter.triggers()
            if table == table_name
        }

    def primary_key(self, table_name: str, column_name: str) -> bool:
        return (table_name, column_name) in self._adapter.primary_keys()

    def references(self, table_name: str, column_name: str) -> Optional[str]:
        return {
            (table, column): references for (table, column, references)
            in self._adapter.references()
        }.get((table_name, column_name))

    def index(self, table_name: str, column_name: str) -> Optional[str]:
        for table, column, index in self._adapter.indexes():
            if table == table_name and column == column_name:
                return index
        return None

    def constraints(self, table_name: str, column_name: str) -> Dict[str, str]:
        return {
            constraint:ctype for (table, column, constraint, ctype)
            in self._adapter.constraints()
            if table == table_name and column == column_name
        }

    def functions(self) -> List[str]:
        return self._adapter.functions()

    def procedures(self) -> List[str]:
        return self._adapter.procedures()

    def sequences(self) -> List[str]:
        return self._adapter.sequences()
