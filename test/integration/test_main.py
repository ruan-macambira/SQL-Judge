# pylint: disable=C
import sys
from sql_judge.__main__ import sql_judge
from pytest import mark

BASEPATH = 'test/integration/'

def setup_module():
    sys.path.append(BASEPATH + 'adapters')
    sys.path.append(BASEPATH + 'validations')

@mark.integration_test
def test_main():
    config = [BASEPATH + 'configs/config.json']
    expected_output = []
    assert sql_judge(config) == expected_output

@mark.xfail
@mark.integration_test
def test_empty_configuration():
    config = [BASEPATH + 'configs/empty_config.json']
    assert sql_judge(config) == []

@mark.xfail
@mark.integration_test
def test_invalid_configuration():
    config = [BASEPATH + 'configs/invalid_config.json']
    assert sql_judge(config) == []

@mark.xfail
@mark.integration_test
def test_non_existent_file():
    config = [BASEPATH + 'configs/nonexistent_config.json']
    assert sql_judge(config) == []
