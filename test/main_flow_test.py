#pylint: disable=missing-function-docstring
""" Test for running the main flow of the system """
from lib.validation import batch_validate_entities, Configuration, entities_to_validate
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

def foreign_key_columns_should_be_table_name_id(column):
    if column.references is None:
        return None
    expected_name = f'{column.references.name}_id'.upper()
    if column.name.upper() == expected_name:
        return None
    return f"Column should be named '{expected_name}', but it is '{column.name.upper()}' instead"

def index_starts_with_index(index):
    if index.name == f'index_{index.column.name}':
        return None
    return f"Table Should start with 'index', but it is '{index.name}' instead"

def tests_validate_database_schema(build_mock_conn):
    # Setting Up Mock Database
    mock_values = {
        'tblProduct': {
            'columns': {'id': 'numeric', 'cl_name': 'varchar', 'cl_weigth': 'numeric'},
            'primary_key': ['id']
        }, 'tblService': {
            'columns': {'service_id': 'numeric'},
            'primary_key': ['service_id']
        }, 'tblEmployee': {
            'columns': {'id': 'integer', 'service_id': 'integer'},
            'primary_key': ['id'],
            'references': {'service_id': 'tblService'}
        }, 'metadata_info': {
            'columns': {'version': 'varchar'}
        }
    }

    # Setting Up Configuration
    config = Configuration(
        ignore_tables='metadata_info',
        validations={
            'Tables': [table_has_tbl_as_prefix],
            'Columns': [column_has_cl_as_prefix,
                        primary_key_columns_should_be_named_id,
                        foreign_key_columns_should_be_table_name_id],
        },
        connection=build_mock_conn(mock_values)
    )

    schema = generate_schema(config.connection)

    tbl_product = schema.tables[0]
    tbl_service = schema.tables[1]
    tbl_employee = schema.tables[2]
    metadata = schema.tables[3]

    # Validate
    validation_tables = entities_to_validate('Tables', schema, config)
    validation_columns = entities_to_validate('Columns', schema, config)

    assert metadata not in batch_validate_entities(validation_tables, config.validations['Tables'])
    assert batch_validate_entities(validation_columns, config.validations['Columns'])[0] == \
        (tbl_product.columns[0], "Column 'id' does not have 'cl' as prefix")
    assert batch_validate_entities(validation_columns, config.validations['Columns'])[2] == \
        (tbl_service.columns[0], "Column should be named 'id', but it is 'service_id' instead")
    assert batch_validate_entities(validation_columns, config.validations['Columns'])[5] == \
        (tbl_employee.columns[1],
         "Column should be named 'TBLSERVICE_ID', but it is 'SERVICE_ID' instead")

def tests_validate_run(build_mock_conn):
    # Setting Up Mock Database
    mock_values = {
        'tblProduct': {
            'columns': {
                'id': 'numeric', 'cl_name': 'varchar', 'cl_weight': 'numeric'
            },
            'indexes': {
                'id': 'id_index'
            }
        }, 'metadata_info': {
            'columns': {'version': 'varchar'}
        }
    }

    # Setting Up Configuration
    config = Configuration(
        ignore_tables='metadata_info',
        validations={
            'Tables': [table_has_tbl_as_prefix],
            'Columns': [column_has_cl_as_prefix],
            'Indexes': [index_starts_with_index]
        },
        connection=build_mock_conn(mock_values)
    )

    actual_report = run(config)

    assert ' + tblProduct' not in actual_report
    assert ' + metadata_info' not in actual_report
    assert "   + Column 'id' does not have 'cl' as prefix" in actual_report
    assert " + tblProduct.id.id_index" in actual_report
