from lib.run import run
from lib.validation import ValidationConfig
from lib.connection import DBConnection
from .examples import *

class MockConnection(DBConnection):
    """ Mock classes to generate the return values of a connection object """
    def __init__(self, mock_values):
        self.mock_values = mock_values

    def execute(self, sql):
        return None

    def tables(self):
        return self.mock_values.keys()

    def columns(self, table_name):
        return self.mock_values[table_name]

_mock_values = {
        'tblProduct': [
            {'name': 'id', 'type': 'numeric'},
            {'name': 'cl_name', 'type': 'varchar'},
            {'name':'cl_weight', 'type': 'numeric'}
        ],
        'metadata_info': [{'name': 'version', 'type': 'varchar'}]
}

config = ValidationConfig(
        ignore_tables=['metadata_info'],
        table_validations=[table_has_valid_initials, table_starts_with_t],
        # column_validations=[column_has_cl_as_prefix],
        column_validations=[columm_starts_with_c],
        connection=MockConnection(_mock_values)
    )

if __name__ == '__main__':
    report_rows = run(config)

    for row in report_rows:
        print(row)
