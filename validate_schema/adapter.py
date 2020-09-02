""" Database adapters """
from typing import List, Dict, Optional, Tuple
class DBAdapter:
    """ Specify the methods a Database Connection must have.
    In order to the Schema Builder work properly, every function
    in this class must be implemented as oriented by its docstring.
    It is recommended that the user utilizes this class as the adapter
    parent class, since doing it will make the linter warn about not implemented
    methods, and mypy will be able to identify if both the signature and
    return types are in accordance with the abstract method, though it is not
    mandatory."""

    def tables(self) -> List[str]:
        """Should return a List of string the names of the tables in the schema"""
        raise NotImplementedError

    def columns(self) -> List[Tuple[str,...]]:
        """Should reveice as an argument one table name provided by
        self.tables, and return a Dict containing its columns.
        The Key of the dict should be the column name,
        while its value should be the column type.

        Note that every table name provided in self.tables will be used
        as an argument when calling this function"""
        raise NotImplementedError

    def triggers(self) -> List[Tuple[str,...]]:
        """Should Receive as argument the table name, and returns a Dict with its
        associated triggers. The key should be its name, while the value should be the 'hook',
        i.e when that trigger is triggered (ex.: AFTER INSERT)
        If there is no trigger associated to the table, it should retutn an empty trigger.

        Note that every table name provided in self.tables will be used
        as an argument when calling this function"""
        raise NotImplementedError

    def primary_keys(self) -> List[Tuple[str,...]]:
        """Should receive as an argument a table name and one of its columns name, and return
        a boolean indicating if the specified table is a primary_key(True if yes, False if no).

        Note that every column name provided in self.columns for every table provided in
        self.tables will be used as an argument when calling this function"""
        raise NotImplementedError

    def references(self) -> List[Tuple[str,...]]:
        """Should receive as an argument a table name and one of its column names, and return
        a the name of the table it references if there is one, and None if there is none. The
        table name must be one specified in self.tables.

        Note that every column name provided in self.columns for every table provided in
        self.tables will be used as an argument when calling this function"""
        raise NotImplementedError

    def indexes(self) -> List[Tuple[str,...]]:
        """ Return the indexes assigned a column in a table """
        raise NotImplementedError

    def constraints(self) -> List[Tuple[str,...]]:
        """Should receive as arguments a table nem and the name of one of its columns, and return
        a Dict with its associated Constraints. The Key shoulde be the name,
        while its value should be the type (ex.: NOT NULL, UNIQUE, CHECK).
        In case no constraints are associated with the column, it should return an empty Dict

        Note that every column name provided in self.columns for every table provided in
        self.tables will be used as an argument when calling this function"""
        raise NotImplementedError

    def functions(self) -> List[str]:
        """Should return a List of string with the names of the functions in the schema"""
        raise NotImplementedError

    def procedures(self) -> List[str]:
        """Should return a List of string with the names of the procedures in the schema"""
        raise NotImplementedError

    def sequences(self) -> List[str]:
        """Should return a List of strings with the names of the sequences in the schema"""
        raise NotImplementedError
