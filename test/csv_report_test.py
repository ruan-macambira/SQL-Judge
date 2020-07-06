# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from lib.csv_report import generate_report

def test_generate_report():
    report = {
        'Tables': {'Table': ['Validation']}
    }

    assert generate_report(report) == ['Tables, Table, Validation']

def test_report_ignore_empty_entity_groups():
    report = {
        'Tables': {},
        'Columns': {'Column': ['Validation']}
    }

    assert generate_report(report) == ['Columns, Column, Validation']

def test_report_ignore_empty_empty_entities():
    report = {
        'Tables': {'Table': ['Validation'], 'Another Table': []}
    }

    assert generate_report(report) == ['Tables, Table, Validation']

def test_empty_report():
    assert generate_report({}) == []
