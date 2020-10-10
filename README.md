# SQL Judge, a tool for validation Relational Databases Schemas (SQL)

Also avaliable in [PT-BR](https://github.com/MxBromelia/SQL-Judge/blob/master/doc/README_pt-br.md)

## Goals
SQL Judge has a goal to allow writing database schema validations that are easily testable and portable between different Database implementations (Postgres, MariaDB, MySQL, etc.)

It achieves the first by making the validations pure python functions that are executed as-is in the validation, needing only an decorator to being recognized as one, making the function testable through regular python unit testing tools (such as unittest and pytest).

The second is achieved by utilizing a independent, user-provided way to access the database (see [Adapters](#Adapters))

## Install
```
pip install sql_judge
```

## How to Use
In order to use the tool, the user must pass a configuration file in JSON format. For example, if you have the configuration in a file called ```config.json```, it would execute the tool with:

```bash
python -m sql_judge config.json
```

Currently, all configuration options must be passed through a configuration file. You can, however, pass multiple files, like this:

```bash
python -m sql_judge config.json another_config.json
```

In case of conflict between the two files, the latter has preference.

### Setting up a configuration file
The configuration file must be formatted correctly ni order to the program to execute properly. Here is a guide in how to fill it properly:

The SQL Judge configuration has the following format, with a more detailed information below it:
```json
{
  "adapter": {
    "module": "adapter_module",
    "class": "AdapterClass",
    "params": ["posarg1"],
    "named_params": { "namedarg1": "value1"}  
  },
  "validations": {
    "module": "validations_module"
  },
  "ignore_tables": ["ignored_table"],
  "export": {
    "format": "\"CLI\" or \"CSV\""
  }
}
```

**adapter**: options regarding the adapter(see [Adapters](#Adapters) for more info), it has the following options:
 - module *(mandatory)*: The python module containing the adapter
 - class *(mandatory)*: The Adapter class presented in the module
 - params *(optional)*: unnamed parameters passed to the Adapter constuctor
 - named_params *(optional)*: named parameters passed to the Adapter constructor

**validations**: Options regarding the schema validations:
 - module *(mandatory)*: The module containing the validations functions

**ignore_tables** (*optional, default: []*): Pass which tables should not be included in the module validation, dicriminated by the name and name only(i.e does not support pattern matching _yet_).

**export**: The generated report format. *Currently it has no option but show te report in the stdout, not passing to a file*
 - format (*optional, options: [CLI, CSV], default: CLI*)

 _OBS: Since the tool deals with python modules instead of pure text files, the modules passed to the configuration file must be in the sys.PATH. If the files are in the same folder that the tool is invoked should cause no problems._
 
## Adapters
Adapters are the way SQL Judge has access to the database schema. The user provides through the configuration file a class that acts as it. This class must implement the same interface that ```AbstractAdapter``` present in ```src/sql_judge/adapter.py``` has. More information in how to implement such class is presented in the class and methods docstrings.

The idea is that, in the future, these adapters will be able to be passed through plug-ins.

## Writing Validations
In order to have the validations tested against the schema, the user must create a python module containing the validations, and which entities they should validate against. A validation is recognized by the program when a function is decorated with ```validates```. The program assumes each validation follow this behavior:

 - A validation must be decorated with ```validates```, passing the entity it will be validated against(ex.: Tables, Columns)
   - Obs.: Currently, it needs to pass the entity capitalized and in plural - Tables and Indexes instead of table and index, for example.
 - The given function must have one, and only one, parameter, that will represent the entity to be validated.
 - When given entity follows the rule present in the validation, the function must return None
 - When given entity does not follow the rule present in the validation, the function must return a string, preferably detailing the reason it failed, since the string will be passed to the report

Here's an example of a validation module

```python
from sql_judge import validates # Decorator that marks functions as validations

def not_a_validation(): # Since it does not have the decorator, it is not recognized as a validation

@validates('Tables') # Makes the function a validation of tables
def table_must_start_with_tbl(table):
  if table.name[0:4] != 'tbl_':
    return None # Return None if the entity follows the rule

  # Return a string containing the error when it does not follow the rule
  return 'Table must start with "tbl_"'
```

## Entities API
SQL Judge's Schema builder supports the following databases entities:
 - Tables;
 - Functions;
 - Procedures;
 - Columns;
 - Triggers;
 - Indexes;
 - Constraints;
 - Sequences;

By default, each entity provides its name and its relation to others entities (columns associated to a table, for example). You can pass another details about a given entity through the adapter. The properties can be accessed by calling by the key provided in the adapter. So, if you passed in the columns an aditional key 'type', you would acces it by using ```column.type```. Note that all the properties are accessed through properties, not methods. Following, the minimal interface that each entity has that exists by default:

### Schema
|Property   |Return Type       |Description              |  
|-----------|------------------|-------------------------|  
|tables     |List[Table]       |Schema Tables            |  
|functions  |List[Entity]      |Schema Functions         |  
|procedures |List[Entity]      |Schema Procedures        |  
|sequences  |List[Entity]      |Schema sequences         |  
|columns    |List[Column]      |Schema Table Columns     |  
|triggers   |List[TableEntity] |Schema Table Triggers    |  
|indexes    |List[ColumnEntity]|Schema Column Indexes    |  
|constraints|List[ColumnEntity]|Schema Column constraints|  

### Properties commom to all Entities
|Property|Return Type|Description                                                 |  
|--------|-----------|------------------------------------------------------------|  
|name    |str        |Entity name                                                 |  
|schema  |Schema     |Main Object, able to access every schema entity             |  

### Table
|Property   |Return Type      |Description       |      
|-----------|-----------------|------------------|  
|columns    |List[Column]     |Table Columns     |  
|triggers   |List[TableEntity]|Table Triggers    |  
|primary key|Column           |Primary Key Column|

### Properties commom to Column, Trigger, Constraint and Index
|Property|Return Type|Description                   |      
|--------|-----------|------------------------------|  
|table   |Table      |Table that contains the entity|

### Column
|Property   |Return Type       |Description                                                                         |      
|-----------|------------------|------------------------------------------------------------------------------------|  
|primary_key|boolean           |True if the column is the primary key. False if not                                 |
|references |Table             |If column has a foreign key constraint, returns the table it references. None if not|
|indexes    |List[ColumnIndex] |Column Indexes                                                                      |
|constraints|List[ColumnEntity]|Column Constraints                                                                  |

### Properties commom to Index and Constraint
|Property|Return Type|Description                    |      
|--------|-----------|-------------------------------|  
|column  |Column     |Column that contains the Entity|
