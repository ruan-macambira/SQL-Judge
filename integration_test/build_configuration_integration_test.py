# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest
from validate_schema.parse_configuration.build_configuration import ConfigurationBuilder

# ConfigurationBuilder.build
def test_build_configuration_sends_export_format_as_is(build_configuration_builder):
    assert build_configuration_builder(export_format='CLI').build().export == 'CLI'

def test_build_configuration_passes_unnamed_params(build_configuration_builder):
    assert build_configuration_builder(adapter_params=['foo']) \
        .build().connection.args == ('foo',)

def test_build_configuration_passes_named_params(build_configuration_builder):
    assert build_configuration_builder(adapter_named_params={'foo':'bar'}) \
        .build().connection.kwargs == {'foo': 'bar'}

def test_build_configuration_sends_ignore_tables_as_is(build_configuration_builder):
    assert build_configuration_builder(ignore_tables=['metainfo']) \
        .build().ignore_tables == ['metainfo']

def test_build_configuration_loads_adapter_instance(build_configuration_builder, adapter_module):
    assert build_configuration_builder(
        adapter_module='integration_test.adapter', adapter_class='Adapter'
    ).build().connection == adapter_module.Adapter()

def test_default_configuration_is_a_valid_json_config():
    # TODO: remover teste dos unitários e fazê-lo carregar o JSON das configurações padrões
    json_str = r"""{
        "adapter": {"module": "adapter","class": "Adapter","params": [], "named_params": {}},
        "validations": {"module": "validations"},
        "ignore_tables": [],
        "export": {"format": "CLI","output": "stdout"}}"""
    assert ConfigurationBuilder.from_json(json_str).is_valid() is True
