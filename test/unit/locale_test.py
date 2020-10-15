# pylint: disable=C
from pytest import raises
from sql_judge import locale

def setup_function():
    locale.load_labels({
        'key': 'value'
    })

def test_get_existing_key():
    assert locale.translate('key') == 'value'

def test_get_nonexistent_key():
    with raises(RuntimeError):
        locale.translate('non_key')

def test_t_is_an_alias_for_translate():
    assert locale.translate('key') == locale.t('key')
