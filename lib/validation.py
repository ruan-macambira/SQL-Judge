""" Validations """
from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Union, Dict
from .schema import Table, Schema, Column, SchemaEntity
from .adapter import DBAdapter

@dataclass
class Configuration:
    """ Stores and configuration options for running the validations """
    connection: DBAdapter
    validations: Dict[str, List[Callable]] = field(default_factory=dict)
    ignore_tables: List[str] = field(default_factory=list)

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

def not_ignored(entity_group: str, entity: SchemaEntity, config: Configuration) -> bool:
    """ Checks if the entity should not be ignored """
    rules = {
        'Tables': lambda table: table.name not in config.ignore_tables,
        'Columns': lambda column: column.table.name not in config.ignore_tables
    }

    return rules[entity_group](entity)

def entities_to_validate(
        entity_group: str, schema: Schema, config: Configuration) -> List[SchemaEntity]:
    """ Filter in the entities of a certain group that are meant to run the validations """
    if schema is None or config is None:
        raise TypeError
    return [
        entity for entity in schema.entities[entity_group]
        if not_ignored(entity_group, entity, config)
    ]
