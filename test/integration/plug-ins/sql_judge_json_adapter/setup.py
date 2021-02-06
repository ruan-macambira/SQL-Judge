from setuptools import setup

setup(
    name='sql-judge-json-adapter',
    install_requires='sql-judge',
    entry_points = {
        'sql_judge.adapter': ['json_adapter = json_adapter']
    },
    py_modules=['json_adapter']
)