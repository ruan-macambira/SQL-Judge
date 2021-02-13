"""Test Utils"""

from typing import Dict, List, Callable
from .parse_configuration.schema_validations import module_validations, to_configuration
from .validate import validate_entity
from .schema import Entity

class Validator:
    """Allows to validate a single entity against a validation module"""
    def __init__(self, validations: Dict[str, List[Callable]]):
        self.validations = to_configuration(module_validations(validations))

    def valid(self, entity: Entity):
        """Checks if entity is valid against the validations"""
        return len(self.validate(entity)) == 0

    def validate(self, entity: Entity):
        """Returns all invalidations of an entity. Returns an empty list if there is none"""
        return [v for v in validate_entity(self.validations, entity) if v is not None]
