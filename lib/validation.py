""" Validations """
from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Union, Dict
from .schema import Table, Schema, Column, Entity
from .adapter import DBAdapter

@dataclass
class Configuration:
    """ Stores and configuration options for running the validations """
    connection: DBAdapter
    validations: Dict[str, List[Callable]] = field(default_factory=dict)
    ignore_tables: List[str] = field(default_factory=list)

def validate_entity(entity: Union[Table, Column], validations: List[Callable]) -> List[str]:
    """ Run a list of validations for an entity """
    raw_messages = [val(entity) for val in validations]
    return [message for message in raw_messages if message is not None]
