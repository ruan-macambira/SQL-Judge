VALID_ENTITIES = ['table', 'sequence', 'function', 'procedure', 'column', 'trigger', 'constraint', 'index', 'primary_key', 'reference']
def raise_if_invalid_entity(method):
    def wrapper(self, group, *args, **kwargs):
        if group not in VALID_ENTITIES:
            raise AttributeError
        return method(self, group, *args, **kwargs)
    return wrapper

class QuerySchema:
    def __init__(self):
        self.__entities = {entity: [] for entity in VALID_ENTITIES}

    @raise_if_invalid_entity
    def insert(self, group: str, entities: list):
        self.__entities[group] += entities

    @raise_if_invalid_entity
    def select(self, group: str):
        return self.__entities[group]

def query_schema_from_adapter(adapter):
    query_schema = QuerySchema()

    tables = ({'name': name} for name in adapter.tables())
    query_schema.insert('table', tables)

    functions = ({'name': name} for name in adapter.functions())
    query_schema.insert('function', functions)

    procedures = ({'name': name} for name in adapter.procedures())
    query_schema.insert('procedure', procedures)

    sequences = ({'name': name} for name in adapter.sequences())
    query_schema.insert('sequence', sequences)

    columns = ({'table_name': table, 'name': name, 'type': ctype} for (table, name, ctype) in adapter.columns())
    query_schema.insert('column', columns)

    primary_keys = ({'table_name': table, 'name': name} for (table, name) in adapter.primary_keys())
    query_schema.insert('primary_key', primary_keys)

    references = (
        {'table_name': table, 'column_name': column, 'references': references}
        for (table, column, references) in adapter.references())
    query_schema.insert('reference', references)

    triggers = ({'table_name': table, 'name': name, 'hook': hook} for (table, name, hook) in adapter.triggers())
    query_schema.insert('trigger', triggers)

    indexes = ({'table_name': table, 'column_name': column, 'name': name} for (table, column, name) in adapter.indexes())
    query_schema.insert('index', indexes)

    constraints = (
        {'table_name': table, 'column_name': column, 'name': name, 'type': ctype}
        for (table, column, name, ctype) in adapter.constraints())
    query_schema.insert('constraint', constraints)

    return query_schema
