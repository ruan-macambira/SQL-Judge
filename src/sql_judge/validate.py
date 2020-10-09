""" Run the application """
from typing import Callable, Dict, List
from collections import namedtuple
from .schema import Schema, Entity
from .validation_entity import needs_validation, canonical_name

Fail = namedtuple('Fail', ['group', 'report_name', 'message'])

def _titleize(group: str):
    if group[-1] == 's':
        return group
    if group.lower() == 'index':
        return 'Indexes'
    return group.capitalize() + 's'

def validate_entities(validations: Dict[str, List[Callable]], ignore_tables: List[str], schema: Schema):
    """ Run the schema validation and return a report """
    report: list = []
    for entity in schema.entities():
        if not needs_validation(entity, ignore_tables):
            continue
        group = _titleize(entity.__name__)
        vals = validations.get(_titleize(group), [])
        messages = (_guard_validation(validation, entity) for validation in vals)
        report += [Fail(group=group, report_name=canonical_name(entity), message=message) for message in messages if message is not None]

    return report

def _guard_validation(validation: Callable, entity: Entity):
    try:
        return validation(entity)
    except Exception as err: # pylint: disable=broad-except
        return f'validation "{validation.__name__}" raised a {type(err).__name__} with the message "{err}"'
