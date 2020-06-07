# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring
from lib.schema import Table
from . import examples

def table(name):
    return Table(name)

# table_starts_with_t
def test_start_with_t_validation():
    assert examples.table_starts_with_t(table('TCONTATO')) is True

def test_not_start_with_t_validation():
    assert examples.table_starts_with_t(table('CONTATO')) is False

# table_has_valid_initials
def test_table_has_one_word_initials():
    assert examples.table_has_valid_initials(table('TPESS_PESSOA')) is True

def test_table_has_two_words_initials():
    assert examples.table_has_valid_initials(table('TPELU_PESSOA_LUGAR')) is True

def test_table_has_three_words_initials():
    assert examples.table_has_valid_initials(table('TPELO_PESSOA_LUGAR_OBJETO')) is True

def test_table_has_four_words_initials():
    assert examples.table_has_valid_initials(table('TPLOC_PESSOA_LUGAR_OBJETO_COR'))

def test_table_has_four_plus_words_initials():
    assert examples.table_has_valid_initials(table('TPLOC_PESSOA_LUGAR_OBJETO_COR_CARRO'))

def test_table_has_no_initials():
    assert examples.table_has_valid_initials(table('TCONTATO')) is False
