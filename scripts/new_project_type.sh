#!/usr/bin/env bash

# bash scripts/new_project_type.sh Example

#$1 Firstcapital
#echo ${1,,} all lowercase
#echo ${1^^} all UPPERCASE

cp projecthandler/example_model._py projecthandler/${1,,}_model.py
sed -i -e "s/Exampletoken/$1/g" projecthandler/${1,,}_model.py
sed -i -e "s/exampletoken/${1,,}/g" projecthandler/${1,,}_model.py
sed -i -e "s/EXAMPLETOKEN/${1^^}/g" projecthandler/${1,,}_model.py

mkdir lib/${1,,}

cp lib/example/example_rdcl_graph._py lib/${1,,}/${1,,}_rdcl_graph.py
sed -i -e "s/Exampletoken/$1/g" lib/${1,,}/${1,,}_rdcl_graph.py
sed -i -e "s/exampletoken/${1,,}/g" lib/${1,,}/${1,,}_rdcl_graph.py
sed -i -e "s/EXAMPLETOKEN/${1^^}/g" lib/${1,,}/${1,,}_rdcl_graph.py

cp lib/example/example_parser._py lib/${1,,}/${1,,}_parser.py
sed -i -e "s/Exampletoken/$1/g" lib/${1,,}/${1,,}_parser.py
sed -i -e "s/exampletoken/${1,,}/g" lib/${1,,}/${1,,}_parser.py
sed -i -e "s/EXAMPLETOKEN/${1^^}/g" lib/${1,,}/${1,,}_parser.py

cp lib/example/__init__._py lib/${1,,}/__init__.py
sed -i -e "s/Exampletoken/$1/g" lib/${1,,}/__init__.py
sed -i -e "s/exampletoken/${1,,}/g" lib/${1,,}/__init__.py
sed -i -e "s/EXAMPLETOKEN/${1^^}/g" lib/${1,,}/__init__.py


