# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest
from sql_judge import judge

def test_raises_when_adapter_is_not_instance_of_abstract_adapter():
    with pytest.raises(RuntimeError):
        judge(
            adapter=tuple(),
            validations_module=None
        )
