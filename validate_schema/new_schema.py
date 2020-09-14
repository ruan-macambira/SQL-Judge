class Schema:
    def __init__(self, query_schema):
        self.__query_schema = query_schema

class Entity:
    def __init__(self, group, query_schema, name, **additional_params):
        self._query_schema = query_schema
        self.__name = name
        self.__group = group
        self.__additional_params = additional_params

    @property
    def name(self):
        return self.__name

    @property
    def group(self):
        return self.__group

    @property
    def schema(self):
        return Schema(self._query_schema)

    def __getattr__(self, item):
        if item in self.__additional_params:
            return self.__additional_params[item]
        raise AttributeError(f"Object '{type(self).__name__}' has no attribute '{item}'")


class Table(Entity):
    def __init__(self, name, query_schema, **additional_params):
        super().__init__(group='table', name=name, query_schema=query_schema, **additional_params)
    @property
    def columns(self):
        return [
            Column(query_schema=self._query_schema, **params)
            for params in self._query_schema.select_from_table('column', self.name)
        ]

    @property
    def primary_key(self): # precisa adicionar a opção de adicionar no schema para ser implementado
        raise NotImplementedError

    @property
    def triggers(self):
        return [
            TableEntity(group='trigger', query_schema=self._query_schema, **params)
            for params in self._query_schema.select_from_table('trigger', self.name)
        ]


class TableEntity(Entity):
    def __init__(self, group, name, table_name, query_schema, **additional_params):
        super().__init__(group=group, name=name, query_schema=query_schema, **additional_params)
        self._table_name = table_name

    @property
    def table(self):
        table_options = _find(self._query_schema.select_from_schema('table'), lambda el: el['name'] == self._table_name)
        return Table(query_schema=self._query_schema, **table_options)

class Column(TableEntity):
    def __init__(self, name, table_name, query_schema, **additional_params):
        super().__init__(group='column', name=name, table_name=table_name, query_schema=query_schema, **additional_params)

    @property
    def indexes(self):
        return [
            ColumnEntity(group='index', query_schema=self._query_schema, **params)
            for params in self._query_schema.select_from_column('index', self._table_name, self.name)
        ]

    @property
    def constraints(self):
        return [
            ColumnEntity(group='constraint', query_schema=self._query_schema, **params)
            for params in self._query_schema.select_from_column('constraint', self._table_name, self.name)
        ]

    @property
    def references(self): # precisa adicionar a opção de adicionar no schema para ser implementado
        raise NotImplementedError

class ColumnEntity(TableEntity):
    def __init__(self, group, name, table_name, column_name, query_schema, **additional_params):
        super().__init__(group=group, name=name, table_name=table_name, query_schema=query_schema, **additional_params)
        self._column_name = column_name

    @property
    def column(self) -> Column:
        column_options = _find(self._query_schema.select_from_table('column', table_name=self._table_name), lambda el: el['name'] == self._column_name)
        return Column(query_schema=self._query_schema, **column_options)

def _find(collection, condition):
    return next((element for element in collection if condition(element)), None)
