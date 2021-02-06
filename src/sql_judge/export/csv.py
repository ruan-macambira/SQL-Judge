""" Generate the Report Output in CSV format

Report Example:
Table, table_one, message one
Table, table_one, message two
Column, table_one.column_one, message one
Column, table_one.column_two, message one
"""
from typing import List
from ..validate import Fail
def export_csv(report_hash: List[Fail]) -> List[str]:
    report = []
    for group, report_name, message in report_hash:
        report.append(f'{group.capitalize()}, {report_name}, {message}')
    return report
