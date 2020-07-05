""" Fixtures """
# pylint: disable=redefined-outer-name
import pytest
from lib.schema import Schema, Table, Column, Index, Constraint, Trigger, SchemaEntity
from lib.generate_schema import add_entity_to_schema, add_subentity_to_entity
from lib.adapter import DBAdapter
from lib.validation import Configuration
from lib.mock_adapter import MockAdapter

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

# validation.ValidationConfig
@pytest.fixture
def build_validation_config():
    """ Validation Configuration object Factory """
    def _build_validation_config(validations=None, connection=None, ignore_tables=None):
        return Configuration(
            connection=connection, validations=validations or {},
            ignore_tables=ignore_tables or []
        )
    return _build_validation_config

@pytest.fixture
def validation_config(build_validation_config, mock_conn):
    """ Basic validation Configuration File """
    return build_validation_config(validations={}, connection=mock_conn, ignore_tables=[])

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
