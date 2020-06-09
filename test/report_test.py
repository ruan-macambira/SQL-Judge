# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring

from lib.report import Report, generate_report
from lib.report import TableReport, generate_table_report

def test_generate_table_report():
    table_report = TableReport(table_name='table_one', messages=['message one'])

    assert generate_table_report(table_report) == [' + table_one', '   + message one']

def test_generate_report_one_table():
    table_report = TableReport(table_name='table_one', messages=['message one'])
    report = Report([table_report])

    assert generate_report(report) == [
        'REPORT', '=' * 50, 'Tables:', '=' * 50,
        ' + table_one', '   + message one', '-' * 40
    ]

def test_generate_report_two_tables():
    table_reports = [
        TableReport(table_name='table_one', messages=['message one']),
        TableReport(table_name='table_two', messages=['message two'])
    ]
    report = Report(table_reports)

    assert generate_report(report) == [
        'REPORT', '=' * 50, 'Tables:', '=' * 50,
        ' + table_one', '   + message one', '-' * 40,
        ' + table_two', '   + message two', '-' * 40
    ]
