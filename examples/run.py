import os
from lib.run import run
from lib.validation import ValidationConfig
from lib.connection import SQLiteConnection
from helpers import generate_sqlite_schema
from .examples import *


def main():
    schema = {
        'tbl_store': [
            {'name': 'id', 'type': 'integer', 'primary_key': 'true'},
            {'name': 'cl_name', 'type': 'varchar'},
            {'name': 'cl_address', 'type': 'varchar'}
        ], 'employee': [
            {'name': 'id', 'type': 'integer', 'primary_key': 'true'},
            {'name': 'store_id', 'type': 'integer', 'references': 'tbl_store(id)'},
            {'name': 'name', 'type': 'varchar'}
        ], 'metadata_info': [{'name': 'version', 'type': 'varchar'}]
    }

    generate_sqlite_schema('./example_schema', schema)

    config = ValidationConfig(
            ignore_tables=['METADATA_INFO'],
            table_validations=[table_has_valid_initials, table_starts_with_t],
            column_validations=[columm_starts_with_c],
            connection=SQLiteConnection('./example_schema')
        )

    report_rows = run(config)

    for row in report_rows:
        print(row)
    os.remove('./example_schema')


if __name__ == '__main__':
    main()