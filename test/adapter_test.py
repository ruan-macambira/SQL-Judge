# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

def test_tables_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.tables()

def test_columns_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.columns('table')

def test_primary_key_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.primary_key('table', 'column')

def test_references_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.references('table', 'column')

def test_index_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.index('table', 'column')
