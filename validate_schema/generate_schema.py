""" Use the database connection to adapt its schema to the applications objects """
from .schema import Schema, Table, Column, Index, Constraint, Trigger, SchemaEntity, Entity
from .adapter import DBAdapter
from .query_adapter import QueryAdapter
from .query_schema import query_schema_from_adapter
from .new_schema import Schema as NSchema

def generate_schema(conn: DBAdapter) -> Schema:
    """ Generate an Schema objects containing the schema contained in the provided database """
    # return _generate_schema(QueryAdapter(conn))
    return NSchema(query_schema_from_adapter(conn))

def _generate_schema(conn: QueryAdapter) -> Schema:
    schema = Schema()
    for table_name in conn.tables():
        table: Table = Table(table_name)
        _insert_columns_to_table(table, conn)
        _insert_triggers_to_table(table, conn)
        add_entity_to_schema(schema, table, 'tables')

    for column in schema.columns:
        _insert_references_to_column(column, schema, conn)
        _insert_index_to_column(column, conn)
        _insert_constraints_to_column(column, conn)

    for function_name in conn.functions():
        function: SchemaEntity = SchemaEntity(function_name)
        add_entity_to_schema(schema, function, 'functions')

    for procedure_name in conn.procedures():
        procedure: SchemaEntity = SchemaEntity(procedure_name)
        add_entity_to_schema(schema, procedure, 'procedures')

    for sequence_name in conn.sequences():
        sequence: SchemaEntity = SchemaEntity(sequence_name)
        add_entity_to_schema(schema, sequence, 'sequences')

    return schema

def add_subentity_to_entity(entity, ref_entity: str, subentity: Entity, ref_subentity: str):
    """ Add SubEntity to Entity """
    getattr(entity, ref_subentity).append(subentity)
    setattr(subentity, ref_entity, entity)

def add_entity_to_schema(schema: Schema, entity: Entity, ref_entity: str):
    """ Add Entity to Schema """
    add_subentity_to_entity(schema, 'schema', entity, ref_entity)

def add_index_to_column(column: Column, index: Index) -> None:
    """ Add an Index to a Column """
    setattr(column, 'index', index)
    setattr(index, 'column', column)

def _insert_columns_to_table(table: Table, conn: QueryAdapter) -> None:
    for name, col_type in conn.columns(table.name).items():
        column = Column(name=name, col_type=col_type,
                        primary_key=conn.primary_key(table.name, name))
        add_subentity_to_entity(table, 'table', column, 'columns')

def _insert_triggers_to_table(table: Table, conn: QueryAdapter) -> None:
    for name, hook in conn.triggers(table.name).items():
        trigger = Trigger(name=name, hook=hook)
        add_subentity_to_entity(table, 'table', trigger, 'triggers')

def _insert_references_to_column(column: Column, schema: Schema, conn: QueryAdapter) -> None:
    references = conn.references(column.table.name, column.name)
    for table in schema.tables:
        if references == table.name:
            column.references = table
            return

def _insert_index_to_column(column: Column, conn: QueryAdapter) -> None:
    index_name = conn.index(column.table.name, column.name)
    if index_name is not None:
        add_index_to_column(column, Index(name=index_name))

def _insert_constraints_to_column(column: Column, conn: QueryAdapter) -> None:
    for (cons_name, cons_type) in conn.constraints(column.table.name, column.name).items():
        constraint = Constraint(name=cons_name, cons_type=cons_type)
        add_subentity_to_entity(column, 'column', constraint, 'constraints')
