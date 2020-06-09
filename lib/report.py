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

class Report:
    def __init__(self, table_reports: List[TableReport] = None):
        self.table_reports = table_reports if table_reports else []

def generate_table_report(table_report: TableReport):
    output = []
    output.append(f' + {table_report.table_name}')

    for message in table_report.messages:
        output.append(f'   + {message}')
    
    return output

def generate_report(report):
    output = []
    output.append('REPORT')
    output.append('=' * 50)
    output.append('Tables:')
    output.append('=' * 50)

    for table_report in report.table_reports:
        output += generate_table_report(table_report)
        output.append('-' * 40)

    return output