# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import json
import pytest
from validate_schema.parse_configuration.build_configuration import ConfigurationBuilder

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

def test_merging_a_builder_preserves_adapter_class_if_not_present(build_configuration_builder):
    assert build_configuration_builder() \
        .merge(build_configuration_builder(adapter_class=None)) \
        .adapter_class == build_configuration_builder().adapter_class

def test_merging_a_builder_overwrites_adapter_class_if_present(build_configuration_builder):
    assert build_configuration_builder(adapter_class='original_class') \
        .merge(build_configuration_builder(adapter_class='overwritten_class')) \
        .adapter_class == 'overwritten_class'

def test_mergind_a_builder_preserves_adapter_class_if_not_present(build_configuration_builder):
    assert build_configuration_builder(adapter_class='original_class') \
        .merge(build_configuration_builder(adapter_class=None)) \
        .adapter_class == 'original_class'

def test_merging_a_build_overwrites_adapter_params_if_present(build_configuration_builder):
    assert build_configuration_builder(adapter_params=['foo']) \
        .merge(build_configuration_builder(adapter_params=['bar'])) \
        .adapter_params == ['bar']

def test_merging_a_build_preserves_adapter_params_if_not_present(build_configuration_builder):
    assert build_configuration_builder(adapter_params=['foo']) \
        .merge(build_configuration_builder()) \
        .adapter_params == ['foo']

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



# from_json
def test_from_json_parses_json_string_and_generates_a_configuration_builder():
    json_str = json.dumps({
        'adapter': {
            'module': 'adapter', 'class': 'Adapter',
            'params': ['foo'], 'named_params': {'foo': 'bar'}},
        'ignore_tables':['metainfo'], 'validations': {'module': 'validations'}
    })
    assert ConfigurationBuilder.from_json(json_str) == \
        ConfigurationBuilder(
            adapter_module='adapter', adapter_class='Adapter',
            adapter_params=['foo'], adapter_named_params={'foo':'bar'},
            ignore_tables=['metainfo'], validations_module='validations'
        )

def test_from_json_succeeds_even_with_an_empty_config():
    json_str = json.dumps({})
    assert ConfigurationBuilder.from_json(json_str) == ConfigurationBuilder()
