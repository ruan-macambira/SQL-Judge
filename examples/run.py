from lib.run import run
from lib.validation import ValidationConfig
from lib.connection import SQLiteConnection
from helpers import generate_sqlite_schema
from .examples import *


schema = {
        'tblProduct': [
            {'name': 'id', 'type': 'numeric'},
            {'name': 'cl_name', 'type': 'varchar'},
            {'name':'cl_weight', 'type': 'numeric'}
        ],
        'metadata_info': [{'name': 'version', 'type': 'varchar'}]
}

generate_sqlite_schema('./example_schema', schema)

config = ValidationConfig(
        ignore_tables=['METADATA_INFO'],
        table_validations=[table_has_valid_initials, table_starts_with_t],
        # column_validations=[column_has_cl_as_prefix],
        column_validations=[columm_starts_with_c],
        connection=SQLiteConnection('./example_schema')
    )

if __name__ == '__main__':
    report_rows = run(config)

    for row in report_rows:
        print(row)
