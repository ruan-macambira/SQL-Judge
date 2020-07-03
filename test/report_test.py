# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring

from lib.report import generate_report
from lib.report import _entity_report

def test_generate_entity_report_one_message():
    assert _entity_report('table_one', ['message one']) == \
        [' + table_one', '   + message one']

def test_generate_entity_report_two_messages():
    assert _entity_report('table_one.column_one', ['message one', 'message two']) == \
        [' + table_one.column_one', '   + message one', '   + message two']

def test_generate_report_one_entity():
    report = {'Tables': {
        'table_one': ['message one']
    }}

    assert generate_report(report) == [
        'REPORT', '=' * 50, 'Tables:', '=' * 50,
        ' + table_one', '   + message one', '-' * 40
    ]

def test_generate_report_two_entities():
    report = {'Columns': {
        'table_one.column_one': ['message one'],
        'table_one.column_two': ['message two']
    }}

    assert generate_report(report) == [
        'REPORT', '=' * 50, 'Columns:', '=' * 50,
        ' + table_one.column_one', '   + message one', '-' * 40,
        ' + table_one.column_two', '   + message two', '-' * 40
    ]

def test_generate_report_two_distinct_entities():
    report = {'Tables': {
        'table_one': ['message one']
    }, 'Columns': {
        'table_one.column_one': ['message one']
    }}

    assert generate_report(report) == [
        'REPORT', '=' * 50,
        'Tables:', '=' * 50,
        ' + table_one', '   + message one', '-' * 40,
        'Columns:', '=' * 50,
        ' + table_one.column_one', '   + message one', '-' * 40
    ]
