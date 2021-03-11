# pylint: disable=C
import sys
import logging
from sql_judge.__main__ import sql_judge
from pytest import mark

BASEPATH = 'test/integration/'

def setup_module():
    sys.path.append(BASEPATH + 'adapters')
    sys.path.append(BASEPATH + 'validations')

@mark.integration_test
def test_no_configuration(caplog):
    sql_judge([])
    assert caplog.record_tuples[0] == ('root', logging.ERROR, 'At least one configuration file must be provided')

@mark.integration_test
def test_empty_configuration(caplog):
    config = [BASEPATH + 'configs/empty_config.json']
    sql_judge(config)
    assert caplog.record_tuples[0] == ('root', logging.ERROR, 'Builder could not resolve Adapter Type')

@mark.integration_test
def test_invalid_configuration(caplog):
    config = [BASEPATH + 'configs/invalid_config.json']
    sql_judge(config)
    assert caplog.record_tuples[0] == ('root', logging.ERROR, "Error while parsing 'test/integration/configs/invalid_config.json'")

@mark.integration_test
def test_non_existent_file(caplog):
    config = [BASEPATH + 'configs/nonexistent_config.json']
    sql_judge(config)
    assert caplog.record_tuples[0] == ('root', logging.ERROR, "File 'test/integration/configs/nonexistent_config.json' could not be found")

@mark.integration_test
def test_nonexisten_plugin(caplog):
    config = [BASEPATH + 'configs/plugin_does_not_exist_config.json']
    sql_judge(config)
    assert caplog.record_tuples[0] == ('root', logging.ERROR, "Could not find plugin with 'nonexistent_adapter' ID")

@mark.integration_test
def test_plugin_adapter():
    config = [BASEPATH + 'configs/plugin_config.json']
    assert sql_judge(config) == [
        'REPORT', '=' * 50,
        'table:', '=' * 50,' + invalid_table', '   + Invalid', '-' * 40,
        'column:', '=' * 50, ' + invalid_table.invalid_column', '   + Invalid', '-' * 40
    ]

@mark.integration_test
def test_cli_export():
    config = [BASEPATH + 'configs/config.json']
    assert sql_judge(config) == [
        'REPORT', '=' * 50,
        'table:', '=' * 50,' + invalid_table', '   + Invalid', '-' * 40,
        'column:', '=' * 50, ' + invalid_table.invalid_column', '   + Invalid', '-' * 40
    ]

@mark.integration_test
def test_csv_export():
    config = [BASEPATH + 'configs/config.json', BASEPATH + 'configs/config_csv.json']
    assert sql_judge(config) == [
        'Table, invalid_table, Invalid',
        'Column, invalid_table.invalid_column, Invalid'
        ]
