# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from collections import namedtuple
import pytest
from validate_schema.configuration import configuration_from_module

@pytest.fixture
def configuration():
    mockule = namedtuple('mockule', ['adapter', 'validations', 'ignore_tables', 'export'])
    mock_module = mockule(
        adapter=lambda: 'adapter',
        validations=lambda: 'validations',
        ignore_tables=lambda: 'ignore_tables',
        export=lambda: 'export'
    )
    return configuration_from_module(mock_module)

def test_configuration_has_adapter(configuration): #pylint: disable=redefined-outer-name
    assert configuration.connection == 'adapter'

def test_configuration_has_validations(configuration): #pylint: disable=redefined-outer-name
    assert configuration.validations == 'validations'

def test_configuration_has_ignore_tables(configuration): #pylint: disable=redefined-outer-name
    assert configuration.ignore_tables == 'ignore_tables'

def test_configuration_has_export(configuration): #pylint: disable=redefined-outer-name
    assert configuration.export == 'export'
