# pylint: disable = missing-module-docstring
# pylint: disable = missing-function-docstring

from lib.report import Report, generate_report
from lib.report import TableReport, generate_table_report
from lib.report import ColumnReport, generate_column_report

def test_generate_table_report_one_message():
    table_report = TableReport(table_name='table_one', messages=['message one'])

    assert generate_table_report(table_report) == [' + table_one', '   + message one']

def test_generate_table_report_two_messages():
    table_report = TableReport(table_name='table_one', messages=['message one', 'message two'])

    assert generate_table_report(table_report) == \
        [' + table_one', '   + message one', '   + message two']

def test_generate_column_report_one_message():
    column_report = ColumnReport(table_name='table_one',
                                 column_name='column_one', messages=['message one'])

    assert generate_column_report(column_report) == [' + table_one.column_one', '   + message one']

def test_generate_column_report_two_messages():
    column_report = ColumnReport(table_name='table_one',
                                 column_name='column_one', messages=['message one', 'message two'])

    assert generate_column_report(column_report) == \
        [' + table_one.column_one', '   + message one', '   + message two']

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

def test_generate_report_one_column():
    column_reports = [
        ColumnReport(table_name='table_one', column_name='column_one', messages=['message one'])
    ]
    report = Report(column_reports=column_reports)

    assert generate_report(report) == [
        'REPORT', '=' * 50, 'Columns:', '=' * 50,
        ' + table_one.column_one', '   + message one', '-' * 40
    ]

def test_generate_report_two_columns():
    column_reports = [
        ColumnReport(table_name='table_one', column_name='column_one', messages=['message one']),
        ColumnReport(table_name='table_one', column_name='column_two', messages=['message two'])
    ]
    report = Report(column_reports=column_reports)

    assert generate_report(report) == [
        'REPORT', '=' * 50, 'Columns:', '=' * 50,
        ' + table_one.column_one', '   + message one', '-' * 40,
        ' + table_one.column_two', '   + message two', '-' * 40
    ]

def test_generate_report_one_table_one_column():
    table_reports = [TableReport(table_name='table_one', messages=['message one'])]
    column_reports = [
        ColumnReport(table_name='table_one', column_name='column_one', messages=['message one'])
    ]
    report = Report(table_reports=table_reports, column_reports=column_reports)

    assert generate_report(report) == [
        'REPORT', '=' * 50,
        'Tables:', '=' * 50,
        ' + table_one', '   + message one', '-' * 40,
        'Columns:', '=' * 50,
        ' + table_one.column_one', '   + message one', '-' * 40
    ]
