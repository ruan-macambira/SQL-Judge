""" Generate the Report Output to the schema validation

Report Example:

REPORT
=================================================

Tables:
=================================================
 + table_one
   + message one
   + message two
---------------------------------------

Columns:
=================================================
 + table_one.column_one
   + message one
---------------------------------------
 + table_one.column_two
   + message one
---------------------------------------
"""
from typing import List

class EntityReport:
    """ Generic Class for an Entity Report

    Each EntityReport SubClass will have an constructor indicating the needed information
    to identify the identity of a given entity, and an implementation of the 'report_name'
    method, which formats the entity identity in a string, utilizing the needed data"""
    def __init__(self, table_name: str, messages: List[str]):
        self.table_name = table_name
        self.messages = messages

    def report_name(self):
        """ The unique name a given Entity has, which it will appear on the Report """
        raise NotImplementedError

class TableReport(EntityReport):
    """ Table for Reporting """
    def report_name(self):
        return self.table_name

class ColumnReport(EntityReport):
    """ Column for Reporting """
    def __init__(self, table_name: str, column_name: str, messages: List[str]):
        super().__init__(table_name, messages)
        self.column_name = column_name

    def report_name(self):
        return f'{self.table_name}.{self.column_name}'

class Report:
    """ A Form Object responsible to store every information presented in the Report """
    def __init__(self, table_reports: List[TableReport] = None,
                 column_reports: List[ColumnReport] = None):
        self.table_reports: List[TableReport] = table_reports if table_reports else []
        self.column_reports: List[ColumnReport] = column_reports if column_reports else []

def generate_entity_report(entity_name: str, messages: List[str]) -> List[str]:
    """ Serializes the messages of a given entity to the Report

    It generates a list that translates as:

     + entity
       + message one
       + message two"""
    return [f' + {entity_name}'] + [f'   + {message}' for message in messages]

def generate_entities_report(entities_report: List[EntityReport], entity_group_name: str) -> list:
    if len(entities_report) == 0:
        return []

    output = [f'{entity_group_name}:', '=' * 50]
    for entity in entities_report:
        output += generate_entity_report(entity.report_name(), entity.messages)
        output.append('-' * 40)

    return output

def generate_report(report: Report) -> List[str]:
    return ['REPORT', '=' * 50] + \
        generate_entities_report(report.table_reports, 'Tables') + \
            generate_entities_report(report.column_reports, 'Columns')