from validate_schema.serialized_adapter import SerializedAdapter
import json

class JSONAdapter(SerializedAdapter):
    def __init__(self, filepath):
        with open(filepath) as json_file:
            super().__init__(json.load(json_file))
