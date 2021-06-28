""" Fixtures """
# pylint: disable=redefined-outer-name
from pytest import fixture
from sql_judge.serialized_adapter import SerializedAdapter
from sql_judge import schema

@fixture
def build_schema_adapter():
    """ Mock Database schema Adapter Factory """
    def _build_schema_adapter(info):
        return SerializedAdapter(info)
    return _build_schema_adapter

@fixture
def schema_adapter(build_schema_adapter):
    """ A basic mock database schema adapter """
    return build_schema_adapter({
        'tables': {
            'table_one': {'columns': {'column_one': {'type': 'text'}}},
            'table_two': {'columns': {'column_1': {'type': 'int'}, 'column_2': {'type': 'int'}}}
        }
    })

@fixture
def serial_schema():
    def _serial_schema(info: dict):
        return schema.Schema(SerializedAdapter(info))
    return _serial_schema

@fixture
def build_entity():
    def build(group: str, name: str, **custom_params):
        return getattr(schema, group)(schema=None, name=name, **custom_params)
    return build
