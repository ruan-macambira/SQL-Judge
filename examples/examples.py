def expected_initials(table_name):
    splitted = table_name[1:].split('_')
    if len(splitted) == 1:
        return 'XXXX'
    elif len(splitted) == 2:
        return splitted[1][0:4]
    elif len(splitted) == 3:
        return splitted[1][0:2] + splitted[2][0:2]
    elif len(splitted) == 4:
        return splitted[1][0:2] + splitted[2][0] + splitted[3][0]
    else:
        return splitted[1][0] + splitted[2][0] + splitted[3][0] + splitted[4][0]

def initials(table_name):
    return table_name[1:5]

def table_has_valid_initials(table):
    if initials(table.name) == expected_initials(table.name):
        return None
    else:
        return f'Unmatched Initials. Expected: {expected_initials(table.name)}, Got: {initials(table.name)}'

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
