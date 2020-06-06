def table_has_valid_initials(table_name):
    splitted = table_name[1:].split('_')
    if len(splitted) == 2:
        return splitted[0] == splitted[1][0:4]
    elif len(splitted) == 3:
        return splitted[0] == splitted[1][0:2] + splitted[2][0:2]
    elif len(splitted) == 4:
        return splitted[0] == splitted[1][0:2] + splitted[2][0] + splitted[3][0]
    elif len(splitted) >= 5:
        return splitted[0] == splitted[1][0] + splitted[2][0] + splitted[3][0] + splitted[4][0]
    else:
        return False

def table_starts_with_t(table_name):
    return table_name[0].upper() == 'T'