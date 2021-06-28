# pylint: disable=C,redefined-outer-name
import sys
from pytest import mark, fixture
from sql_judge import judge
from io import StringIO
from adapters.xjson_adapter import JSONAdapter
from validations import validation

BASEPATH = 'test/integration/'

def setup_module():
    sys.path.append(BASEPATH + 'adapters')
    sys.path.append(BASEPATH + 'validations')

@fixture
def iofile() -> StringIO:
    return StringIO()

@mark.integration_test
def test_cli_export(iofile: StringIO):
    judge(
        adapter=JSONAdapter('test/integration/schemas/schema.json'),
        validations_module=validation,
        ignore_tables=['skippable_table'],
        out=iofile
    )
    assert iofile.getvalue() == '\n'.join([
        "REPORT", '=' * 50,
        'table:', '=' * 50, ' + invalid_table',
        '   + Invalid', '-' * 40,
        'column:', '=' * 50,
        ' + invalid_table.invalid_column',
        '   + Invalid', '-' * 40, ''
    ])

@mark.integration_test
def test_csv_export(iofile: StringIO):
    judge(
        adapter=JSONAdapter('test/integration/schemas/schema.json'),
        validations_module=validation,
        ignore_tables=['skippable_table'],
        export='CSV',
        out=iofile
    )
    assert iofile.getvalue() == (
        'Table, invalid_table, Invalid\n'
        'Column, invalid_table.invalid_column, Invalid\n'
    )
