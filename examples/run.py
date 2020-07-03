#pylint: disable=missing-module-docstring
import os
from lib.run import run
from lib.validation import Configuration
from adapters.sqlite_adapter import SQLiteAdapter
from helpers import generate_sqlite_schema
from .examples import * #pylint: disable=wildcard-import


def main():
    """ run the example """
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

    generate_sqlite_schema(schema, './example_schema')

    config = Configuration(
        ignore_tables=['METADATA_INFO'],
        validations={
            'Tables': [table_has_valid_initials, table_starts_with_t],
            'Columns': [columm_starts_with_c],
            'Triggers': [], 'Indexes': [], 'Constraints': [], 'Functions': [], 'Procedures': []
        },
        connection=SQLiteAdapter('./example_schema')
        )

    try:
        report_rows = run(config)
        for row in report_rows:
            print(row)
    finally:
        os.remove('./example_schema')


if __name__ == '__main__':
    main()
