#!/usr/bin/env bash

# new_project_type
# usage:
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

#usecases

mkdir usecases/${1^^}


#html templates

mkdir projecthandler/template/project/${1,,}
cp -r projecthandler/template/project/example/* projecthandler/template/project/${1,,} 

find projecthandler/template/project/${1,,} -name "*example*" -exec rename "s/example/${1,,}/g" {} \;

