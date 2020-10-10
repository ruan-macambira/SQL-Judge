# pylint: disable=C
import sys
import logging
from sql_judge.__main__ import sql_judge
from pytest import mark, fixture

@fixture
def stdout(capsys):
    return capsys.readouterr().out

BASEPATH = 'test/integration/'

def setup_module():
    sys.path.append(BASEPATH + 'adapters')
    sys.path.append(BASEPATH + 'validations')

@mark.integration_test
def test_empty_configuration(caplog):
    config = [BASEPATH + 'configs/empty_config.json']
    sql_judge(config)
    assert caplog.record_tuples[0] == ('root', logging.ERROR, 'Adapter Module not provided')

@mark.integration_test
def test_invalid_configuration(caplog):
    config = [BASEPATH + 'configs/invalid_config.json']
    sql_judge(config)
    assert caplog.record_tuples[0] == ('root', logging.ERROR, 'Error while parsing configuration')

@mark.integration_test
def test_non_existent_file(caplog):
    config = [BASEPATH + 'configs/nonexistent_config.json']
    sql_judge(config)
    assert caplog.record_tuples[0] == ('root', logging.ERROR, "File 'test/integration/configs/nonexistent_config.json' could not be found")

@mark.integration_test
def test_cli_export(stdout):
    config = [BASEPATH + 'configs/config.json']
    assert sql_judge(config) == [
        'REPORT', '=' * 50, 'table:', '=' * 50, ' + invalid_table', '   + Invalid', '-' * 40
    ]

@mark.integration_test
def test_csv_export(stdout):
    config = [BASEPATH + 'configs/config.json', BASEPATH + 'configs/config_csv.json']
    assert sql_judge(config) == ['Table, invalid_table, Invalid']
