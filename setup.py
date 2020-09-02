"""Setup File"""
from setuptools import setup

setup(
    name='validate_schema',
    version='0.1b3',
    description='Validate SQL database Schemas using Python',
    author='MxBromelia',
    packages=['validate_schema', 'validate_schema.export', 'validate_schema.parse_configuration'],
    package_data={
        '': ['*.json']
    }
)
