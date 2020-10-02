""" Generate Report in CSV """
from typing import List, Dict
def export_csv(report_hash: Dict[str, Dict[str, List[str]]]) -> List[str]:
    report = []
    for entity_group, entities in report_hash.items():
        for entity, messages in entities.items():
            for message in messages:
                report.append('{}, {}, {}'.format(entity_group, entity, message))
    return report
