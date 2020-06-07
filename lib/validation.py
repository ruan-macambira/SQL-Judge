from typing import Callable, List, Tuple
from .schema import Table, Schema, Column

def run_table_validations(table: Table, validations: List[Callable]) -> List[str]:
    """ Run a set of validations through a table and return its errors in a list """
    if table is None:
        raise TypeError
    if len(validations) == 0:
        raise ValueError

    raw_messages = [val(table) for val in validations]
    return [message for message in raw_messages if message is not None]

def run_tableset_validation(tableset: List[Table], validations: List[Callable]) -> List[Tuple[Table, str]]:
    """ Run a set of validations through a set of tables, and returns the validations errors, attached to the invalid object"""
    val_res: List[Tuple[Table, str]] = []

    for table in tableset:
        val_res += [(table, message) for message in run_table_validations(table, validations)]

    return val_res

def run_column_validations(column: Column, validations: List[Callable]) -> List[str]:
    if column is None:
        raise TypeError
    if len(validations) == 0:
        raise ValueError

    raw_messages = [val(column) for val in validations]
    return [message for message in raw_messages if message is not None]

def run_columnset_validations(columnset: List[Column], validations: List[Callable]) -> List[Tuple[Column, str]]:
    val_res: List[Tuple[Column, str]] = []

    for column in columnset:
        val_res += [(column, message) for message in run_column_validations(column, validations)]

    return val_res

class ValidationConfig:
    """ Stores and configuration options for running the validations """
    def __init__(self, ignore_tables: List[str] = None):
        self.ignore_tables: List[str] = [] if ignore_tables is None else ignore_tables

def tables_to_validate(schema: Schema, config: ValidationConfig):
    if schema is None or config is None:
        raise TypeError
    return [table for table in schema.tables if table.name not in config.ignore_tables]
