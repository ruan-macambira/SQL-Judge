# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

def _stripped_table_name(table):
    if table_starts_with_tbl(table) is None:
        return table.name[4:]
    return table.name

def table_starts_with_tbl(table):
    if table.name[0:4] == 'TBL_':
        return None
    return 'Table should start with "TBL_"'

def referenced_table_is_named_after_its_reference(column):
    if column.references is None:
        return None
    expected_name = _stripped_table_name(column.references) + '_ID'
    if column.name != expected_name:
        return f'Since it\' a foreign key, column should be named "{expected_name}"'

def column_name_matches_type(column):
    if column.primary_key or column.references:
        return None
    expected_prefix = {
        'DATETIME': 'DT',
        'REAL': 'RL_',
        'VARCHAR': 'VC_',
        '': ''
    }
    if expected_prefix[column.type] == column.name[0:3]:
        return None
    return f'{column.type} column should start with {expected_prefix[column.type]}'

def trigger_starts_with_tg(trigger):
    if trigger.name[0:3] == 'TG_':
        return None
    return 'Trigger name should start with "TG_"'
