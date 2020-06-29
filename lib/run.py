""" Run the application """
from typing import List, Dict, Callable
from lib.validation import batch_validate_entities, Configuration, \
    tables_to_validate, columns_to_validate
from lib.generate_schema import generate_schema
from lib.report import generate_report

def run(config: Configuration) -> List[str]:
    """ Run the schema validation and return a report """
    schema = generate_schema(config.connection)

    tables = tables_to_validate(schema, config)
    columns = columns_to_validate(schema, config)

    table_reports = _validate(tables, config.validations['table'],
                              lambda table: table.name)
    column_reports = _validate(columns, config.validations['column'],
                               lambda column: f'{column.table.name}.{column.name}')

    report = {'Tables': table_reports, 'Columns': column_reports}
    return generate_report(report)

def _validate(entities: list, validations: List[Callable],
              entity_id: Callable) -> Dict[str, List[str]]:
    """ run the validations for the entity group and return in a format
    compatible to the report generator

    return format: {'entity': ['message']}"""
    reports = {}
    vals = _group_validations(
        batch_validate_entities(entities, validations))
    for entity, messages in vals.items():
        reports[entity_id(entity)] = messages

    return reports

def _group_validations(validations: List[tuple]) -> dict:
    grouped: dict = {}

    for validation in validations:
        if validation[0] not in grouped:
            grouped[validation[0]] = []

        grouped[validation[0]].append(validation[1])

    return grouped
