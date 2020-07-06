# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from lib.export.csv import export_csv

def test_generate_report():
    report = {
        'Tables': {'Table': ['Validation']}
    }

    assert export_csv(report) == ['Tables, Table, Validation']

def test_report_ignore_empty_entity_groups():
    report = {
        'Tables': {},
        'Columns': {'Column': ['Validation']}
    }

    assert export_csv(report) == ['Columns, Column, Validation']

def test_report_ignore_empty_empty_entities():
    report = {
        'Tables': {'Table': ['Validation'], 'Another Table': []}
    }

    assert export_csv(report) == ['Tables, Table, Validation']

def test_empty_report():
    assert export_csv({}) == []
