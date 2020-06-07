from .schema import Table
from typing import Callable, List, Tuple

def run_table_validations(table: Table, validations: List[Callable]) -> List[str]:
    if table is None:
        raise TypeError
    if len(validations) == 0:
        raise ValueError

    raw_messages = [val(table) for val in validations]
    return [message for message in raw_messages if message is not None]

def run_tableset_validation(tableset: List[Table], validations: List[Callable]) -> List[Tuple[Table, str]]:
    val_res: List[Tuple[Table, str]] = []

    for table in tableset:
        aux = run_table_validations(table, validations)
        if len(aux) != 0:
            val_res += [(table, message) for message in aux]
    
    return val_res
