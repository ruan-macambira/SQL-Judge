import itertools
VALID_ENTITIES = ['table', 'sequence', 'function', 'procedure', 'column', 'trigger', 'constraint', 'index']
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

