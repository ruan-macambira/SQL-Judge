""" Fixtures """
# pylint: disable=redefined-outer-name
from pytest import fixture
from sql_judge.serialized_adapter import SerializedAdapter
from sql_judge.parse_configuration.build_configuration import ConfigurationBuilder
from sql_judge.parse_configuration import adapter_builder
from sql_judge import schema

@fixture
def build_configuration_builder(build_adapter_builder):
    """ Configuration Builder Factory """
    def _build(
        adapter_module='test.test_modules.adapter', adapter_class='Adapter',
        adapter_params=None, adapter_named_params=None,
        validations_module='test.test_modules.validations',
        ignore_tables=None, export_format='CLI'):
        return ConfigurationBuilder(
            adapter=build_adapter_builder(
                module=adapter_module,
                klass=adapter_class,
                params=adapter_params or [],
                named_params=adapter_named_params or {}
            ),
            validations_module=validations_module,
            ignore_tables=ignore_tables or [],
            export_format=export_format
        )
    return _build

@fixture
def configuration_builder(build_configuration_builder):
    """ Basic Configuration Builder """
    return build_configuration_builder()

@fixture
def build_adapter_builder():
    """Adapter Builder Factory"""
    def _build(**options):
        return adapter_builder.load(options)
    return _build

@fixture
def unresolved_adapter(build_adapter_builder):
    """Unresolved Adapter Builder"""
    return build_adapter_builder()

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
