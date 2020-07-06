""" Run the application """
from typing import List, Dict, Callable
from lib.validation import Configuration, validate_entity
from lib.generate_schema import generate_schema
from lib.meta_schema import schema_entities
from lib import export

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

def _generate_report(config: Configuration, report_hash: dict) -> List[str]:
    return {
        'CLI': export.export_cli,
        'CSV': export.export_csv
    }[config.export](report_hash)
