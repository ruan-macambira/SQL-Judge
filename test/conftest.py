""" Fixtures """
# pylint: disable=redefined-outer-name
import pytest
from sql_judge.serialized_adapter import SerializedAdapter
from sql_judge.parse_configuration.build_configuration import ConfigurationBuilder
from sql_judge.schema import Schema

@pytest.fixture
def build_configuration_builder():
    """ Configuration Builder Factory """
    def _build(
        adapter_module='test.test_modules.adapter', adapter_class='Adapter',
        adapter_params=None, adapter_named_params=None,
        validations_module='test.test_modules.validations',
        ignore_tables=None, export_format='CLI'):
        return ConfigurationBuilder(
            adapter_module=adapter_module,
            adapter_class=adapter_class,
            adapter_params=adapter_params or [],
            adapter_named_params=adapter_named_params or {},
            validations_module=validations_module,
            ignore_tables=ignore_tables or [],
            export_format=export_format
        )
    return _build

@pytest.fixture
def configuration_builder(build_configuration_builder):
    """ Basic Configuration Builder """
    return build_configuration_builder()

@pytest.fixture
def build_schema_adapter():
    """ Mock Database schema Adapter Factory """
    def _build_schema_adapter(info):
        return SerializedAdapter(info)
    return _build_schema_adapter

@pytest.fixture
def schema_adapter(build_schema_adapter):
    """ A basic mock database schema adapter """
    return build_schema_adapter({
        'tables': {
            'table_one': {'columns': {'column_one': {'type': 'text'}}},
            'table_two': {'columns': {'column_1': {'type': 'int'}, 'column_2': {'type': 'int'}}}
        }
    })

@pytest.fixture
def serial_schema():
    def _serial_schema(info: dict):
        return Schema(SerializedAdapter(info))
    return _serial_schema
