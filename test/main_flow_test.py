""" Test for running the main flow of the system """
from lib.schema import Schema, Table, Column, add_column, add_table
from lib.validation import batch_validate_entities, ValidationConfig, tables_to_validate, columns_to_validate

def table_has_tbl_as_prefix(table):
    if table.name[0:3] != 'tbl':
        return f"Table '{table.name}' does not have 'tbl' as prefix"
    return None

def column_has_cl_as_prefix(column):
    if column.name[0:2] != 'cl':
        return f"Column '{column.name}' does not have 'cl' as prefix"

def tests_validate_database_schema():
    # Setting Up Mock Database
    schema = Schema()

    tbl_product = Table('tblProduct')
    metadata = Table('metadata_info')

    add_table(schema, tbl_product)
    add_table(schema, metadata)

    add_column(tbl_product, Column('id', 'numeric'))
    add_column(tbl_product, Column('cl_name', 'varchar'))
    add_column(tbl_product, Column('cl_weight', 'numberic'))

    add_column(metadata, Column('version', 'varchar'))

    # Setting Up Configuration
    config = ValidationConfig(
        ignore_tables='metadata_info',
        table_validations=[table_has_tbl_as_prefix],
        column_validations=[column_has_cl_as_prefix]
    )

    # Validate
    validation_tables = tables_to_validate(schema, config)
    validation_columns = columns_to_validate(schema, config)

    assert metadata not in batch_validate_entities(validation_tables, config.table_validations)
    assert batch_validate_entities(validation_columns, config.column_validations)[0] == \
        (tbl_product.columns[0], "Column 'id' does not have 'cl' as prefix")
