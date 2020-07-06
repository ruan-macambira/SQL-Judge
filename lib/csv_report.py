""" Generate Report in CSV """
from typing import List, Dict
def generate_report(report_hash: Dict[str, Dict[str, List[str]]]) -> List[str]:
    csv_report = []
    for entity_group, entities in report_hash.items():
        for entity, messages in entities.items():
            for message in messages:
                csv_report.append('{}, {}, {}'.format(entity_group, entity, message))
    return csv_report
