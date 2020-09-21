""" Use the database connection to adapt its schema to the applications objects """
from .schema import Schema
from .adapter import AbstractAdapter
from .query_schema import query_schema_from_adapter

def generate_schema(conn: AbstractAdapter) -> Schema:
    """ Generate an Schema objects containing the schema contained in the provided database """
    # return _generate_schema(QueryAdapter(conn))
    return Schema(query_schema_from_adapter(conn))

