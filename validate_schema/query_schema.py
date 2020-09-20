VALID_ENTITIES = ['tables', 'sequences', 'functions', 'procedures', 'columns', 'triggers', 'constraints', 'indexes', 'primary_keys', 'references']
def raise_if_invalid_entity(method):
    def wrapper(self, group, *args, **kwargs):
        if group not in VALID_ENTITIES:
            raise AttributeError
        return method(self, group, *args, **kwargs)
    return wrapper

class QuerySchema:
    def __init__(self, adapter):
        self._adapter = adapter

    @raise_if_invalid_entity
    def select(self, group: str):
        return getattr(self._adapter, group)()

def query_schema_from_adapter(adapter):
    return QuerySchema(adapter)
