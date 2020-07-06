#pylint: disable=missing-module-docstring
from lib.run import run
from lib.configuration import Configuration
from lib.mock_adapter import MockAdapter
from .examples import * #pylint: disable=wildcard-import


def main():
    """ run the example """
    adapter = MockAdapter({
        'metainfo': {
            'columns':{'alter_hash': 'text', 'comment': 'text'},
            'primary_key': 'id',
        },
        'tbl_user': {
            'columns': {'id': 'int', 'vc_username': 'varchar', 'vc_password': 'varchar'},
            'primary_key': 'id',
        },
        'tbl_product': {
            'columns': {'id': 'int', 'product_name': 'varchar', 'rl_price': 'real'},
            'primary_key': 'id',
        },
        'purchases': {
            'columns':{'buyer': 'int', 'product_id': 'int', 'nm_quantity': 'int'},
            'primary_key': 'buyer',
            'references': {'product_id': 'tbl_product'},
            'triggers': {'tg_new_product_history': 'after insert'}
        },
        'tbl_price_history': {
            'columns': {'product_id': 'int', 'history_price': 'real', 'dt_since': 'datetime'},
            'references': {'product_id': 'tbl_product'},
            'triggers': {'alter_product_price': 'after update'}
        },
    })
    config = Configuration(
        ignore_tables=['metainfo'],
        validations={
            'Tables': [table_starts_with_tbl],
            'Columns': [referenced_table_is_named_after_its_reference, column_name_matches_type],
            'Triggers': [trigger_starts_with_tg],
            'Indexes': [], 'Constraints': [], 'Functions': [], 'Procedures': []
        },
        connection=adapter
    )
    report_rows = run(config)
    for row in report_rows:
        print(row)


if __name__ == '__main__':
    main()
