from lib.adapter import DBAdapter

class MockAdapter(DBAdapter):
    """ Mock classes to generate the return values of a connection object """
    def __init__(self, mock_values):
        self.mock_values = mock_values
    
    def connection(self):
        return None

    def execute(self, sql):
        return None

    def tables(self):
        return self.mock_values.keys()

    def columns(self, table_name):
        return self.mock_values[table_name]