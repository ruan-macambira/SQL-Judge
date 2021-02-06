# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import pytest

from sql_judge.parse_configuration.adapter_builder import (
    UnresolvedAdapterBuilder,
    AppendedAdapterBuilder,
    default_adapter,
    from_json
)

#Fixtures
@pytest.fixture
def build_appended_adapter_builder(build_adapter_builder):
    def _build(module='module', klass='class', params=None,named_params=None):
        return build_adapter_builder(
            module=module, klass=klass,
            params=params or [], named_params = named_params or {}
        )
    return _build

@pytest.fixture
def appended_adapter_builder(build_appended_adapter_builder):
    return build_appended_adapter_builder()

# default adapter
def test_default_adapter_is_unresolved():
    assert isinstance(default_adapter(), UnresolvedAdapterBuilder)

# from json
def test_from_json_substitutes_class_with_klass():
    assert from_json({'module': 'module', 'class':'override'}).klass == 'override'


# Unresolved Adapter Builder
def test_empty_adapter_is_unresolved(build_adapter_builder):
    assert isinstance(build_adapter_builder(), UnresolvedAdapterBuilder)

def test_unresolved_adapter_is_always_elligible():
    assert UnresolvedAdapterBuilder.elligible(None)

def test_unresolved_adapter_is_invalid(unresolved_adapter):
    assert not unresolved_adapter.is_valid()

def test_unresolved_adapter_invalid_message(unresolved_adapter):
    unresolved_adapter.is_valid()
    assert unresolved_adapter.error() == \
        'Builder could not resolve Adapter Type'

def test_unresolved_adapter_converts_into_an_empty_dict(unresolved_adapter):
    assert unresolved_adapter.asdict() == {}

def test_unresolved_adapter_cannot_build(unresolved_adapter):
    with pytest.raises(RuntimeError):
        unresolved_adapter.build()

# Appended Adapter
def test_adapter_equality(build_adapter_builder):
    assert build_adapter_builder() == build_adapter_builder()

def test_adapter_with_module_and_class_is_appended(build_adapter_builder):
    assert isinstance(build_adapter_builder(module='module', klass='class'), AppendedAdapterBuilder)

def test_appended_adapter_is_validity(appended_adapter_builder):
    assert appended_adapter_builder.is_valid()

def test_appended_adapter_is_invalid_with_no_class_provided(build_appended_adapter_builder):
    assert not build_appended_adapter_builder(klass=None).is_valid()

def test_appended_adapter_is_invalid_with_no_module_provided(build_appended_adapter_builder):
    assert not build_appended_adapter_builder(module=None).is_valid()

def test_appended_adapter_asdict(appended_adapter_builder):
    assert appended_adapter_builder.asdict() == {
        'module': 'module', 'klass': 'class', 'params': [], 'named_params': {}
    }

def test_merge_appended_adapter(build_appended_adapter_builder):
    assert build_appended_adapter_builder() \
                .merge(build_appended_adapter_builder(module='override')) \
                .module == 'override'
