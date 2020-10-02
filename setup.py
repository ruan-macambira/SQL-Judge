"""Setup File"""
from setuptools import setup

setup(
    name='sql_judge',
    version='0.1b3',
    description='Validate SQL database Schemas using Python',
    author='MxBromelia',
    packages=['sql_judge', 'sql_judge.export', 'sql_judge.parse_configuration'],
    package_data={
        '': ['*.json']
    }
)
