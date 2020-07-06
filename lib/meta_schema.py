""" Schema Decorators to use in validations """
from dataclasses import dataclass
from typing import Callable
from .schema import Schema, Entity, TableEntity, ColumnEntity
from .configuration import Configuration

def schema_entities(schema: Schema):
    """ the entities in the schema serialized to run the validations """
    return {
        'Tables': _list_entities(schema.tables, _report_self, _validate_self),
        'Functions': _list_entities(schema.functions, _report_self, _validate_self),
        'Procedures': _list_entities(schema.procedures, _report_self, _validate_self),
        'Columns': _list_entities(schema.columns, _report_table, _validate_table),
        'Triggers': _list_entities(schema.triggers, _report_table, _validate_table),
        'Indexes': _list_entities(schema.indexes, _report_column, _validate_column),
        'Constraints': _list_entities(schema.constraints, _report_column, _validate_column),
    }

@dataclass
class MetaEntity:
    """Entity decorator to give it properties used in validation"""
    entity: Entity
    report: Callable
    validate: Callable

    def canonical_name(self):
        """ Name used in report """
        return self.report(self.entity)

    def needs_validation(self, config: Configuration):
        """ Condition met to be validated """
        return self.validate(self.entity, config)

def _list_entities(entity_list, report, validate):
    return [
        MetaEntity(entity=entity, report=report, validate=validate)
        for entity in entity_list
    ]

def _report_self(entity: Entity):
    return entity.name

def _report_table(entity: TableEntity):
    return f'{_report_self(entity.table)}.{_report_self(entity)}'

def _report_column(entity: ColumnEntity):
    return f'{_report_table(entity.column)}.{_report_self(entity)}'

def _validate_self(entity: Entity, config: Configuration):
    return entity.name not in config.ignore_tables

def _validate_table(entity: TableEntity, config: Configuration):
    return _validate_self(entity.table, config)

def _validate_column(entity: ColumnEntity, config: Configuration):
    return _validate_table(entity.column, config)
