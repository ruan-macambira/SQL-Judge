""" Run the application """
from typing import Callable, Dict, List

from . import Configuration
from .meta_schema import schema_entities
from .schema import Entity, Schema

def validate_entities(config: Configuration, schema: Schema) -> dict:
    """ Run the schema validation and return a report """
    report = {}
    for group, entities in schema_entities(schema).items():
        report[group] = _validate(
            [entity for entity in entities if entity.needs_validation(config)],
            config.validations[group])

    return report

def _validate(entities: list, validations: List[Callable]) -> Dict[str, List[str]]:
    """ run the validations for the entity group and return in a format
    compatible to the report generator

    return format: {'entity': ['message']}"""
    reports = {}
    for entity in entities:
        messages = validate_entity(entity.entity, validations)
        if messages != []:
            reports[entity.canonical_name()] = messages

    return reports

def validate_entity(entity: Entity, validations: List[Callable]) -> List[str]:
    """ Run a list of validations for an entity """
    raw_messages = (_guard_validation(val,entity) for val in validations)
    return [message for message in raw_messages if message is not None]

def _guard_validation(validation: Callable, entity: Entity):
    try:
        return validation(entity)
    except Exception as err: # pylint: disable=broad-except
        return f'validation "{validation.__name__}" raised a {type(err).__name__} with the message "{err}"'
