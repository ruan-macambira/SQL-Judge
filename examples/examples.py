# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from validate_schema import validates

def _stripped_table_name(table):
    if table_starts_with_tbl(table) is None:
        return table.name[4:].upper()
    return table.name

@validates('Tables')
def table_starts_with_tbl(table):
    if table.name[0:4].upper() == 'TBL_':
        return None
    return 'Table should start with "TBL_"'

@validates('Columns')
def referenced_table_is_named_after_its_reference(column):
    if column.references is None:
        return None
    expected_name = _stripped_table_name(column.references) + '_ID'
    if column.name != expected_name:
        return f'Since it\' a foreign key, column should be named "{expected_name}"'

@validates('Columns')
def column_name_matches_type(column):
    if column.primary_key or column.references:
        return None
    expected_prefix = {
        'DATETIME': 'DT_',
        'REAL': 'RL_',
        'VARCHAR': 'VC_',
        '': '',
        'INT': 'NM_'
    }
    if expected_prefix[column.type.upper()] == column.name[0:3].upper():
        return None
    return f'{column.type} column should start with {expected_prefix[column.type.upper()]}'

@validates('Triggers')
def trigger_starts_with_tg(trigger):
    if trigger.name[0:3].upper() == 'TG_':
        return None
    return 'Trigger name should start with "TG_"'
