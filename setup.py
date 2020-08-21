"""Setup File"""
from setuptools import setup

setup(
    name='sql_schema_validator',
    version='0.alpha',
    description='Validate SQL database Schemas using Python',
    author='MxBromelia',
    packages=['validate_schema', 'validate_schema.export']
)
