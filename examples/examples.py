# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
def _expected_initials(table_name):
    splitted = table_name[1:].split('_')
    if len(splitted) == 1:
        return 'XXXX'
    if len(splitted) == 2:
        return splitted[1][0:4]
    if len(splitted) == 3:
        return splitted[1][0:2] + splitted[2][0:2]
    if len(splitted) == 4:
        return splitted[1][0:2] + splitted[2][0] + splitted[3][0]
    return splitted[1][0] + splitted[2][0] + splitted[3][0] + splitted[4][0]

def _initials(table_name):
    return table_name[1:5]

def table_has_valid_initials(table):
    if _initials(table.name) == _expected_initials(table.name):
        return None
    return f'Unmatched Initials. Expected: {_expected_initials(table.name)}' \
        f', Got: {_initials(table.name)}'

def table_starts_with_t(table):
    if table.name[0].upper() == 'T':
        return None
    return 'Table should start with t'

def columm_starts_with_c(column):
    if column.primary_key:
        return 'this column acts as an primary key'
    if column.references is not None:
        return 'this column refences {}'.format(column.table.name)
    if column.name[0].upper() == 'C':
        return None
    return 'Column should start with c'
