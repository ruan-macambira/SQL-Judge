#pylint: disable=missing-module-docstring
import subprocess
import os
from lib.run import run
from lib.validation import Configuration
from adapters.sqlite_adapter import SQLiteAdapter
from .examples import * #pylint: disable=wildcard-import


def main():
    """ run the example """
    schema = subprocess.run(
        f'sh {os.path.dirname(__file__)}/generate_schema.sh',
        shell=True, check=True, text=True, capture_output=True
    ).stdout.strip()
    config = Configuration(
        ignore_tables=['METAINFO'],
        validations={
            'Tables': [table_starts_with_tbl],
            'Columns': [referenced_table_is_named_after_its_reference, column_name_matches_type],
            'Triggers': [trigger_starts_with_tg],
            'Indexes': [], 'Constraints': [], 'Functions': [], 'Procedures': []
        },
        connection=SQLiteAdapter(schema)
    )
    try:
        report_rows = run(config)
        for row in report_rows:
            print(row)
    finally:
        os.remove(schema)


if __name__ == '__main__':
    main()
