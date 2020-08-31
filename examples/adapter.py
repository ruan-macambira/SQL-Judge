from validate_schema.mock_adapter import MockAdapter
import json

class JSONAdapter(MockAdapter):
    def __init__(self, filepath):
        with open(filepath) as json_file:
            super().__init__(json.load(json_file))
