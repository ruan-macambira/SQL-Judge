""" Fixtures """
# pylint: disable=redefined-outer-name
import pytest
from validate_schema.schema import Schema, Table, Column, Index, Constraint, Trigger, SchemaEntity
from validate_schema.generate_schema import add_entity_to_schema, add_subentity_to_entity
from validate_schema.adapter import DBAdapter
from validate_schema import Configuration
from validate_schema.mock_adapter import MockAdapter
from validate_schema.parse_configuration.build_configuration import ConfigurationBuilder

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
def empty_configuration_builder():
    """ Empty Configuration Builder """
    return ConfigurationBuilder()

# adapter.DBAdapter
@pytest.fixture
def db_adapter():
    """ Basic DB Adapter """
    return DBAdapter()

# schema.Schema
@pytest.fixture
def build_schema(build_table):
    """ Schema Factory """
    def _build_schema(tables: int = 0):
        at_schema = Schema()
        for i in range(tables):
            add_entity_to_schema(at_schema, build_table(name=f'table_{i}'), 'tables')
        return at_schema
    return _build_schema

@pytest.fixture
def schema(build_schema):
    """ Basic Schema """
    return build_schema()


# schema.Table
@pytest.fixture
def build_table(build_column):
    """ Table Factory """
    def _build_table(name: str = 'table_name', columns: int = 0):
        at_table = Table(name)
        for _ in range(columns):
            add_subentity_to_entity(at_table, 'table', build_column(), 'columns')
        return at_table
    return _build_table

@pytest.fixture
def table(build_table):
    """ Basic Table """
    return build_table()

# schema.Column
@pytest.fixture
def build_column():
    """ Column Factory """
    def _build_column(name: str = 'column_name', col_type: str = 'column_type',
                      primary_key: bool = False, references: Table = None):
        return Column(name=name, col_type=col_type, primary_key=primary_key, references=references)
    return _build_column

@pytest.fixture
def column(build_column):
    """ Basic Column """
    return build_column()

@pytest.fixture
def primary_key_column(build_column):
    """ Column that serves as a Primary Key in a Table"""
    return build_column(primary_key=True)

# schema.Index
@pytest.fixture
def index():
    """ Basic Index """
    return Index('index', False)

# schema.constraint
@pytest.fixture
def constraint():
    """ Basic Constraint """
    return Constraint('constraint', 'PK')

#schema.trigger
@pytest.fixture
def trigger():
    """ Basic Trigger """
    return Trigger('trigger', 'AFTER INSERT')

#schema.function
@pytest.fixture
def function():
    """ Basic function """
    return SchemaEntity('function')

@pytest.fixture
def procedure():
    """ Basic Procedure """
    return SchemaEntity('procedure')

@pytest.fixture
def configuration():
    VALIDATIONS = {
        'Tables': [], 'Functions': [], 'Procedures': [],
        'Columns': [], 'Triggers': [], 'Constraints': [], 'Indexes': []
    }
    def _configuration(connection=None, validations=None, ignore_tables=None, export='CLI'):
        return Configuration(
            connection=connection,
            validations=validations or VALIDATIONS,
            ignore_tables=ignore_tables or [],
            export=export
        )
    return _configuration

@pytest.fixture
def build_mock_conn():
    """ Mock Database schema Adapter Factory """
    def _build_mock_conn(tables_info, functions_info=None, procedures_info=None):
        return MockAdapter(tables_info, functions_info, procedures_info)
    return _build_mock_conn

@pytest.fixture
def mock_conn(build_mock_conn):
    """ A basic mock database schema adapter """
    return build_mock_conn({
        'table_one': {
            'columns': {'column_one': 'text'},
        }, 'table_two': {
            'columns': {'column_1': 'int', 'column_2': 'int'}
        }
    })
