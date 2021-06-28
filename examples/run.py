from pathlib import Path
from adapter import JSONAdapter
import examples
from sql_judge import judge

# Roundabout way of opening "schema.json" in order to properly run when called by nox
# in the parent folder
adapter_file = Path(__file__).parent / 'schema.json'

if __name__ == '__main__':
    judge(
        adapter=JSONAdapter(adapter_file),
        validations_module=examples,
        ignore_tables=['metainfo']
    )
