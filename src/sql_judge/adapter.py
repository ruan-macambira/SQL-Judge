""" Database adapters """
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
class AbstractAdapter(ABC):
    """
    The main and only source for building the schema.

    All the methods in this interface are mandatory. If you do not want to add a specific element
    to the schema to be built, implement the given function returning an empty list([]).
    Note, however, that not putting elements that are related to others, namely tables and
    columns, it may cause unexpected behavior

    The methods can be classified in two types: entity methods and relation method.

    Entity Methods are the ones that are used to generate an entity(table, column, etc.),
    and they need to return a list of dicts.
    Many of these methods also need to inform its relation to another entities, but its main purpose
    is to inform what are the entities in the database and what properties
    should this given object have, and the values it returns.

    Entity methods have a dict to represent an entity because it allows you to pass
    any kind of parameter of an object you want,
    at the same it that it does not enforce any of them besides its name
    and its relations to another entities. So, for example,
    if you want to make a validation that utilizes its data type,
    add a key which value is the column data type ('data_type', for example),
    and you will be able to access
    this information through the object as a method (column.data_type, for example).

    Relation methods are, in the other hand, used to inform certain relationships between entities,
    specifically primary and foreign keys.
    This information is presented separated from the column method
    in order to not insert a disproportional amount of logic inside one method(columns).
    They need to return a list of tuples, or at least in an ordered object(like a list)
    the information in what needs to appear
    and in which order is explained in more detail in each method docstring.
    """
    @abstractmethod
    def tables(self) -> List[Dict[str, str]]:
        """Return a list containing a dict for every table in the schema

         mandatory keys:
          - name: The Table name
         forbidden keys:
          - columns
          - triggers
        """
        raise NotImplementedError

    @abstractmethod
    def columns(self) -> List[Dict[str, str]]:
        """Return a dict for every column in the schema

         mandatory keys:
          - name: The Column name
          - table: The name of the Table that owns the column
         forbiddent keys:
          - constraints
          - indexes
          - primary_keys
          - references
        """
        raise NotImplementedError

    @abstractmethod
    def triggers(self) -> List[Dict[str, str]]:
        """Return a list of dicts, each representing one of every triggers in the schema

        mandatory keys:
         - name: the Trigger name
         - table: The Name of the Table that owns it
        """
        raise NotImplementedError

    @abstractmethod
    def primary_keys(self) -> List[Tuple[str, str]]:
        """Return a tuple for every table that contains one primary key.
        If the said table has no primary key, do not put the table at all.

        The tuple must have the table name as its first element, and the name
        of the column that is its primary key as it's second. Currently does not
        support primary keys with multiple columns.
        """
        raise NotImplementedError

    @abstractmethod
    def references(self) -> List[Tuple[str, str, str]]:
        """Return a tuple for every column that is a foreign key for a table, ordered by:

        (the name of the column table, the column name, the name of the referenced table)
        If a column is not a reference for any table, it should not appear in this list at all.
        """
        raise NotImplementedError

    @abstractmethod
    def indexes(self) -> List[Dict[str, str]]:
        """ Return a dict for every index int the schema

        mandatory keys:
         - name: the Index name
         - column: the column bound with the index
        currently, it does not support a multi-column index """
        raise NotImplementedError

    @abstractmethod
    def constraints(self) -> List[Dict[str, str]]:
        """Return a dict for every constraint present in the schema

        mandatory keys:
         - name: the Constraint name
         - column: the column bound with constraint
        """
        raise NotImplementedError

    @abstractmethod
    def functions(self) -> List[Dict[str, str]]:
        """Return a dict for every function present in the schema

        mandatory keys:
         - name: the function name
        """
        raise NotImplementedError

    @abstractmethod
    def procedures(self) -> List[Dict[str, str]]:
        """Return a dict for every procedure present in the schema

        mandatory keys:
         - name: the procedure name
        """
        raise NotImplementedError

    @abstractmethod
    def sequences(self) -> List[Dict[str, str]]:
        """Return a dict for every sequence present in the schema

        mandatory keys:
         - name: the sequence name
        """
        raise NotImplementedError
