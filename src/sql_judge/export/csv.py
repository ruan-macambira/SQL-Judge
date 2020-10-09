""" Generate Report in CSV """
from typing import List, Dict
from ..validate import Fail
def export_csv(report_hash: List[Fail]) -> List[str]:
    report = []
    for group, report_name, message in report_hash:
        report.append(f'{group.capitalize()}, {report_name}, {message}')
    return report
