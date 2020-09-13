VALID_ENTITIES = ['table', 'sequence', 'function', 'procedure', 'column', 'trigger', 'constraint', 'index']
def raise_if_invalid_entity(method):
    def wrapper(self, group, *args, **kwargs):
        if group not in VALID_ENTITIES:
            raise AttributeError
        return method(self, group, *args, **kwargs)
    return wrapper

class QuerySchema:
    def __init__(self):
        self.__from_schema = {'table': [], 'sequence': [], 'function': [], 'procedure': []}
        self.__from_table = {'column': {}, 'trigger': {}}
        self.__from_column = {'constraint': {}, 'index': {}}

    @raise_if_invalid_entity
    def insert_to_schema(self, group: str, schema_entities: list):
        self.__from_schema[group] = schema_entities

    @raise_if_invalid_entity
    def insert_to_table(self, group: str, table_entities: list):
        from_group = self.__from_table[group]
        for table_entity in table_entities:
            table_name = table_entity['table_name']
            if from_group.get(table_name) is None:
                from_group[table_name] = []
            from_group[table_name].append(table_entity)

    @raise_if_invalid_entity
    def insert_to_column(self, group: str, column_entities: list):
        from_group = self.__from_column[group]
        for column_entity in column_entities:
            column_identifier = (column_entity['table_name'], column_entity['column_name'])
            if from_group.get(column_identifier) is None:
                from_group[column_identifier] = []
            from_group[column_identifier].append(column_entity)

    @raise_if_invalid_entity
    def select_from_schema(self, group: str):
        return self.__from_schema[group]

    @raise_if_invalid_entity
    def select_from_table(self, group: str, table_name: str):
        return self.__from_table[group][table_name]

    @raise_if_invalid_entity
    def select_from_column(self, group: str, table_name: str, column_name: str):
        return self.__from_column[group][(table_name, column_name)]
