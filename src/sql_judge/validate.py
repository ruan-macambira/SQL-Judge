""" Run the application """
from typing import Callable, Dict, Collection
from collections import namedtuple
from .schema import Schema, Entity
from .validation_entity import needs_validation, canonical_name

Fail = namedtuple('Fail', ['group', 'report_name', 'message'])

def validate_entities(validations: Dict[str, Collection[Callable]], ignore_tables: Collection[str], schema: Schema):
    """ Run the schema validation and return a report """
    report: list = []
    for entity in schema.entities():
        if not needs_validation(entity, ignore_tables):
            continue
        group = entity.__name__.lower()
        messages = validate_entity(validations, entity)
        report += [Fail(group, canonical_name(entity), message)
                   for message in messages if message is not None]

    return report

def validate_entity(validations: Dict[str, Collection[Callable]], entity: Entity):
    """Validate Entity"""
    group = entity.__name__.lower()
    return (_guard_validation(validation, entity)
            for validation in validations.get(group, []))

def _guard_validation(validation: Callable, entity: Entity):
    try:
        return validation(entity)
    except Exception as err: # pylint: disable=broad-except
        return f'validation "{validation.__name__}" raised a {type(err).__name__} with the message "{err}"'
