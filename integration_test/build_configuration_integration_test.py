# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import json
import pkg_resources
from sql_judge.parse_configuration.build_configuration import ConfigurationBuilder

def test_build_configuration_loads_adapter_instance(build_configuration_builder, adapter_module):
    assert build_configuration_builder(
        adapter_module='adapter', adapter_class='Adapter'
    ).build().connection == adapter_module.Adapter()

def test_default_configuration_is_a_valid_json_config_except_for_user_defined_modules():
    json_obj = json.loads(pkg_resources.resource_string(
        'sql_judge.parse_configuration', 'default_configuration.json'))
    json_obj.update({
        'adapter': {
            'module': 'adapter',
            'class': 'Adapter'
        }, 'validations': {
            'module': 'validations'
        }
    })
    json_str = json.dumps(json_obj)
    assert ConfigurationBuilder.from_json(json_str).is_valid() is True
