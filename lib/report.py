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
 + table_two
   + message_one

Columns:
=================================================
 + table_one.column_one
   + message one
---------------------------------------
 + table_one.column_two
   + message one
---------------------------------------
 + table_two.column_one
   + message one
"""
from typing import List

class TableReport:
    def __init__(self, table_name: str, messages: List[str]):
        self.table_name = table_name
        self.messages = messages

class ColumnReport:
    def __init__(self, table_name: str, column_name: str, messages: List[str]):
        self.table_name = table_name
        self.column_name = column_name
        self.messages = messages

class Report:
    def __init__(self, table_reports: List[TableReport] = None,
                 column_reports: List[ColumnReport] = None):
        self.table_reports: List[TableReport] = table_reports if table_reports else []
        self.column_reports: List[ColumnReport] = column_reports if column_reports else []

def generate_table_report(table_report: TableReport):
    output = []
    output.append(f' + {table_report.table_name}')

    for message in table_report.messages:
        output.append(f'   + {message}')

    return output

def generate_column_report(column_report: ColumnReport):
    output = []
    output.append(f' + {column_report.table_name}.{column_report.column_name}')
    for message in column_report.messages:
        output.append(f'   + {message}')

    return output

def generate_report(report):
    output = []
    output.append('REPORT')
    output.append('=' * 50)

    if len(report.table_reports) > 0:
        output.append('Tables:')
        output.append('=' * 50)

    for table_report in report.table_reports:
        output += generate_table_report(table_report)
        output.append('-' * 40)

    if len(report.column_reports) > 0:
        output.append('Columns:')
        output.append('=' * 50)

    for column_report in report.column_reports:
        output += generate_column_report(column_report)
        output.append('-' * 40)

    return output
