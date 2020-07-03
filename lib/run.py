""" Run the application """
from typing import List, Dict, Callable
from lib.validation import Configuration, validate_entity
from lib.generate_schema import generate_schema
from lib.meta_schema import MetaSchema
from lib.report import generate_report

def run(config: Configuration) -> List[str]:
    """ Run the schema validation and return a report """
    schema = generate_schema(config.connection)
    meta_schema = MetaSchema(schema)
    report = {}
    for group, entities in meta_schema.entities().items():
        report[group] = _validate(
            [entity for entity in entities if entity.needs_validation(config)],
            config.validations[group])

    return generate_report(report)

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
