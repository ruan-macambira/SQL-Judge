# pylint: disable=C
from pytest import raises
from sql_judge import locale

def setup_module():
    locale.load_labels({
        'key': 'value',
        'nested_key': {'key': 'nested_value'}
    })

def test_get_existing_key():
    assert locale.translate('key') == 'value'

def test_get_nested_key():
    assert locale.translate('nested_key.key') == 'nested_value'

def test_get_nested_key_scope():
    assert locale.translate('key', scope='nested_key') == 'nested_value'

def test_get_nonexistent_key():
    with raises(RuntimeError):
        locale.translate('non_key')

def test_get_nonexistent_nested_key():
    with raises(RuntimeError):
        locale.translate('nested_key.non_key')

def test_t_is_an_alias_for_translate(): 
    assert locale.translate('key') == locale.t('key')
