# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from sql_judge.schema import Schema

def test_generate_schema_adds_tables_to_schema(mock_conn):
    schema = Schema(mock_conn)

    assert [table.name for table in schema.tables] == ['table_one', 'table_two']

def test_generate_schema_adds_functions_to_schema(build_mock_conn):
    functions = ['function_one']
    mock_adapter = build_mock_conn({'functions': {'function_one': {}}})
    schema = Schema(mock_adapter)

    assert [function.name for function in schema.functions] == functions

def test_generate_schema_adds_procedures_to_schema(build_mock_conn):
    procedures = ['procedure_one']
    mock_adapter = build_mock_conn({'procedures': {'procedure_one': {}}})
    schema = Schema(mock_adapter)

    assert [procedure.name for procedure in schema.procedures] == procedures

def test_generate_schema_adds_sequences_to_schema(build_mock_conn):
    sequences = ['sequence_one']
    mock_adapter = build_mock_conn({'sequences': {'sequence_one': {}}})
    schema = Schema(mock_adapter)

    assert [sequence.name for sequence in schema.sequences] == sequences

def test_generate_schema_adds_triggers_to_table(build_mock_conn):
    mock_adapter = build_mock_conn({
        'tables': {'table_one': {'triggers': {'trigger_one': {'hook': 'hook_one'}}}}
    })
    schema = Schema(mock_adapter)

    assert schema.triggers[0].name == 'trigger_one'
    assert schema.triggers[0].hook == 'hook_one'

def test_generate_schema_add_columns_to_schema(mock_conn):
    schema = Schema(mock_conn)

    assert [column.name for column in schema.tables[0].columns] == ['column_one']
    assert [column.name for column in schema.tables[1].columns] == ['column_1', 'column_2']

def test_generate_schema_add_constraints_to_column(build_mock_conn):
    tables_info = {
        'tables': {'table_one': {'columns': {'column_one': {
            'type': 'type_one', 'constraints': {'constraint_one': {'type': 'type_one'}}}
    }}}}
    mock_adapter = build_mock_conn(tables_info)
    schema = Schema(mock_adapter)

    assert schema.columns[0].constraints[0].name == 'constraint_one'
    assert schema.columns[0].constraints[0].type == 'type_one'

def test_generate_schema_assigns_the_column_type_to_column(mock_conn):
    schema = Schema(mock_conn)

    assert [column.type for column in schema.tables[0].columns] == ['text']

def test_generate_schema_assigns_the_primary_key_to_the_table(build_mock_conn):
    mock_conn = build_mock_conn({
        'tables': {'table_primary_key': {'columns': {'primary_column': {'type': 'integer', 'primary_key': True}}}}
    })
    schema = Schema(mock_conn)

    assert schema.tables[0].primary_key.name == 'primary_column'

def test_generate_schema_assigns_references_to_foreign_keys_columns(build_mock_conn):
    mock_conn = build_mock_conn({
        'tables': {
            'table': {'columns': {'id': {'primary_key': True}}},
            'foreign_key_table': {'columns': {'table_id': {'references': 'table'}}}
        }
    })
    schema = Schema(mock_conn)

    assert schema.tables[1].columns[0].references == schema.tables[0]

def test_generate_schema_assigns_index(build_mock_conn):
    mock_conn = build_mock_conn({
        'tables': {'table': {'columns': {'id': {'type': 'integer', 'indexes': {'id_index': {}}}}}}
    })
    schema = Schema(mock_conn)

    assert schema.tables[0].columns[0].index == schema.indexes[0]
