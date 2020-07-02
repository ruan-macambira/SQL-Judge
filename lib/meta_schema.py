from dataclasses import dataclass
from typing import Callable
from .schema import Schema, Entity, TableEntity, ColumnEntity
from .validation import Configuration
class MetaSchema:
    def __init__(self, schema: Schema):
        self.schema = schema

    def _entity(self, entities, report, validate):
        return [
            MetaEntity(entity=entity, report=report, validate=validate)
            for entity in entities
        ]

    def entities(self):
        return {
            'Tables': self._entity(self.schema.tables, _report_self, _validate_self),
            'Functions': self._entity(self.schema.functions, _report_self, _validate_self),
            'Procedures': self._entity(self.schema.procedures, _report_self, _validate_self),
            'Columns': self._entity(self.schema.columns, _report_table, _validate_table),
            'Triggers': self._entity(self.schema.triggers, _report_table, _validate_table),
            'Indexes': self._entity(self.schema.indexes, _report_column, _validate_column),
            'Constraints': self._entity(self.schema.constraints, _report_column, _validate_column),
        }

    def entity_groups(self):
        return self.entities().keys()

@dataclass
class MetaEntity:
    entity: Entity
    report: Callable
    validate: Callable

    def canonical_name(self):
        return self.report(self.entity)

    def needs_validation(self, config: Configuration):
        return self.validate(self.entity, config)

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
