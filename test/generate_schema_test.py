from lib.generate_schema import generate_schema

def test_generate_schema_adds_tables_to_schema(mock_conn):
    schema = generate_schema(mock_conn)

    assert [table.name for table in schema.tables] == ['table_one', 'table_two']

def test_generate_schema_add_columns_to_scehma(mock_conn):
    schema = generate_schema(mock_conn)

    assert [column.name for column in schema.tables[0].columns] == ['column_one']
    assert [column.name for column in schema.tables[1].columns] == ['column_1', 'column_2']

def test_generate_schema_assigns_the_column_type_to_column(mock_conn):
    schema = generate_schema(mock_conn)

    assert [column.type for column in schema.tables[0].columns] == ['text']
