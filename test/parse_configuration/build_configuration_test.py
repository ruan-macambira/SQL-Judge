# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import json
import pytest
from validate_schema.parse_configuration.build_configuration import ConfigurationBuilder
from ..test_modules import adapter

# ConfigurationBuilder.is_valid
def test_empty_builder_is_invalid(empty_configuration_builder):
    assert empty_configuration_builder.is_valid() is False

def test_valid_builder(configuration_builder):
    assert configuration_builder.is_valid() is True

def test_builder_is_invalid_when_there_is_no_adapter_module(build_configuration_builder):
    assert build_configuration_builder(adapter_module=None).is_valid() is False

def test_builder_is_invalid_when_there_is_no_adapter_class(build_configuration_builder):
    assert build_configuration_builder(adapter_class=None).is_valid() is False

def test_builder_is_invalid_when_there_is_no_validations_module(build_configuration_builder):
    assert build_configuration_builder(validations_module=None).is_valid() is False

def test_builder_is_invalid_when_there_is_no_export_format(build_configuration_builder):
    assert build_configuration_builder(export_format=None).is_valid() is False

# ConfigurationBuilder.merge
def test_merging_a_builder_to_an_empty_build_does_not_affect_it():
    configuration_builder = ConfigurationBuilder()
    assert configuration_builder == \
        configuration_builder.merge(ConfigurationBuilder())

def test_merging_a_builder_does_preserves_adapter_module_if_not_present(build_configuration_builder):
    assert build_configuration_builder() \
        .merge(build_configuration_builder(adapter_module=None)) \
        .adapter_module == build_configuration_builder().adapter_module

def test_merging_a_builder_overwrites_adapter_module_if_present(build_configuration_builder):
    assert build_configuration_builder() \
        .merge(build_configuration_builder(adapter_module='overwritten_module')) \
        .adapter_module == 'overwritten_module'

def test_merging_a_builder_does_preserves_adapter_class_if_not_present(build_configuration_builder):
    assert build_configuration_builder() \
        .merge(build_configuration_builder(adapter_class=None)) \
        .adapter_class == build_configuration_builder().adapter_class

def test_merging_a_builder_overwrites_adapter_class_if_present(build_configuration_builder):
    assert build_configuration_builder() \
        .merge(build_configuration_builder(adapter_class='overwritten_class')) \
        .adapter_class == 'overwritten_class'

def test_merging_two_builders_concatenate_their_ignored_tables(build_configuration_builder):
    builder_one = build_configuration_builder(ignore_tables=['foo'])
    builder_two = build_configuration_builder(ignore_tables=['bar'])
    assert builder_one.merge(builder_two).ignore_tables == ['foo', 'bar']

def test_merging_a_builder_does_preserves_validations_module_if_not_present(build_configuration_builder):
    assert build_configuration_builder() \
        .merge(build_configuration_builder(validations_module=None)) \
        .validations_module == build_configuration_builder().validations_module

def test_merging_a_builder_overwrites_validations_module_if_present(build_configuration_builder):
    assert build_configuration_builder() \
        .merge(build_configuration_builder(validations_module='overwritten_module')) \
        .validations_module == 'overwritten_module'

# ConfigurationBuilder.build
def test_trying_to_build_an_invalid_configuration_raises_value_error(build_configuration_builder):
    with pytest.raises(ValueError):
        build_configuration_builder(adapter_module=None).build()

def test_build_configuration_sends_export_format_as_is(build_configuration_builder):
    assert build_configuration_builder(export_format='CLI').build().export == 'CLI'

def test_build_configuration_sends_ignore_tables_as_is(build_configuration_builder):
    assert build_configuration_builder(ignore_tables=['metainfo']) \
        .build().ignore_tables == ['metainfo']

def test_build_configuration_loads_adapter_instance(build_configuration_builder):
    assert build_configuration_builder(
        adapter_module='test.test_modules.adapter', adapter_class='Adapter'
    ).build().connection == adapter.Adapter()

# from_json
def test_from_json_parses_json_string_and_generates_a_configuration_builder():
    json_str = json.dumps({
        'adapter': {'module': 'adapter', 'class': 'Adapter'},
        'ignore_tables':['metainfo'], 'validations': {'module': 'validations'}
    })
    assert ConfigurationBuilder.from_json(json_str) == \
        ConfigurationBuilder(
            adapter_module='adapter', adapter_class='Adapter',
            ignore_tables=['metainfo'], validations_module='validations'
        )

def test_from_json_succeeds_even_with_an_empty_config():
    json_str = json.dumps({})
    assert ConfigurationBuilder.from_json(json_str) == ConfigurationBuilder()

def test_default_configuration_is_a_valid_json_config():
    # TODO: remover teste dos unitários e fazê-lo carregar o JSON das configurações padrões
    json_str = r"""{
        "adapter": {"module": "adapter","class": "Adapter","args": {}},
        "validations": {"module": "validations"},
        "ignore_tables": [],
        "export": {"format": "CLI","output": "stdout"}}"""
    assert ConfigurationBuilder.from_json(json_str).is_valid() is True
