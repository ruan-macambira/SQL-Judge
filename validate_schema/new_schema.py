import functools

def cached_property(method):
    return property(functools.lru_cache()(method))

class Schema:
    def __init__(self, query_schema):
        self.__query_schema = query_schema

    @cached_property
    def tables(self):
        return [
            Table(schema=self, **params)
            for params in self.__query_schema.select('table')
        ]

    def __references(self, params):
        ref = _find(self.__query_schema.select('reference'), lambda el: el['table_name'] == params['table_name'] and el['column_name'] == params['name'])
        return None if not ref else ref['references']

    @cached_property
    def columns(self):
        is_primary_key = lambda col: col in self.__query_schema.select('primary_key')
        return [
            Column(
                schema=self, primary_key = is_primary_key(params),
                references = self.__references(params), **params)
            for params in self.__query_schema.select('column')
        ]

    def __entities(self, factory, group):
        return [
            factory(group=group, schema=self, **params)
            for params in self.__query_schema.select(group)
        ]

    @cached_property
    def sequences(self):
        return self.__entities(Entity, 'sequence')

    @cached_property
    def functions(self):
        return self.__entities(Entity, 'function')

    @cached_property
    def procedures(self):
        return self.__entities(Entity, 'procedure')

    @cached_property
    def triggers(self):
        return self.__entities(TableEntity, 'trigger')

    @cached_property
    def constraints(self):
        return self.__entities(ColumnEntity, 'constraint')

    @cached_property
    def indexes(self):
        return self.__entities(ColumnEntity, 'index')

class Entity:
    def __init__(self, group, schema, name, **additional_params):
        self._schema = schema
        self.__name = name
        self.__group = group
        self._additional_params = additional_params

    @property
    def name(self):
        return self.__name

    @property
    def group(self):
        return self.__group

    @property
    def schema(self):
        return self._schema

    def __getattribute__(self, item):
        if item in super().__getattribute__('_additional_params'):
            return self._additional_params[item]
        return super().__getattribute__(item)

class Table(Entity):
    def __init__(self, name, schema, **additional_params):
        super().__init__(group='table', name=name, schema=schema, **additional_params)
    @property
    def columns(self):
        return [
            column for column in self._schema.columns if column.table.name == self.name
        ]

    @property
    def primary_key(self): # precisa adicionar a opção de adicionar no schema para ser implementado
        return _find(self.columns, lambda col: col.primary_key)

    @property
    def triggers(self):
        return [
            trigger for trigger in self._schema.triggers if trigger.table.name == self.name
        ]


class TableEntity(Entity):
    def __init__(self, group, name, table_name, schema, **additional_params):
        super().__init__(group=group, name=name, schema=schema, **additional_params)
        self._table_name = table_name
        self._table = _find(self._schema.tables, lambda el: el.name == self._table_name)

    @property
    def table(self):
        return self._table

class Column(TableEntity):
    def __init__(self, name, table_name, schema, primary_key=False, references=None, **additional_params):
        super().__init__(group='column', name=name, table_name=table_name, schema=schema, **additional_params)
        self.__primary_key = primary_key
        self._references = references

    @property
    def primary_key(self):
        return self.__primary_key

    @property
    def references(self): # precisa adicionar a opção de adicionar no schema para ser implementado
        if not self._references:
            return None
        return _find(self._schema.tables, lambda el: el.name == self._references)

    @property
    def indexes(self):
        return [
            index for index in self._schema.indexes
            if index.table.name == self._table_name and index.column.name == self.name
        ]

    @property
    def constraints(self):
        return [
            cons for cons in self._schema.constraints
            if cons.table.name == self._table_name and cons.column.name == self.name
        ]

class ColumnEntity(TableEntity):
    def __init__(self, group, name, table_name, column_name, schema, **additional_params):
        super().__init__(group=group, name=name, table_name=table_name, schema=schema, **additional_params)
        self._column_name = column_name

    @property
    def column(self) -> Column:
        return _find(self._schema.columns, lambda el: el.table.name == self._table_name and el.name == self._column_name)

def _find(collection, condition):
    return next((element for element in collection if condition(element)), None)
