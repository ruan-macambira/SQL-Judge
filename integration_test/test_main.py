import sys
import pytest
from sql_judge.__main__ import sql_judge

def setup_module():
    sys.path.append('integration_test/adapters')
    sys.path.append('integration_test/validations')

@pytest.mark.integration_test
def test_main():
    config = ['integration_test/configs/config.json']
    expected_output = []
    assert sql_judge(config) == expected_output
