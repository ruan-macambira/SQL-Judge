"""Setup File"""
from setuptools import setup, find_packages

def long_description(): # pylint: disable=missing-function-docstring
    with open('README.md', 'r') as file:
        return file.read()

setup(
    name='sql_judge',
    version='0.1b5',
    description='Validate SQL database Schemas using Python',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='MxBromelia',
    packages= find_packages(where='src'),
    package_dir={"": "src"},
    package_data={
        '': ['*.json']
    }
)
