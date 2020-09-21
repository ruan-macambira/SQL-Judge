""" Fixtures """
# pylint: disable=redefined-outer-name
import pytest
from validate_schema.adapter import AbstractAdapter
from validate_schema import Configuration
from validate_schema.serialized_adapter import SerializedAdapter
from validate_schema.parse_configuration.build_configuration import ConfigurationBuilder
from validate_schema.schema import Table

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
def table():
    return Table(schema=None, name='table_name')

@pytest.fixture
def configuration_builder(build_configuration_builder):
    """ Basic Configuration Builder """
    return build_configuration_builder()

@pytest.fixture
def empty_configuration_builder():
    """ Empty Configuration Builder """
    return ConfigurationBuilder()

# adapter.DBAdapter
@pytest.fixture
def db_adapter():
    """ Basic DB Adapter """
    return AbstractAdapter()

@pytest.fixture
def configuration():
    VALIDATIONS = {
        'Tables': [], 'Functions': [], 'Procedures': [], 'Sequences': [],
        'Columns': [], 'Triggers': [], 'Constraints': [], 'Indexes': []
    }
    def _configuration(connection=None, validations=None, ignore_tables=None, export='CLI'):
        return Configuration(
            connection=connection,
            validations={**VALIDATIONS, **(validations or {})},
            ignore_tables=ignore_tables or [],
            export=export
        )
    return _configuration

@pytest.fixture
def build_mock_conn():
    """ Mock Database schema Adapter Factory """
    def _build_mock_conn(info):
        return SerializedAdapter(info)
    return _build_mock_conn

@pytest.fixture
def mock_conn(build_mock_conn):
    """ A basic mock database schema adapter """
    return build_mock_conn({
        'tables': {
            'table_one': {'columns': {'column_one': {'type': 'text'}}},
            'table_two': {'columns': {'column_1': {'type': 'int'}, 'column_2': {'type': 'int'}}}
        }
    })
