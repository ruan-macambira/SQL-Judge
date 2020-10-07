""" Run the application """
from typing import Callable, Dict, List, Iterable
from itertools import product
from .schema import Schema, Entity
from .validation_entity import needs_validation, canonical_name
from .util import group_by

def validate_entities(validations: Dict[str, List[Callable]], ignore_tables: List[str], schema: Schema):
    """ Run the schema validation and return a report """
    report: dict = {}
    for group, entities in schema.entities().items():
        vals = validations.get(group, [])
        combinations = ((entity, _guard_validation(validation, entity)) for entity, validation in product(entities, vals) if needs_validation(entity, ignore_tables))
        result = ((entity.__name__, canonical_name(entity), message) for entity, message in combinations if message is not None)
        report[group] = group_by(result, lambda x: x[1], lambda x: x[2])

    return report

def _guard_validation(validation: Callable, entity: Entity):
    try:
        return validation(entity)
    except Exception as err: # pylint: disable=broad-except
        return f'validation "{validation.__name__}" raised a {type(err).__name__} with the message "{err}"'
