#!/usr/bin/env bash

# clean_project_type
# usage:
# bash scripts/clean_project_type.sh Example

#$1 Firstcapital
#echo ${1,,} all lowercase
#echo ${1^^} all UPPERCASE


rm projecthandler/${1,,}_model.py

rm -r lib/${1,,}

rm -r projecthandler/template/project/${1,,}

