""" Test for running the main flow of the system """
from lib.validation import batch_validate_entities, ValidationConfig, \
    tables_to_validate, columns_to_validate
from lib.generate_schema import generate_schema
from lib.run import run

def table_has_tbl_as_prefix(table):
    if table.name[0:3] != 'tbl':
        return f"Table '{table.name}' does not have 'tbl' as prefix"
    return None

def column_has_cl_as_prefix(column):
    if column.name[0:2] != 'cl':
        return f"Column '{column.name}' does not have 'cl' as prefix"

def primary_key_columns_should_be_named_id(column):
    if column.primary_key is False:    
        return None
    if column.name.upper() == 'ID':
        return None
    return f"Column should be named 'id', but it is '{column.name}' instead"

def tests_validate_database_schema(build_mock_conn):
    # Setting Up Mock Database
    mock_values = {
        'tblProduct': [
            {'name': 'id', 'type': 'numeric', 'primary_key': 'true'},
            {'name': 'cl_name', 'type': 'varchar'},
            {'name':'cl_weight', 'type': 'numeric'}
        ],
        'tblService': [
            {'name': 'service_id', 'type': 'numeric', 'primary_key': 'true'}
        ],
        'metadata_info': [{'name': 'version', 'type': 'varchar'}]
    }

    # Setting Up Configuration
    config = ValidationConfig(
        ignore_tables='metadata_info',
        table_validations=[table_has_tbl_as_prefix],
        column_validations=[column_has_cl_as_prefix, primary_key_columns_should_be_named_id],
        connection=build_mock_conn(mock_values)
    )

    schema = generate_schema(config.connection)

    tbl_product = schema.tables[0]
    tbl_service = schema.tables[1]
    metadata = schema.tables[2]

    # Validate
    validation_tables = tables_to_validate(schema, config)
    validation_columns = columns_to_validate(schema, config)

    assert metadata not in batch_validate_entities(validation_tables, config.table_validations)
    assert batch_validate_entities(validation_columns, config.column_validations)[0] == \
        (tbl_product.columns[0], "Column 'id' does not have 'cl' as prefix")
    assert batch_validate_entities(validation_columns, config.column_validations)[2] == \
        (tbl_service.columns[0], "Column should be named 'id', but it is 'service_id' instead")

def tests_validate_run(build_mock_conn):
    # Setting Up Mock Database
    mock_values = {
        'tblProduct': [
            {'name': 'id', 'type': 'numeric'},
            {'name': 'cl_name', 'type': 'varchar'},
            {'name':'cl_weight', 'type': 'numeric'}
        ],
        'metadata_info': [{'name': 'version', 'type': 'varchar'}]
    }

    # Setting Up Configuration
    config = ValidationConfig(
        ignore_tables='metadata_info',
        table_validations=[table_has_tbl_as_prefix],
        column_validations=[column_has_cl_as_prefix],
        connection=build_mock_conn(mock_values)
    )

    actual_report = run(config)

    assert ' + tblProduct' not in actual_report
    assert ' + metadata_info' not in actual_report
    assert "   + Column 'id' does not have 'cl' as prefix" in actual_report
