""" Generate Reports in different output format """
from typing import List, Dict, Callable, Any
from .csv import export_csv
from .cli import export_cli

def formatted_output(report: dict, xformat: str) -> List[str]:
    """Generates a report based in the format presented in 'xformat'"""
    formats: Dict[str, Callable[[Any], List[str]]] = {
        'CLI': export_cli,
        'CSV': export_csv
    }
    return formats[xformat](report)
