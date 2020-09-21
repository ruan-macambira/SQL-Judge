"""Validates the Schema"""
from dataclasses import dataclass, field
from typing import Callable, List, Dict
from .adapter import AbstractAdapter

def validates(entity):
    """ Sets Entity to which the validation will run """
    def _validates(validation):
        validation.validates = entity
        return validation
    return _validates

@dataclass
class Configuration:
    """ Stores and configuration options for running the validations """
    connection: AbstractAdapter
    validations: Dict[str, List[Callable]] = field(default_factory=dict)
    ignore_tables: List[str] = field(default_factory=list)
    export: str = 'CLI'
