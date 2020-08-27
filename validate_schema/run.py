""" Run the application """
import functools
from typing import List, Dict, Callable
from .schema import Entity
from .configuration import Configuration
from .generate_schema import generate_schema
from .meta_schema import schema_entities
from . import export

def validates(entity):
    """ Sets Entity to which the validation will run """
    def _validates(validation):
        validation.validates = entity
        return validation
    return _validates

def run(config: Configuration) -> List[str]:
    """ Run the schema validation and return a report """
    schema = generate_schema(config.connection)
    report = {}
    for group, entities in schema_entities(schema).items():
        report[group] = _validate(
            [entity for entity in entities if entity.needs_validation(config)],
            config.validations[group])

    return _generate_report(config, report)

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
    raw_messages = [val(entity) for val in validations]
    return [message for message in raw_messages if message is not None]


def _generate_report(config: Configuration, report_hash: dict) -> List[str]:
    return {
        'CLI': export.export_cli,
        'CSV': export.export_csv
    }[config.export](report_hash)
