#pylint: disable=missing-function-docstring
""" Test for running the main flow of the system """
from sql_judge import Configuration
from sql_judge.schema import Schema
from sql_judge.validate import validate_entities
from sql_judge.export import formatted_output

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

def constraint_starts_with_table_name(constraint):
    table_name = constraint.column.table.name
    if constraint.name[:len(table_name)] == table_name:
        return None
    return f"Table Should start with '{table_name}', but it is '{constraint.name}' instead"

def trigger_is_wrong(_trigger):
    return "It's Wrong"

def test_validate_run(build_mock_conn):
    # Setting Up Mock Database
    info = {
        'tables': {
            'tblProduct': {
                'columns': {
                    'id': {'type': 'numeric',
                        'indexes': {'id_index': {}},
                        'constraints': {'id_primary_key': {'type': 'primary_key'}}
                    },
                    'cl_name': {'type': 'varchar'}, 'cl_weight': {'type': 'numeric'}},
                'triggers': {'wrong_name_trigger': {'type': 'AFTER INSERT'}}
            }
        },
        'functions': {'wrong_name_function': {}},
        'procedures': {'wrong_name_procedure': {}}
    }

    # Setting Up Configuration
    config = Configuration(
        ignore_tables='metadata_info',
        validations={
            'Tables': [table_has_tbl_as_prefix],
            'Columns': [column_has_cl_as_prefix],
            'Indexes': [index_starts_with_index],
            'Constraints': [constraint_starts_with_table_name],
            'Triggers': [trigger_is_wrong],
            'Functions': [trigger_is_wrong], 'Procedures': [], 'Sequences': []
        },
        connection=build_mock_conn(info)
    )
    schema = Schema(config.connection)
    validations_result = validate_entities(config.validations, config.ignore_tables, schema)
    actual_report = formatted_output(validations_result, 'CLI')

    assert ' + tblProduct' not in actual_report
    assert ' + metadata_info' not in actual_report
    assert "   + Column 'id' does not have 'cl' as prefix" in actual_report
    assert " + tblProduct.id.id_index" in actual_report
    assert " + tblProduct.id.id_primary_key" in actual_report
    assert " + tblProduct.wrong_name_trigger" in actual_report
    assert " + wrong_name_function" in actual_report

def test_validate_csv(build_mock_conn):
    tables_info = {
        'Table': {
            'columns': {'id': 'numeric'}
        }
    }
    tables_info = {'tables': {'Table': {'columns': {'id': {'type': 'numeric'}}}}}

    config = Configuration(
        ignore_tables=[],
        validations={
            'Tables': [lambda _: 'Validation'],
            'Columns': [], 'Indexes': [], 'Constraints': [],
            'Triggers': [], 'Functions':[], 'Procedures': [], 'Sequences': []
        },
        connection=build_mock_conn(tables_info),
        export='CSV')
    schema = Schema(config.connection)
    validations_result = validate_entities(config.validations, config.ignore_tables, schema)
    actual_report = formatted_output(validations_result, 'CSV')

    assert 'Tables, Table, Validation' in actual_report
