# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest
from sql_judge.export import formatted_output

@pytest.fixture
def report():
    return { 'Tables': { 'table_one': ['validation_one'] } }

def test_formatted_output_cli(report): #pylint: disable=redefined-outer-name
    assert formatted_output(report, 'CLI')[4] == ' + table_one'
    assert formatted_output(report, 'CLI')[5] == '   + validation_one'

def test_formatted_output_csv(report):  #pylint: disable=redefined-outer-name
    assert formatted_output(report, 'CSV') == ['Tables, table_one, validation_one']
