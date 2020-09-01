""" Generate Reports in different output format """
from typing import List
from .csv import export_csv
from .cli import export_cli

def formatted_output(report: dict, xformat: str) -> List[str]:
    return {
        'CLI': export_cli,
        'CSV': export_csv
    }[xformat](report)
