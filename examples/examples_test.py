# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring
from validate_schema.schema import Table, Column, Trigger
from . import examples

def table(name):
    return Table(name)

# table_starts_with_tbl
def test_starts_with_tbl():
    assert examples.table_starts_with_tbl(table('TBL_TABLE')) is None

def test_does_not_start_with_tbl():
    assert examples.table_starts_with_tbl(table('TABLE')) == 'Table should start with "TBL_"'

# referenced_table_is_named_after_its_reference
def test_table_is_names_after_its_reference():
    column = Column(name='TABLE_ID', col_type='', references=Table('TABLE'))
    assert examples.referenced_table_is_named_after_its_reference(column) is None

def test_Table_is_not_named_after_its_reference():
    column = Column(name='COL_TABLE', col_type='', references=Table('TABLE'))
    assert examples.referenced_table_is_named_after_its_reference(column) == \
        'Since it\' a foreign key, column should be named "TABLE_ID"'

# column_name_matches_type
def test_name_matches_type():
    column = Column(name='RL_REAL', col_type='REAL')
    assert examples.column_name_matches_type(column) is None

def test_name_does_not_match_type():
    column = Column(name='REAL', col_type='REAL')
    assert examples.column_name_matches_type(column) == \
        'REAL column should start with RL_'

# trigger_starts_with_tg
def test_starts_with_tg():
    assert examples.trigger_starts_with_tg(Trigger('TG_TRIGGER', 'BEFORE UPDATE')) is None

def test_does_not_start_with_tg():
    assert examples.trigger_starts_with_tg(Trigger('TRIGGER', 'AFTER UPDATE')) == \
        'Trigger name should start with "TG_"'
