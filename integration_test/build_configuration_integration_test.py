# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pkg_resources
from sql_judge.parse_configuration.build_configuration import ConfigurationBuilder

def test_build_configuration_loads_adapter_instance(build_configuration_builder, adapter_module):
    assert build_configuration_builder(
        adapter_module='adapter', adapter_class='Adapter'
    ).build().connection == adapter_module.Adapter()

def test_default_configuration_is_a_valid_json_config():
    json_str = pkg_resources.resource_string(
        'sql_judge.parse_configuration', 'default_configuration.json')
    assert ConfigurationBuilder.from_json(json_str).is_valid() is True
