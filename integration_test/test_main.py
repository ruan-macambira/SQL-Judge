# pylint: disable=C
import sys
from sql_judge.__main__ import sql_judge
from pytest import mark

def setup_module():
    sys.path.append('integration_test/adapters')
    sys.path.append('integration_test/validations')

@mark.integration_test
def test_main():
    config = ['integration_test/configs/config.json']
    expected_output = []
    assert sql_judge(config) == expected_output

@mark.xfail
@mark.integration_test
def test_empty_configuration():
    config = ['integration_test/configs/empty_config.json']
    assert sql_judge(config) == []

@mark.xfail
@mark.integration_test
def test_invalid_configuration():
    config = ['integration_test/configs/invalid_config.json']
    assert sql_judge(config) == []

@mark.xfail
@mark.integration_test
def test_non_existent_file():
    config = ['integration_test/configs/nonexistent_config.json']
    assert sql_judge(config) == []
