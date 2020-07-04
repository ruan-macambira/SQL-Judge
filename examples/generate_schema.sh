#!/bin/bash
this_folder=$(dirname $(realpath $0))
sqlite_file=${this_folder}/example_schema
dml_file=${this_folder}/schema.sql

sqlite3 ${sqlite_file} < ${dml_file}

echo $sqlite_file