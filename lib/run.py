""" Run the application """
from typing import List, Dict, Callable
from lib.validation import batch_validate_entities, Configuration, entities_to_validate
from lib.generate_schema import generate_schema
from lib.report import generate_report

def run(config: Configuration) -> List[str]:
    """ Run the schema validation and return a report """
    schema = generate_schema(config.connection)
    report = {
        entity_group: _validate(
            entities_to_validate(entity_group, schema, config),
            config.validations[entity_group])
        for entity_group in schema.entity_groups
    }

    return generate_report(report)

def _validate(entities: list, validations: List[Callable]) -> Dict[str, List[str]]:
    """ run the validations for the entity group and return in a format
    compatible to the report generator

    return format: {'entity': ['message']}"""
    reports = {}
    vals = _group_validations(
        batch_validate_entities(entities, validations))
    for entity, messages in vals.items():
        reports[entity.canonical_name] = messages

    return reports

def _group_validations(validations: List[tuple]) -> dict:
    grouped: dict = {}

    for validation in validations:
        if validation[0] not in grouped:
            grouped[validation[0]] = []

        grouped[validation[0]].append(validation[1])

    return grouped
