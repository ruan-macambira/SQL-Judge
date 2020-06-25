""" Validations """
from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Union
from .schema import Table, Schema, Column
from .adapter import DBAdapter

def validate_entity(entity: Union[Table, Column], validations: List[Callable]) -> List[str]:
    """ Run a list of validations for an entity """
    if entity is None:
        raise TypeError
    if len(validations) == 0:
        raise ValueError

    raw_messages = [val(entity) for val in validations]
    return [message for message in raw_messages if message is not None]

def batch_validate_entities(entities: List, validations: List[Callable]) -> List:
    """ Run a list of validations for a list of entities """
    val_res: List[Tuple] = []

    for entity in entities:
        val_res += [(entity, message) for message in validate_entity(entity, validations)]

    return val_res

@dataclass
class ValidationConfig:
    """ Stores and configuration options for running the validations """
    connection: DBAdapter
    table_validations: List[Callable] = field(default_factory=List)
    column_validations: List[Callable] = field(default_factory=List)
    ignore_tables: List[str] = field(default_factory=List)

def tables_to_validate(schema: Schema, config: ValidationConfig):
    """ Filter Entity Tables to ignore the ones specified in configuration """
    if schema is None or config is None:
        raise TypeError
    return [table for table in schema.tables if table.name not in config.ignore_tables]

def columns_to_validate(schema: Schema, config: ValidationConfig):
    """ Filter Entity Columns to ignore those that are from the tables to ignore """
    if schema is None or config is None:
        raise TypeError
    return [column for column in schema.columns
            if column.table is not None and column.table.name not in config.ignore_tables]
