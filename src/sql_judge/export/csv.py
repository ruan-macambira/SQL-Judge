""" Generate Report in CSV """
from typing import List, Dict
def export_csv(report_hash: Dict[str, Dict[str, List[str]]]) -> List[str]:
    report = []
    for report_line in report_hash:
        report.append(', '.join(report_line))
    return report
