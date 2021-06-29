""" Run the application """
from typing import Callable, Dict, Collection
from collections import namedtuple
from .schema import Schema, Entity
from .validation_entity import canonical_name

Fail = namedtuple('Fail', ['group', 'report_name', 'message'])

def entities_validation(validations: Dict[str, Collection[Callable]], _needs_validation: Callable, schema: Schema):
    report: list = []
    for entity in schema.entities():
        if not _needs_validation(entity):
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
        error = type(err).__name__
        return f'validation "{validation.__name__}" raised a {error} with the message "{err}"'
