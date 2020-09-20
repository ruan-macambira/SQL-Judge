# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring
from validate_schema.validate import validate_entity, validate_entities
from validate_schema.generate_schema import generate_schema
from validate_schema import validates

def pass_validation(_table):
    return None

def fail_validation(_table):
    return 'ERROR'

def raise_validation(_table):
    raise Exception('something wrong happened')

# validate_entity
def test_validate_entity_returns_a_list(table):
    assert validate_entity(table, [pass_validation, fail_validation]) == ['ERROR']

def test_validate_entity_no_messages_returns_empty_list(table):
    assert validate_entity(table, [pass_validation]) == []

def test_validate_entity_captures_exceptions_and_passes_to_messages(table):
    assert validate_entity(table, [raise_validation]) == \
        ['validation "raise_validation" raised a Exception with the message "something wrong happened"']

# validate
def test_validate_entities(build_mock_conn, configuration):
    mock_adapter = build_mock_conn({'tables': {'table_one': {}}})

    config = configuration(validations={'Tables': [fail_validation], 'Columns': [pass_validation]})
    schema = generate_schema(mock_adapter)
    assert validate_entities(config, schema) == {
        'Tables': {'table_one': ['ERROR']}, 'Functions': {}, 'Procedures': {},
        'Columns': {}, 'Triggers': {}, 'Indexes': {}, 'Constraints': {}, 'Sequences': {}
    }

# validates
@validates('table')
def validation(_table):
    return 'It runs!'

def test_validates_sets_validates_attribute():
    assert validation.validates == 'table'

def test_validates_returns_callable():
    assert validation(None) == 'It runs!'
