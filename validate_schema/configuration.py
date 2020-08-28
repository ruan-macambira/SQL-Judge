""" Validations """
from dataclasses import dataclass, field
from typing import Callable, List, Dict
from .adapter import DBAdapter

@dataclass
class Configuration:
    """ Stores and configuration options for running the validations """
    connection: DBAdapter
    validations: Dict[str, List[Callable]] = field(default_factory=dict)
    ignore_tables: List[str] = field(default_factory=list)
    export: str = 'CLI'
